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


def generate_single(html_content: str, theme_name: str, output_path: str) -> None:
    """Generate a single PDF with the specified theme.

    Args:
        html_content: HTML string to render.
        theme_name: Key from PDF_THEMES (minimal, corporate, darkmode).
        output_path: Destination file path.
    """
    if theme_name not in PDF_THEMES:
        raise ValueError(f"Unknown PDF theme '{theme_name}'. Available: {list(PDF_THEMES.keys())}")
    css = PDF_THEMES[theme_name]
    print(f"  [PDF] Generating {os.path.basename(output_path)} ({theme_name})...")
    asyncio.run(_render_pdf(html_content, css, output_path))
    print(f"  [PDF] Saved: {output_path}")


def generate_all(md_file: str, output_dir: str, themes: Optional[list[str]] = None,
                 parallel: bool = True) -> list[str]:
    """Generate PDFs for multiple themes.

    Args:
        md_file: Path to the source Markdown file.
        output_dir: Directory to write output PDFs.
        themes: List of theme names, or None for all themes.
        parallel: If True, render themes concurrently via threads.

    Returns:
        List of output file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    html_content = read_markdown(md_file)
    theme_list = themes or list(PDF_THEMES.keys())
    base = os.path.splitext(os.path.basename(md_file))[0]

    paths = []
    threads = []

    for theme_name in theme_list:
        out_path = os.path.join(output_dir, f"{base}_pdf_{theme_name}.pdf")
        paths.append(out_path)
        if parallel:
            t = threading.Thread(target=generate_single, args=(html_content, theme_name, out_path))
            threads.append(t)
        else:
            generate_single(html_content, theme_name, out_path)

    if parallel and threads:
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    return paths


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf.py <markdown_file> [output_dir]")
        sys.exit(1)
    md = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "./outputs"
    results = generate_all(md, out)
    print(f"\nGenerated {len(results)} PDFs.")
