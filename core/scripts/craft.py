import argparse
import os
import sys

from generate_docx import generate_docx
from generate_pdf import generate_pdf


def main():
    parser = argparse.ArgumentParser(description="DocumentCraft CLI")
    parser.add_argument("input_file", help="Path to the input markdown file")
    parser.add_argument("--format", choices=["docx", "pdf", "both"], default="docx", help="Output format")
    parser.add_argument("--output", help="Output file path (optional)")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} not found.")
        sys.exit(1)

    base_name = os.path.splitext(args.input_file)[0]

    if args.format in ["docx", "both"]:
        out_path = args.output if args.output and args.format == "docx" else f"{base_name}.docx"
        print(f"Generating DOCX: {out_path}")
        generate_docx(args.input_file, out_path)

    if args.format in ["pdf", "both"]:
        out_path = args.output if args.output and args.format == "pdf" else f"{base_name}.pdf"
        print(f"Generating PDF: {out_path}")
        generate_pdf(args.input_file, out_path)

    print("DocumentCraft execution completed successfully.")

if __name__ == "__main__":
    main()
