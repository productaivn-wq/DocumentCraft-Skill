import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches


def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')

    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        borders.append(border)

    tblPr.append(borders)

def apply_docx_theme(docx_path):
    doc = docx.Document(docx_path)

    for table in doc.tables:
        set_table_borders(table)

        if len(table.columns) == 5:
            widths = (Inches(0.5), Inches(1.8), Inches(1.2), Inches(2.5), Inches(2.5))
        else:
            widths = [Inches(1.5)] * len(table.columns)

        for row in table.rows:
            for idx, width in enumerate(widths):
                if idx < len(row.cells):
                    row.cells[idx].width = width

            for cell in row.cells:
                text = cell.text
                if "•" in text:
                    new_text = text.replace("•", "\n•").strip()
                    if new_text.startswith("\n"):
                        new_text = new_text[1:]
                    new_text = new_text.replace(" \n", "\n")
                    new_text = new_text.replace("\n\n", "\n")
                    cell.text = new_text

    doc.save(docx_path)
