"""DOCX generation engine for DocumentCraft.

Uses python-docx + htmldocx to render Markdown into styled Word documents.
Supports parallel multi-theme generation via threading.
"""

import os
import threading
from typing import Callable, Optional

from docx import Document
from htmldocx import HtmlToDocx

from lib.md_parser import read_markdown
from lib.themes_docx import DOCX_THEMES


def _apply_table_borders(doc: Document) -> None:
    """Post-process: apply 'Table Grid' style to all tables for visible borders."""
    for table in doc.tables:
        try:
            table.style = "Table Grid"
        except KeyError:
            pass


def generate_single(html_content: str, theme_name: str, output_path: str) -> None:
    """Generate a single DOCX with the specified theme.

    Args:
        html_content: HTML string to inject.
        theme_name: Key from DOCX_THEMES (classic, minimalist, vibrant).
        output_path: Destination file path.
    """
    if theme_name not in DOCX_THEMES:
        raise ValueError(f"Unknown DOCX theme '{theme_name}'. Available: {list(DOCX_THEMES.keys())}")

    print(f"  [DOCX] Generating {os.path.basename(output_path)} ({theme_name})...")
    doc = Document()

    # Apply theme (mutates Word Styles XML)
    theme_func = DOCX_THEMES[theme_name]
    theme_func(doc)

    # Inject HTML content
    parser = HtmlToDocx()
    parser.add_html_to_document(html_content, doc)

    # Ensure all tables have visible borders
    _apply_table_borders(doc)

    doc.save(output_path)
    print(f"  [DOCX] Saved: {output_path}")


def generate_all(md_file: str, output_dir: str, themes: Optional[list[str]] = None,
                 parallel: bool = True) -> list[str]:
    """Generate DOCX files for multiple themes.

    Args:
        md_file: Path to the source Markdown file.
        output_dir: Directory to write output DOCX files.
        themes: List of theme names, or None for all themes.
        parallel: If True, render themes concurrently via threads.

    Returns:
        List of output file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    html_content = read_markdown(md_file)
    theme_list = themes or list(DOCX_THEMES.keys())
    base = os.path.splitext(os.path.basename(md_file))[0]

    paths = []
    threads = []

    for theme_name in theme_list:
        out_path = os.path.join(output_dir, f"{base}_docx_{theme_name}.docx")
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
        print("Usage: python generate_docx.py <markdown_file> [output_dir]")
        sys.exit(1)
    md = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "./outputs"
    results = generate_all(md, out)
    print(f"\nGenerated {len(results)} DOCX files.")
