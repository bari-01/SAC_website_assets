#!/usr/bin/env python3
"""Generate rich assets_map.jsonl from processed directory.

Produces structured metadata per file for website rendering:
  - path: relative path
  - club: club/organization
  - category: subfolder
  - filename: file name
  - extension: file extension
  - type: image/document/text
  - role: semantic role (OB, Event, Logo, IICM, etc.)
  - tenure: year/tenure if applicable
  - title: human-readable title
  - description: contextual description
  - tags: list of tags
"""

import json
import os
import re
from pathlib import Path


CLUB_NAMES = {
    "AARSHI_-_Drama_Club": "AARSHI - Drama Club",
    "Arts_Club_of_IISER_Kolkata": "Arts Club of IISER Kolkata",
    "Campus_Radio_IISER_KOLKATA": "Campus Radio IISER KOLKATA",
    "IKQC_-_Quiz_Club_of_IISER_Kolkata": "IKQC - Quiz Club of IISER Kolkata",
    "Literary_Club_of_IISER_Kolkata": "Literary Club of IISER Kolkata",
    "Movie_Club_of_IISER_K": "Movie Club of IISER K",
    "Music_Club_of_IISER_K": "Music Club of IISER K",
    "Nature_Club_Of_IISER_Kolkata": "Nature Club of IISER Kolkata",
    "Nrutya_-_The_Dance_Club_of_IISER_Kolkata": "Nrutya - The Dance Club of IISER Kolkata",
    "PIXEL-Photography_Club": "PIXEL - Photography Club",
}

CLUB_TAGS = {
    "AARSHI_-_Drama_Club": ["drama", "theatre", "acting", "stage"],
    "Arts_Club_of_IISER_Kolkata": ["arts", "visual", "creative"],
    "Campus_Radio_IISER_KOLKATA": ["radio", "media", "broadcast", "podcast"],
    "IKQC_-_Quiz_Club_of_IISER_Kolkata": ["quiz", "knowledge", "trivia"],
    "Literary_Club_of_IISER_Kolkata": ["literary", "debate", "writing"],
    "Movie_Club_of_IISER_K": ["movies", "film", "cinema", "screenings"],
    "Music_Club_of_IISER_K": ["music", "singing", "instruments"],
    "Nature_Club_Of_IISER_Kolkata": ["nature", "environment", "ecology"],
    "Nrutya_-_The_Dance_Club_of_IISER_Kolkata": [
        "dance",
        "performance",
        "choreography",
    ],
    "PIXEL-Photography_Club": ["photography", "camera", "visual"],
}


def extract_tenure(text: str) -> str | None:
    """Extract tenure/year from text."""
    m = re.search(r"(\d{2}-\d{2})", text)
    if m:
        return m.group(1)
    m = re.search(r"(20\d{2})", text)
    if m:
        return m.group(1)
    return None


def determine_role(path_parts: list[str], filename: str) -> str:
    """Determine semantic role of a file from its path and filename."""
    path_str = " ".join(path_parts).lower()
    fname_lower = filename.lower()

    if "logo" in path_str or "logo" in fname_lower:
        return "logo"
    if "ob" in path_str or "ob" in fname_lower or "/obs" in path_str:
        return "office-bearer"
    if "iicm" in path_str:
        return "iicm-achievement"
    if "event" in path_str:
        return "event"
    if "workshop" in path_str:
        return "workshop"
    if "equipment" in path_str or "cameras" in path_str:
        return "equipment"
    if "portfolio" in path_str:
        return "portfolio"
    if "ob-details" in fname_lower or "past" in path_str:
        return "ob-details"

    if filename.startswith("OB-"):
        return "office-bearer"
    if filename.startswith("nOB-"):
        return "office-bearer"

    if re.search(
        r"(CEO|CFO|COO|PRO|Secretary|Convener|Treasurer|President|VP|EO|EventOrganiser|EventOrganizer)_?\d{2}-\d{2}",
        filename,
        re.IGNORECASE,
    ):
        return "office-bearer"
    if re.search(
        r"(CEO|CFO|COO|PRO|Secretary|Convener|Treasurer|President|VP|EO)", filename
    ):
        return "office-bearer"

    if filename.startswith("AARSHI-"):
        return "event"
    if "OB_" in filename or "OB-" in filename:
        return "office-bearer"

    return "other"


def clean_title(title: str) -> str:
    """Clean filename into a human-readable title."""
    title = re.sub(
        r"\.(webp|jpg|jpeg|png|pdf|md|docx)$", "", title, flags=re.IGNORECASE
    )
    title = title.replace("_", " ").replace("-", " ")
    title = re.sub(r"\s+", " ", title).strip()
    return title


def extract_name_and_role(filename: str) -> tuple[str, str | None]:
    """Extract person name and their role from OB filenames."""
    name = ""
    role = None

    if filename.startswith("OB-") or filename.startswith("nOB-"):
        is_new = filename.startswith("nOB-")
        stripped = filename[4:] if is_new else filename[3:]
        stripped = re.sub(r"\.webp$", "", stripped)

        parts = stripped.split(" - ")
        if len(parts) >= 2:
            name = clean_title(parts[0])
            role = clean_title(parts[-1])
        else:
            name = clean_title(stripped)
        return name, role

    m = re.search(
        r"^([A-Za-z][A-Za-z .]+?)(CEO|CFO|COO|PRO|Secretary|Convener|Treasurer|President|VP|EO|EventOrganiser|EventOrganizer|EventOrganiser)_",
        filename,
    )
    if m:
        name = clean_title(m.group(1))
        role = clean_title(m.group(2))
        return name, role

    m = re.search(r"OB-([A-Za-z]+)_([A-Za-z]+)", filename)
    if m:
        name = f"{m.group(1)} {m.group(2)}"
        role_match = re.search(r"_([A-Z][a-z]+)\.webp$", filename)
        if role_match:
            role = role_match.group(1)
        return name, role

    base = re.sub(r"\.webp$", "", filename)
    base = re.sub(r"_\d{2}-\d{2}$", "", base)
    name = clean_title(base)
    return name, role


def build_description(path_parts: list[str], filename: str, role: str) -> str:
    """Build a contextual description for a file."""
    if role == "office-bearer":
        name, ob_role = extract_name_and_role(filename)
        tenure = extract_tenure(" ".join(path_parts))
        if ob_role and tenure:
            return f"{name} - {ob_role} ({tenure})"
        elif ob_role:
            return f"{name} - {ob_role}"
        else:
            return name
    elif role == "event":
        return clean_title(filename)
    elif role == "iicm-achievement":
        year = extract_tenure(" ".join(path_parts))
        if year:
            return f"IICM {year} - {clean_title(filename)}"
        return f"IICM Achievement - {clean_title(filename)}"
    elif role == "logo":
        return f"Logo - {clean_title(filename)}"
    elif role == "equipment":
        return f"Equipment - {clean_title(filename)}"
    elif role == "portfolio":
        return f"Portfolio - {clean_title(filename)}"
    else:
        return clean_title(filename)


def get_tags(club: str, path_parts: list[str], role: str) -> list[str]:
    """Build a list of tags for a file."""
    tags = list(CLUB_TAGS.get(club, []))

    if role == "office-bearer":
        tags.append("ob")
    elif role == "iicm-achievement":
        tags.extend(["iicm", "achievement", "competition"])
    elif role == "event":
        tags.append("event")
    elif role == "logo":
        tags.append("logo")
    elif role == "workshop":
        tags.append("workshop")
    elif role == "equipment":
        tags.append("equipment")
    elif role == "portfolio":
        tags.append("portfolio")

    tenure = extract_tenure(" ".join(path_parts))
    if tenure:
        tags.append(f"tenure-{tenure}")

    return tags


def generate_map(processed_dir: Path, output_path: Path) -> None:
    """Generate the assets_map.jsonl file."""
    entries = []

    for root, _, files in os.walk(processed_dir):
        for fname in sorted(files):
            if fname == "assets_map.jsonl":
                continue
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

            role = determine_role(parts, fname)
            description = build_description(parts, fname, role)
            tags = get_tags(club, parts, role)
            tenure = extract_tenure(" ".join(parts))
            if role == "office-bearer":
                name, _ = extract_name_and_role(fname)
                title = name
            elif role == "logo":
                title = description.replace("Logo - ", "")
            else:
                title = clean_title(fname)

            entry = {
                "path": str(rel),
                "club": club,
                "club_name": CLUB_NAMES.get(club, club),
                "category": category,
                "filename": fname,
                "title": title,
                "extension": ext.lstrip("."),
                "type": ftype,
                "role": role,
                "tenure": tenure,
                "description": description,
                "tags": tags,
            }
            entries.append(entry)

    with open(output_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    print(f"Generated {len(entries)} entries in {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate rich assets_map.jsonl")
    parser.add_argument("source", help="Processed assets directory")
    parser.add_argument("-o", "--output", default=None, help="Output path")
    args = parser.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        print(
            f"Source not found: {src}",
            file=sys.stderr if "sys" in dir() else __import__("sys").stderr,
        )
        exit(1)

    out = Path(args.output).resolve() if args.output else src / "assets_map.jsonl"
    generate_map(src, out)


if __name__ == "__main__":
    main()
