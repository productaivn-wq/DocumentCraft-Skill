"""DocumentCraft — Unified CLI for document generation.

Usage:
    python craft.py pdf  <markdown_file> [--output-dir DIR] [--theme THEME] [--brand-color HEX]
    python craft.py docx <markdown_file> [--output-dir DIR] [--theme THEME] [--brand-color HEX]
    python craft.py all  <markdown_file> [--output-dir DIR] [--brand-color HEX]
"""

import argparse
import os
import sys
import time

# Ensure lib/ is importable
sys.path.insert(0, os.path.dirname(__file__))

import generate_pdf
import generate_docx
from lib.themes_pdf import PDF_THEMES
from lib.themes_docx import DOCX_THEMES


def cmd_pdf(args: argparse.Namespace) -> None:
    """Generate PDF(s) from a Markdown file."""
    themes = [args.theme] if args.theme else None
    start = time.time()
    paths = generate_pdf.generate_all(
        md_file=args.markdown_file,
        output_dir=args.output_dir,
        themes=themes,
        parallel=not args.sequential,
        brand_color=args.brand_color,
    )
    elapsed = time.time() - start
    print(f"\n[OK] Generated {len(paths)} PDF(s) in {elapsed:.1f}s")
    for p in paths:
        print(f"   -> {p}")


def cmd_docx(args: argparse.Namespace) -> None:
    """Generate DOCX file(s) from a Markdown file."""
    themes = [args.theme] if args.theme else None
    start = time.time()
    paths = generate_docx.generate_all(
        md_file=args.markdown_file,
        output_dir=args.output_dir,
        themes=themes,
        parallel=not args.sequential,
        brand_color=args.brand_color,
    )
    elapsed = time.time() - start
    print(f"\n[OK] Generated {len(paths)} DOCX file(s) in {elapsed:.1f}s")
    for p in paths:
        print(f"   -> {p}")


def cmd_all(args: argparse.Namespace) -> None:
    """Generate both PDF and DOCX files (all themes)."""
    start = time.time()
    pdf_paths = generate_pdf.generate_all(
        md_file=args.markdown_file,
        output_dir=args.output_dir,
        parallel=not args.sequential,
        brand_color=args.brand_color,
    )
    docx_paths = generate_docx.generate_all(
        md_file=args.markdown_file,
        output_dir=args.output_dir,
        parallel=not args.sequential,
        brand_color=args.brand_color,
    )
    elapsed = time.time() - start
    total = len(pdf_paths) + len(docx_paths)
    print(f"\n[OK] Generated {total} documents in {elapsed:.1f}s")
    print(f"   PDFs:  {len(pdf_paths)}")
    print(f"   DOCX:  {len(docx_paths)}")
    for p in pdf_paths + docx_paths:
        print(f"   -> {p}")


def main():
    parser = argparse.ArgumentParser(
        prog="craft",
        description="DocumentCraft — Markdown to PDF/DOCX with beautiful themes",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # PDF subcommand
    pdf_parser = subparsers.add_parser("pdf", help="Generate PDF(s)")
    pdf_parser.add_argument("markdown_file", help="Path to the source Markdown file")
    pdf_parser.add_argument("--output-dir", default="./outputs", help="Output directory (default: ./outputs)")
    pdf_parser.add_argument("--theme", choices=list(PDF_THEMES.keys()), default=None,
                            help="Generate a single theme (default: all themes)")
    pdf_parser.add_argument("--brand-color", default=None, help="Hex color code (e.g., #FF5733) to override primary theme colors")
    pdf_parser.add_argument("--sequential", action="store_true", help="Disable parallel rendering")
    pdf_parser.set_defaults(func=cmd_pdf)

    # DOCX subcommand
    docx_parser = subparsers.add_parser("docx", help="Generate DOCX file(s)")
    docx_parser.add_argument("markdown_file", help="Path to the source Markdown file")
    docx_parser.add_argument("--output-dir", default="./outputs", help="Output directory (default: ./outputs)")
    docx_parser.add_argument("--theme", choices=list(DOCX_THEMES.keys()), default=None,
                             help="Generate a single theme (default: all themes)")
    docx_parser.add_argument("--brand-color", default=None, help="Hex color code (e.g., #FF5733) to override primary theme colors")
    docx_parser.add_argument("--sequential", action="store_true", help="Disable parallel rendering")
    docx_parser.set_defaults(func=cmd_docx)

    # All subcommand
    all_parser = subparsers.add_parser("all", help="Generate both PDF and DOCX (all themes)")
    all_parser.add_argument("markdown_file", help="Path to the source Markdown file")
    all_parser.add_argument("--output-dir", default="./outputs", help="Output directory (default: ./outputs)")
    all_parser.add_argument("--brand-color", default=None, help="Hex color code (e.g., #FF5733) to override primary theme colors")
    all_parser.add_argument("--sequential", action="store_true", help="Disable parallel rendering")
    all_parser.set_defaults(func=cmd_all)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
