import os
import subprocess

from lib.themes_pdf import get_pdf_css
from playwright.sync_api import sync_playwright


def generate_pdf(input_md, output_pdf):
    # 1. Convert Markdown to HTML using pandoc
    temp_html = output_pdf + ".temp.html"
    result = subprocess.run(["pandoc", "-s", "--metadata", "title=Document", "-o", temp_html, input_md], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc HTML generation failed: {result.stderr}")

    # 2. Inject CSS theme
    css = get_pdf_css()
    with open(temp_html, encoding='utf-8') as f:
        html_content = f.read()

    if "</head>" in html_content:
        html_content = html_content.replace("</head>", f"<style>\n{css}\n</style>\n</head>")
    else:
        html_content = f"<style>\n{css}\n</style>\n" + html_content

    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 3. Print HTML to PDF using Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}")
        page.pdf(path=output_pdf, format="A4", margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"}, print_background=True)
        browser.close()

    # Cleanup
    if os.path.exists(temp_html):
        os.remove(temp_html)
