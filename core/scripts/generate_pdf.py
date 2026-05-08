"""PDF generation engine for DocumentCraft.

Uses Playwright (headless Chromium) to render HTML+CSS into PDF.
Supports parallel multi-theme generation via threading.
"""

import asyncio
import os
import threading
from typing import Optional

from playwright.async_api import async_playwright

from lib.md_parser import read_markdown
from lib.themes_pdf import PDF_THEMES


def build_cover_page_html(metadata: dict) -> str:
    """Generate HTML for the cover page using parsed YAML metadata."""
    if not metadata:
        return ""
    
    title = metadata.get("title", "")
    subtitle = metadata.get("subtitle", "")
    brand = metadata.get("brand", "")
    date = metadata.get("date", "")
    
    # If no title, don't force a cover page
    if not title:
        return ""
        
    html = '<div style="margin-bottom: 100px; text-align: center; margin-top: 150px;">'
    if brand:
        html += f'<h3 style="color: gray; text-transform: uppercase;">{brand}</h3>'
    html += f'<h1 style="font-size: 36pt; border: none; padding-bottom: 0;">{title}</h1>'
    if subtitle:
        html += f'<h2 style="font-size: 20pt; color: gray; border: none; margin-top: 0;">{subtitle}</h2>'
    if date:
        html += f'<p style="margin-top: 50px; font-weight: bold;">{date}</p>'
    html += '</div><div style="page-break-after: always;"></div>'
    
    return html


async def _render_pdf(html_content: str, css_content: str, output_path: str) -> None:
    """Render HTML+CSS to PDF via headless Chromium."""
    full_html = (
        f"<!DOCTYPE html><html><head><style>{css_content}</style></head>"
        f"<body>{html_content}</body></html>"
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(full_html)
        await page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
        )
        await browser.close()


def generate_single(html_content: str, theme_name: str, output_path: str, brand_color: str = None) -> None:
    """Generate a single PDF with the specified theme.

    Args:
        html_content: HTML string to render.
        theme_name: Key from PDF_THEMES (minimal, corporate, darkmode).
        output_path: Destination file path.
        brand_color: Optional hex string to override theme colors.
    """
    if theme_name not in PDF_THEMES:
        raise ValueError(f"Unknown PDF theme '{theme_name}'. Available: {list(PDF_THEMES.keys())}")
    
    # PDF_THEMES now contains functions that return CSS
    theme_func = PDF_THEMES[theme_name]
    css = theme_func(brand_color)
    
    print(f"  [PDF] Generating {os.path.basename(output_path)} ({theme_name})...")
    asyncio.run(_render_pdf(html_content, css, output_path))
    print(f"  [PDF] Saved: {output_path}")


def generate_all(md_file: str, output_dir: str, themes: Optional[list[str]] = None,
                 parallel: bool = True, brand_color: str = None) -> list[str]:
    """Generate PDFs for multiple themes.

    Args:
        md_file: Path to the source Markdown file.
        output_dir: Directory to write output PDFs.
        themes: List of theme names, or None for all themes.
        parallel: If True, render themes concurrently via threads.
        brand_color: Optional hex string to override theme colors.

    Returns:
        List of output file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    html_content, metadata = read_markdown(md_file)
    
    # Inject cover page
    cover_html = build_cover_page_html(metadata)
    full_html_content = cover_html + html_content
    
    theme_list = themes or list(PDF_THEMES.keys())
    base = os.path.splitext(os.path.basename(md_file))[0]

    paths = []
    threads = []

    for theme_name in theme_list:
        out_path = os.path.join(output_dir, f"{base}_pdf_{theme_name}.pdf")
        paths.append(out_path)
        if parallel:
            t = threading.Thread(target=generate_single, args=(full_html_content, theme_name, out_path, brand_color))
            threads.append(t)
        else:
            generate_single(full_html_content, theme_name, out_path, brand_color)

    if parallel and threads:
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    return paths


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf.py <markdown_file> [output_dir] [brand_color]")
        sys.exit(1)
    md = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "./outputs"
    color = sys.argv[3] if len(sys.argv) > 3 else None
    results = generate_all(md, out, brand_color=color)
    print(f"\nGenerated {len(results)} PDFs.")
