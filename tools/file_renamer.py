#!/usr/bin/env python3
"""Rename files and directories to Linux-friendly names (underscores, lowercase)."""

import os
import re
import sys
from pathlib import Path


def sanitize_name(name: str) -> str:
    """Convert name to Linux-friendly format."""
    name = name.strip()
    name = re.sub(r"[\s]+", "_", name)
    name = re.sub(r"[^\w._-]", "", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")
    return name


def rename_tree(root: Path, dry_run: bool = False) -> dict:
    """Recursively rename files and directories bottom-up."""
    stats = {"files_renamed": 0, "dirs_renamed": 0, "skipped": 0}

    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for fname in filenames:
            src = Path(dirpath) / fname
            new_name = sanitize_name(fname)
            if new_name == fname:
                stats["skipped"] += 1
                continue
            dst = src.parent / new_name
            if dst.exists():
                stats["skipped"] += 1
                continue
            if not dry_run:
                src.rename(dst)
            stats["files_renamed"] += 1
            print(f"  FILE: {src.name} -> {new_name}")

        for dname in dirnames:
            src = Path(dirpath) / dname
            new_name = sanitize_name(dname)
            if new_name == dname:
                stats["skipped"] += 1
                continue
            dst = src.parent / new_name
            if dst.exists():
                stats["skipped"] += 1
                continue
            if not dry_run:
                src.rename(dst)
            stats["dirs_renamed"] += 1
            print(f"  DIR:  {src.name} -> {new_name}")

    return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Rename files/dirs to Linux-friendly names"
    )
    parser.add_argument("source", help="Source directory")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without renaming"
    )
    args = parser.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        print(f"Source not found: {src}", file=sys.stderr)
        sys.exit(1)

    print(f"Renaming: {src} {'(dry run)' if args.dry_run else ''}")
    stats = rename_tree(src, args.dry_run)
    print(
        f"\nDone: {stats['files_renamed']} files, {stats['dirs_renamed']} dirs renamed, {stats['skipped']} skipped"
    )


if __name__ == "__main__":
    main()
