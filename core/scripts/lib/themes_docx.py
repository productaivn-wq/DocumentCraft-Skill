"""Word Style theme definitions for DOCX generation via python-docx.

Each theme function mutates the styles of a python-docx Document object
to enforce a consistent visual identity across all structural elements.
"""

from docx import Document
from docx.shared import Pt, RGBColor


def hex_to_rgb(hex_str: str) -> RGBColor:
    """Convert a hex string like '#ff5733' to RGBColor."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = "".join(c + c for c in hex_str)
    return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))


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

def apply_theme_classic(doc: Document, brand_color_hex: str = None) -> None:
    """Corporate consulting theme — Arial, dark blue headers."""
    set_base_font(doc, "Arial", 11, RGBColor(51, 51, 51))
    primary = hex_to_rgb(brand_color_hex) if brand_color_hex else RGBColor(31, 73, 125)   # #1f497d
    secondary = RGBColor(54, 95, 145) if not brand_color_hex else primary
    _set_heading(doc, 1, "Arial", 20, primary)
    _set_heading(doc, 2, "Arial", 16, secondary)
    _set_heading(doc, 3, "Arial", 14, secondary)
    _set_heading(doc, 4, "Arial", 12, secondary)


# ──────────────────────────────────────────────
# Theme: Modern Minimalist
# ──────────────────────────────────────────────

def apply_theme_minimalist(doc: Document, brand_color_hex: str = None) -> None:
    """Clean minimalist theme — Georgia body, Helvetica headers."""
    set_base_font(doc, "Georgia", 11, RGBColor(0, 0, 0))
    grey = RGBColor(89, 89, 89)
    primary = hex_to_rgb(brand_color_hex) if brand_color_hex else RGBColor(0, 0, 0)
    _set_heading(doc, 1, "Helvetica", 24, primary, bold=False)
    _set_heading(doc, 2, "Helvetica", 18, grey, bold=False)
    _set_heading(doc, 3, "Helvetica", 16, grey)
    _set_heading(doc, 4, "Helvetica", 13, grey)


# ──────────────────────────────────────────────
# Theme: Vibrant
# ──────────────────────────────────────────────

def apply_theme_vibrant(doc: Document, brand_color_hex: str = None) -> None:
    """Bold vibrant theme — Segoe UI, purple/teal accents."""
    set_base_font(doc, "Segoe UI", 11, RGBColor(43, 43, 43))
    primary = hex_to_rgb(brand_color_hex) if brand_color_hex else RGBColor(128, 0, 128)
    secondary = RGBColor(0, 128, 128) if not brand_color_hex else primary
    _set_heading(doc, 1, "Segoe UI", 22, primary)
    _set_heading(doc, 2, "Segoe UI", 16, secondary)
    _set_heading(doc, 3, "Segoe UI", 14, primary)
    _set_heading(doc, 4, "Segoe UI", 12, secondary)


# Registry for easy lookup
DOCX_THEMES = {
    "classic": apply_theme_classic,
    "minimalist": apply_theme_minimalist,
    "vibrant": apply_theme_vibrant,
}
