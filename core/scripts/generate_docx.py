import subprocess

from lib.themes_docx import apply_docx_theme


def generate_docx(input_md, output_docx):
    # Use pandoc to convert Markdown to DOCX
    result = subprocess.run(["pandoc", "-o", output_docx, input_md], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc failed: {result.stderr}")

    # Apply post-processing themes (borders, line breaks, widths)
    apply_docx_theme(output_docx)
