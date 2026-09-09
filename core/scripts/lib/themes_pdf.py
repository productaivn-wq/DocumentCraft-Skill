def get_pdf_css():
    return """
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 20px;
    }
    th, td {
        border: 1px solid #000;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    blockquote {
        border-left: 5px solid #3498db;
        padding-left: 15px;
        background-color: #f9f9f9;
        margin: 1.5em 0;
        padding-top: 5px;
        padding-bottom: 5px;
        font-style: italic;
    }
    """
