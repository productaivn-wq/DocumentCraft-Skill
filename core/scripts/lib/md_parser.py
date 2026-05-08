"""Shared Markdown-to-HTML parser for DocumentCraft."""

import markdown
from typing import Tuple


def read_markdown(file_path: str) -> Tuple[str, dict]:
    """Read a Markdown file and convert it to structural HTML.

    Args:
        file_path: Absolute or relative path to the .md file.

    Returns:
        Tuple containing:
        - HTML string suitable for injection into PDF or DOCX renderers.
        - Dict of metadata extracted from YAML frontmatter.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    md = markdown.Markdown(extensions=["tables", "fenced_code", "meta", "toc", "codehilite"])
    html = md.convert(md_text)
    
    # python-markdown meta extension returns dict with list values
    # e.g., {'title': ['My Title']}
    # We flatten it to a simple dict if there's only one item
    meta = {}
    if hasattr(md, "Meta"):
        for k, v in md.Meta.items():
            meta[k] = v[0] if len(v) == 1 else v
            
    # Inject Table of Contents if requested
    toc_flag = str(meta.get("toc", "")).lower()
    if toc_flag in ("true", "yes", "1"):
        if hasattr(md, "toc") and "<div" in md.toc:
            html = f'<div style="page-break-after: always;"><h2 style="border-bottom: 2px solid #ccc; padding-bottom: 10px;">Table of Contents</h2>{md.toc}</div>\n' + html
            
    return html, meta
