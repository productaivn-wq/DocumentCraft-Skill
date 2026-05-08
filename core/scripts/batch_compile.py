"""Batch compiler for DocumentCraft.

Recursively finds all Markdown files in an input directory and compiles them
using craft.py, preserving the original folder hierarchy in the output directory
to prevent filename collisions.
"""

import argparse
import glob
import os
import subprocess
import time

def find_markdown_files(input_dir: str) -> list[str]:
    """Recursively find all .md files in the input directory."""
    # Use glob with recursive=True
    search_pattern = os.path.join(input_dir, "**", "*.md")
    return [f for f in glob.glob(search_pattern, recursive=True) if os.path.isfile(f)]

def main():
    parser = argparse.ArgumentParser(description="Batch compile Markdown files using DocumentCraft")
    parser.add_argument("input_dir", help="Directory containing source Markdown files")
    parser.add_argument("--output-dir", default="./batch_outputs", help="Directory for generated PDFs and DOCXs")
    parser.add_argument("--brand-color", default=None, help="Optional hex color override (e.g., #FF5733)")
    
    args = parser.parse_args()
    
    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)
    
    # Path to the core craft.py script
    craft_script = os.path.join(os.path.dirname(__file__), "craft.py")
    
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return
        
    md_files = find_markdown_files(input_dir)
    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return
        
    print(f"Found {len(md_files)} markdown files. Starting batch compilation...\n")
    
    total_success = 0
    total_failed = 0
    start_time = time.time()
    
    for md in md_files:
        # Calculate relative path to preserve hierarchy
        rel_path = os.path.relpath(md, input_dir)
        rel_dir = os.path.dirname(rel_path)
        
        # Create corresponding output subdirectory
        target_out_dir = os.path.join(output_dir, rel_dir)
        os.makedirs(target_out_dir, exist_ok=True)
        
        print(f"Processing: {rel_path}")
        cmd = ["python", craft_script, "all", md, "--output-dir", target_out_dir]
        
        if args.brand_color:
            cmd.extend(["--brand-color", args.brand_color])
            
        try:
            res = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Parse output to show generated files summary
            stdout_lines = res.stdout.strip().splitlines()
            summary = [line for line in stdout_lines if line.startswith("[OK]")]
            if summary:
                print(f"  {summary[0]}")
            total_success += 1
        except subprocess.CalledProcessError as e:
            print(f"  Failed! Error:\n{e.stderr}")
            total_failed += 1

    elapsed = time.time() - start_time
    print(f"\n======================================")
    print(f"Batch Test Complete")
    print(f"======================================")
    print(f"Total processed: {len(md_files)}")
    print(f"Success: {total_success} files")
    print(f"Failed: {total_failed}")
    print(f"Output directory: {output_dir}")
    print(f"Time elapsed: {elapsed:.2f}s")

if __name__ == "__main__":
    main()
