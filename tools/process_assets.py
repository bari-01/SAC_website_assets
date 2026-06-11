#!/usr/bin/env python3
"""
SAC Asset Pipeline - Process raw assets into website-ready format.

Steps:
  1. Rename files/dirs to Linux-friendly names
  2. Convert images to compressed WebP
  3. Parse DOCX to Markdown + extract images
  4. Parse PDF to Markdown + extract images
  5. Generate final assets_map.jsonl
"""

import json
import os
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

from image_converter import process_directory as convert_images
from docx_parser import process_directory as parse_docx
from pdf_parser import process_directory as parse_pdf
from file_renamer import rename_tree


def generate_assets_map(processed_dir: Path) -> Path:
    """Generate assets_map.jsonl from processed directory."""
    entries = []

    for root, _, files in os.walk(processed_dir):
        for fname in sorted(files):
            fpath = Path(root) / fname
            rel = fpath.relative_to(processed_dir)

            parts = list(rel.parts)
            club = parts[0] if len(parts) > 1 else "root"
            category = parts[1] if len(parts) > 2 else "general"

            ext = fpath.suffix.lower()
            if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".bmp"):
                ftype = "image"
            elif ext in (".docx", ".doc"):
                ftype = "document"
            elif ext == ".pdf":
                ftype = "pdf"
            elif ext in (".xlsx", ".xls", ".csv"):
                ftype = "spreadsheet"
            elif ext in (".md", ".txt"):
                ftype = "text"
            else:
                ftype = "other"

            entries.append(
                {
                    "path": str(rel),
                    "club": club,
                    "category": category,
                    "filename": fname,
                    "extension": ext.lstrip("."),
                    "type": ftype,
                }
            )

    map_path = processed_dir / "assets_map.jsonl"
    with open(map_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    return map_path


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
        print("[1/6] Renaming files to Linux-friendly names...")
        stats = rename_tree(src)
        print(
            f"  Renamed: {stats['files_renamed']} files, {stats['dirs_renamed']} dirs\n"
        )

    print("[2/6] Converting images to WebP...")
    img_stats = convert_images(src, processed_dir, args.quality)
    print(
        f"  Converted: {img_stats['converted']}, Skipped: {img_stats['skipped']}, Errors: {img_stats['errors']}\n"
    )

    if not args.skip_docx:
        print("[3/6] Parsing DOCX files...")
        docx_stats = parse_docx(src, processed_dir)
        print(f"  Parsed: {docx_stats['processed']}, Errors: {docx_stats['errors']}\n")

    if not args.skip_pdf:
        print("[4/6] Parsing PDF files...")
        pdf_stats = parse_pdf(src, processed_dir)
        print(f"  Parsed: {pdf_stats['processed']}, Errors: {pdf_stats['errors']}\n")

    print("[5/6] Converting extracted images to WebP...")
    extract_stats = convert_images(processed_dir, processed_dir, args.quality)
    print(
        f"  Converted: {extract_stats['converted']}, Skipped: {extract_stats['skipped']}, Errors: {extract_stats['errors']}\n"
    )

    print("[6/6] Generating assets map...")
    map_path = generate_assets_map(processed_dir)
    print(f"  Map: {map_path}\n")

    print(f"{'=' * 60}")
    print("Pipeline complete!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
