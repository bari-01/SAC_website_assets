#!/usr/bin/env python3
"""
SAC Asset Pipeline - Process raw assets into website-ready format.

Steps:
  1. Rename files/dirs to Linux-friendly names
  2. Convert images to compressed WebP
  3. Parse DOCX to Markdown + extract images
  4. Parse PDF to Markdown + extract images
  5. Parse HTML to Markdown + convert images
  6. Convert extracted images to WebP
  7. Generate final assets_map.jsonl
"""

import os
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

from image_converter import process_directory as convert_images
from docx_parser import process_directory as parse_docx
from pdf_parser import process_directory as parse_pdf
from html_parser import process_directory as parse_html
from file_renamer import rename_tree
from generate_assets_map import generate_assets_map


def main():
    import argparse

    parser = argparse.ArgumentParser(description="SAC Asset Pipeline")
    parser.add_argument("source", help="Source assets directory")
    parser.add_argument(
        "-o", "--output", default="processed", help="Output subfolder name"
    )
    parser.add_argument("--skip-rename", action="store_true")
    parser.add_argument("--skip-images", action="store_true")
    parser.add_argument("--skip-docx", action="store_true")
    parser.add_argument("--skip-pdf", action="store_true")
    parser.add_argument("--skip-html", action="store_true")
    parser.add_argument("--quality", type=int, default=85, help="WebP quality")
    args = parser.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        print(f"Source not found: {src}", file=sys.stderr)
        sys.exit(1)

    processed_dir = src.parent / args.output
    processed_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"SAC Asset Pipeline")
    print(f"Source: {src}")
    print(f"Output: {processed_dir}")
    print(f"{'=' * 60}\n")

    if not args.skip_rename:
        print("[1/7] Renaming files to Linux-friendly names...")
        stats = rename_tree(src)
        print(
            f"  Renamed: {stats['files_renamed']} files, {stats['dirs_renamed']} dirs\n"
        )

    print("[2/7] Converting images to WebP...")
    img_stats = convert_images(src, processed_dir, args.quality)
    print(
        f"  Converted: {img_stats['converted']}, Skipped: {img_stats['skipped']}, Errors: {img_stats['errors']}\n"
    )

    if not args.skip_docx:
        print("[3/7] Parsing DOCX files...")
        docx_stats = parse_docx(src, processed_dir)
        print(f"  Parsed: {docx_stats['processed']}, Errors: {docx_stats['errors']}\n")

    if not args.skip_pdf:
        print("[4/7] Parsing PDF files...")
        pdf_stats = parse_pdf(src, processed_dir)
        print(f"  Parsed: {pdf_stats['processed']}, Errors: {pdf_stats['errors']}\n")

    if not args.skip_html:
        print("[5/7] Parsing HTML files...")
        html_stats = parse_html(src, processed_dir)
        print(f"  Parsed: {html_stats['processed']}, Errors: {html_stats['errors']}\n")

    print("[6/7] Converting extracted images to WebP...")
    extract_stats = convert_images(processed_dir, processed_dir, args.quality)
    print(
        f"  Converted: {extract_stats['converted']}, Skipped: {extract_stats['skipped']}, Errors: {extract_stats['errors']}\n"
    )

    print("[7/7] Generating assets map...")
    map_path = generate_assets_map(processed_dir)
    print(f"  Map: {map_path}\n")

    print(f"{'=' * 60}")
    print("Pipeline complete!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
