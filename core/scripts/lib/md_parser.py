"""Shared Markdown-to-HTML parser for DocumentCraft."""

import markdown


def read_markdown(file_path: str) -> str:
    """Read a Markdown file and convert it to structural HTML.

    Args:
        file_path: Absolute or relative path to the .md file.

    Returns:
        HTML string suitable for injection into PDF or DOCX renderers.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    return html
