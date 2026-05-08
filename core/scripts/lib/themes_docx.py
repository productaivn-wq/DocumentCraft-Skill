"""Word Style theme definitions for DOCX generation via python-docx.

Each theme function mutates the styles of a python-docx Document object
to enforce a consistent visual identity across all structural elements.
"""

from docx import Document
from docx.shared import Pt, RGBColor


def set_base_font(doc: Document, font_name: str, size_pt: int, rgb_color: RGBColor) -> None:
    """Force the base font across all common structural Word styles.

    Word uses independent styles for lists, tables, and body text that often
    do NOT inherit from 'Normal'. This function explicitly sets the font on
    every structural style to guarantee consistency.
    """
    structural_styles = [
        "Normal", "Body Text", "List Paragraph", "List Bullet",
        "List Number", "Table Grid",
    ]
    for s in structural_styles:
        try:
            style = doc.styles[s]
            style.font.name = font_name
            style.font.size = Pt(size_pt)
            style.font.color.rgb = rgb_color
        except KeyError:
            pass


def _set_heading(doc: Document, level: int, font_name: str, size_pt: int,
                 rgb_color: RGBColor, bold: bool = True) -> None:
    """Set font properties for a heading level (1-4)."""
    try:
        style = doc.styles[f"Heading {level}"]
        style.font.name = font_name
        style.font.size = Pt(size_pt)
        style.font.bold = bold
        style.font.color.rgb = rgb_color
    except KeyError:
        pass


# ──────────────────────────────────────────────
# Theme: Classic Consulting
# ──────────────────────────────────────────────

def apply_theme_classic(doc: Document) -> None:
    """Corporate consulting theme — Arial, dark blue headers."""
    set_base_font(doc, "Arial", 11, RGBColor(51, 51, 51))
    blue = RGBColor(31, 73, 125)   # #1f497d
    blue2 = RGBColor(54, 95, 145)
    _set_heading(doc, 1, "Arial", 20, blue)
    _set_heading(doc, 2, "Arial", 16, blue2)
    _set_heading(doc, 3, "Arial", 14, blue2)
    _set_heading(doc, 4, "Arial", 12, blue2)


# ──────────────────────────────────────────────
# Theme: Modern Minimalist
# ──────────────────────────────────────────────

def apply_theme_minimalist(doc: Document) -> None:
    """Clean minimalist theme — Georgia body, Helvetica headers."""
    set_base_font(doc, "Georgia", 11, RGBColor(0, 0, 0))
    grey = RGBColor(89, 89, 89)
    _set_heading(doc, 1, "Helvetica", 24, RGBColor(0, 0, 0), bold=False)
    _set_heading(doc, 2, "Helvetica", 18, grey, bold=False)
    _set_heading(doc, 3, "Helvetica", 16, grey)
    _set_heading(doc, 4, "Helvetica", 13, grey)


# ──────────────────────────────────────────────
# Theme: Vibrant
# ──────────────────────────────────────────────

def apply_theme_vibrant(doc: Document) -> None:
    """Bold vibrant theme — Segoe UI, purple/teal accents."""
    set_base_font(doc, "Segoe UI", 11, RGBColor(43, 43, 43))
    purple = RGBColor(128, 0, 128)
    teal = RGBColor(0, 128, 128)
    _set_heading(doc, 1, "Segoe UI", 22, purple)
    _set_heading(doc, 2, "Segoe UI", 16, teal)
    _set_heading(doc, 3, "Segoe UI", 14, purple)
    _set_heading(doc, 4, "Segoe UI", 12, teal)


# Registry for easy lookup
DOCX_THEMES = {
    "classic": apply_theme_classic,
    "minimalist": apply_theme_minimalist,
    "vibrant": apply_theme_vibrant,
}
