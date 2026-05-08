"""CSS theme definitions for PDF generation via Playwright."""

def get_theme_minimal(brand_color: str = None) -> str:
    color = brand_color or "#333"
    return f"""
body {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
}}
h1, h2, h3, h4 {{ color: #111; font-weight: 600; }}
h1 {{ font-size: 24pt; border-bottom: 2px solid {color}; padding-bottom: 5px; }}
h2 {{ font-size: 18pt; margin-top: 1.5em; }}
h3 {{ font-size: 14pt; margin-top: 1.2em; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 10pt;
}}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f8f9fa; font-weight: bold; }}
"""

def get_theme_corporate(brand_color: str = None) -> str:
    primary = brand_color or "#0056b3"
    secondary = "#004494" if not brand_color else primary
    return f"""
body {{
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #2b2b2b;
}}
h1 {{ color: {primary}; font-size: 26pt; border-bottom: 3px solid {primary}; padding-bottom: 10px; }}
h2 {{ color: {secondary}; font-size: 18pt; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 2em; }}
h3 {{ color: {secondary}; font-size: 14pt; margin-top: 1.2em; }}
h4 {{ color: {primary}; font-size: 12pt; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 25px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}
th {{ background-color: {primary}; color: white; padding: 10px; text-align: left; }}
td {{ border-bottom: 1px solid #ddd; padding: 8px; }}
tr:nth-child(even) {{ background-color: #f9f9f9; }}
"""

def get_theme_darkmode(brand_color: str = None) -> str:
    accent = brand_color or "#bb86fc"
    return f"""
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #e0e0e0;
    background-color: #121212;
}}
h1, h2, h3, h4 {{ color: #ffffff; }}
h1 {{ text-align: center; font-size: 24pt; letter-spacing: 1px; color: {accent}; }}
h2 {{ border-left: 4px solid {accent}; padding-left: 10px; margin-top: 2em; }}
h3 {{ color: {accent}; font-size: 14pt; margin-top: 1.2em; }}
h4 {{ color: #03dac6; font-size: 12pt; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}}
th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
th {{ background-color: #1f1f1f; color: {accent}; }}
tr:nth-child(even) {{ background-color: #181818; }}
a {{ color: #03dac6; text-decoration: none; }}
"""

# Registry for easy lookup
PDF_THEMES = {
    "minimal": get_theme_minimal,
    "corporate": get_theme_corporate,
    "darkmode": get_theme_darkmode,
}
