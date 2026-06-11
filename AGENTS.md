# SAC Website - Repository Overview for AI Agents

## Purpose

This repository contains all assets and tools for building the **Student Activity Center (SAC) website** for IISER Kolkata. The website showcases 10 cultural clubs, their members, events, and achievements.

---

## Directory Structure

```
SAC_website/
├── assets/                          # RAW assets (original files from clubs)
│   ├── AARSHI - Drama Club/        # Drama/theatre club
│   ├── Arts Club of IISER Kolkata/  # Arts club
│   ├── Campus Radio IISER KOLKATA/  # Campus radio station
│   ├── IKQC - Quiz Club/           # Quiz club
│   ├── Literary Club/               # Literary/debate club
│   ├── Movie Club/                  # Film club
│   ├── Music Club/                  # Music club
│   ├── Nature Club/                 # Environment/nature club
│   ├── Nrutya - Dance Club/        # Dance club (largest dataset)
│   └── PIXEL-Photography Club/     # Photography club
│
├── processed/                       # PROCESSED assets (website-ready)
│   ├── <Club_Name>/                # Same structure as assets/
│   │   ├── *.md                    # Markdown files (club info, OBs, events)
│   │   ├── *_images/               # Extracted images from DOCX/PDF (WebP)
│   │   │   ├── img_001.webp
│   │   │   └── ...
│   │   ├── *.webp                  # Standalone images (converted)
│   │   └── *_pdf.md                # PDF-specific markdown (if DOCX exists)
│   └── assets_map.jsonl            # Master index of all processed files
│
├── tools/                           # Python processing tools
│   ├── pyproject.toml              # UV project config (Python 3.12)
│   ├── process_assets.py           # Main pipeline orchestrator
│   ├── image_converter.py          # Images → WebP (q85, max 2400px)
│   ├── docx_parser.py              # DOCX → Markdown + extract images
│   ├── pdf_parser.py               # PDF → Markdown + extract images
│   ├── file_renamer.py             # Spaces → underscores (Linux-friendly)
│   └── run.sh                      # Quick runner script
│
├── assets_map.jsonl                # Raw assets index (280 entries)
├── SAC Cultural Website Details-...zip  # Original zip from clubs
├── .gitignore
└── .git/                           # Remote: git@github.com:slashdot-iiserk/SAC_website.git
```

---

## Club Data Summary

### 1. AARSHI - Drama Club

- **Files:** 35 images, 1 markdown
- **Content:** Club intro, OB list (25-26, 26-27), IICM achievements (street play, group play, monodrama), event photos (Abhivyakti, Rangabhumi, Lakeer-e-Kabaddi)
- **Key data:** OB names with roles, IICM gold medals, event descriptions

### 2. Arts Club of IISER Kolkata

- **Files:** 6 images, 1 markdown
- **Content:** Club intro, logos (black/white variants), OB photos (26-27)
- **Key data:** Club description, OB details

### 3. Campus Radio IISER KOLKATA (IKCR)

- **Files:** 92 images, 2 markdown (DOCX + PDF versions)
- **Content:** richest dataset - CEO/CFO/COO/PRO positions, event photos (elections, cultural events, sports, interviews, Parakram Divas, Mahishasur Mardini), logos
- **Key data:** Full OB with designations, event categories, 3 logo variants

### 4. IKQC - Quiz Club of IISER Kolkata

- **Files:** 24 images, 1 markdown
- **Content:** Quiz events (Freshers, Dublin Wager, Inquizzitive), IICM achievements, OB list
- **Key data:** Event descriptions, achievement rankings, contact emails

### 5. Literary Club of IISER Kolkata

- **Files:** 9 images, 1 markdown
- **Content:** OB photos (25-26, 26-27), club description
- **Key data:** Secretary, Convenor, Treasurer, Event Manager details

### 6. Movie Club of IISER K

- **Files:** 33 images, 2 markdown (DOCX + PDF versions)
- **Content:** Movie screenings, interbatch events, OB photos
- **Key data:** Club assets, screening photos, social media info

### 7. Music Club of IISER K

- **Files:** 28 images, 1 markdown
- **Content:** IICM photos (mehfil, western, duet, bob), events (Rampage, Jhankaar, Voice), OB photos
- **Key data:** Event categories, OB with roles

### 8. Nature Club Of IISER Kolkata

- **Files:** 10 images, 1 markdown
- **Content:** Eco trails, field trips, OB photos (26-27)
- **Key data:** Club mission (biodiversity, conservation), OB contacts

### 9. Nrutya - Dance Club of IISER Kolkata (LARGEST)

- **Files:** 91 images, 1 markdown
- **Content:** IICM 2023/2024/2025 photos (dance battle, group dance, synchro, solo classical), outer fest achievements, interbatch competitions, Garba night, workshops
- **Key data:** Detailed OB list with phone/email, event categories, achievement history

### 10. PIXEL-Photography Club

- **Files:** 39 images, 4 markdown
- **Content:** Equipment showcase (Nikon, Sony, Kodak), portfolios, event photos (Photon, photowalks), IICM photos
- **Key data:** Equipment list, member portfolios, event documentation

---

## Data Types in Markdown Files

Each club's markdown file typically contains:

1. **Club Introduction** - Mission, vision, description
2. **Current Office Bearers (OBs)** - Names, roles, contact info (phone, email)
3. **Previous OBs** - Historical data
4. **Events** - Descriptions, categories
5. **Achievements** - IICM results, competition wins
6. **Tables** - Structured OB data, achievement records

---

## Tools Usage

### Run Full Pipeline

```bash
cd tools
./run.sh ../assets              # Process all raw assets
./run.sh ../assets --skip-rename  # Skip folder renaming
```

### Individual Tools

```bash
# Convert images only
uv run python image_converter.py ../assets -o ../processed

# Parse DOCX files only
uv run python docx_parser.py ../assets -o ../processed

# Parse PDF files only
uv run python pdf_parser.py ../assets -o ../processed

# Rename files/folders
uv run python file_renamer.py ../processed
```

### Adding New Assets

When new club data arrives (zip file):

1. Extract to `assets/` folder
2. Run `./run.sh ../assets` - pipeline handles everything
3. New files appear in `processed/` with WebP images and markdown

---

## Key Conventions

- **Images:** All converted to WebP format (quality 85, max 2400px)
- **File names:** Spaces replaced with underscores, special chars removed
- **Markdown:** Extracted from DOCX/PDF with embedded image references
- **Structure:** Club name → Category → Files (maintains original hierarchy)

---

## Website Data Access

For building the website, use:

- `processed/assets_map.jsonl` - Index of all processed files
- `processed/<Club>/*.md` - Club content (parsed text)
- `processed/<Club>/*.webp` - Club images
- `processed/<Club>/*_images/` - Extracted images from documents

---

## Processed Directory Tree

```
processed/
├── AARSHI_-_Drama_Club/
│   ├── 25-26_OBs/                    (3 member photos)
│   ├── 26-27_OBs/                    (5 member photos)
│   ├── EVENTS_PICS/                  (11 event photos)
│   ├── IICM_Achievements/            (15 competition photos)
│   ├── AARSHI_-_THE_DRAMA_CLUB.md    (club info + OB list)
│   └── AARSHI_-_THE_DRAMA_CLUB_images/ (1 extracted image)
│
├── Arts_Club_of_IISER_Kolkata/
│   ├── Logos/                        (2 logo variants)
│   ├── OBs_26-27/                    (2 member photos)
│   ├── Arts_Club_of_IISER_Kolkata.md
│   └── Arts_Club_of_IISER_Kolkata_images/ (2 extracted)
│
├── Campus_Radio_IISER_KOLKATA/
│   ├── Campus_Radio_Information/     (62 files: DOCX/PDF extracted)
│   ├── Campus_Radio_Logo/            (3 logo variants)
│   ├── Campus_Radio_Pictures/        (29 event/OB photos)
│   ├── Campus_Radio_Information.md   (DOCX version)
│   └── Campus_Radio_Information_pdf.md (PDF version)
│
├── IKQC_-_Quiz_Club_of_IISER_Kolkata/
│   ├── 26-27_Club_OBs/               (3 member photos)
│   ├── Event_Photographs/            (16 event photos)
│   ├── IICM_Photographs/             (2 competition photos)
│   ├── Logo/                         (3 logo variants)
│   └── IKQC_-_Quiz_Club_of_IISER_Kolkata.md
│
├── Literary_Club_of_IISER_Kolkata/
│   ├── 25-26_OBs/                    (3 member photos)
│   ├── 26-27_OBs/                    (5 member photos)
│   ├── Literery_Club.md
│   └── Literery_Club_images/         (1 extracted)
│
├── Movie_Club_of_IISER_K/
│   ├── Movie_Club_Information/       (25 files: DOCX/PDF extracted)
│   ├── Photos_Of_Movie_Club/         (10 screening/OB photos)
│   ├── Movie_Club_Information.md
│   └── Movie_Club_Information_pdf.md
│
├── Music_Club_of_IISER_K/
│   ├── 2026-27_OBs/                  (5 member photos)
│   ├── Event_Photos/                 (5 photos: Rampage, Jhankaar, Voice)
│   ├── IICM_Photos/                  (4 competition photos)
│   ├── Club_Report.md
│   └── Club_Report_images/           (14 extracted)
│
├── Nature_Club_Of_IISER_Kolkata/
│   ├── 26-27_OBs/                    (3 member photos)
│   ├── Event_Pics/                   (7 eco trail/field trip photos)
│   ├── NATURE_CLUB_SAC_WEBSITE.md
│   └── NATURE_CLUB_SAC_WEBSITE_images/ (0 - no images in DOCX)
│
├── Nrutya_-_The_Dance_Club_of_IISER_Kolkata/
│   ├── 25-26_OBs/                    (5 member photos + xlsx)
│   ├── 26-27_OBs/                    (5 member photos + xlsx)
│   ├── Event_Pics/                   (16: interbatch, garba, workshops)
│   ├── IICM_Pics/                    (61: IICM 2023/2024/2025)
│   ├── Outer_Fest_Achievement/       (4 winner photos)
│   ├── Past_OBs/                     (1 xlsx)
│   ├── Overall_Document/             (1 DOCX - club details)
│   └── Dance_Club_Details_.md        (comprehensive club info)
│
└── PIXEL-Photography_Club/
    ├── Equipments/                   (8 equipment photos)
    ├── Event_Pictures/               (5 event photos)
    ├── IICM/                         (2 competition photos)
    ├── New_OB_26-27_Term/            (4 member photos)
    ├── Portfolio_Pixel/              (15 portfolio images + USE_CASE.md)
    ├── Report_Compiled_Extra/        (7 files: DOCX/PDF extracted)
    ├── Pixel_Data_docx.md
    └── Pixel_Data_docx_images/       (1 extracted)
```

---

## Asset Counts

| Club                | Images  | Markdown | Extracted | Total   |
| ------------------- | ------- | -------- | --------- | ------- |
| AARSHI - Drama Club | 35      | 1        | 1         | 37      |
| Arts Club           | 6       | 1        | 2         | 9       |
| Campus Radio        | 92      | 2        | 60        | 154     |
| IKQC - Quiz Club    | 24      | 1        | 3         | 28      |
| Literary Club       | 9       | 1        | 1         | 11      |
| Movie Club          | 33      | 2        | 21        | 56      |
| Music Club          | 28      | 1        | 14        | 43      |
| Nature Club         | 10      | 1        | 0         | 11      |
| Nrutya - Dance Club | 91      | 1        | 0         | 92      |
| PIXEL - Photography | 39      | 4        | 2         | 45      |
| **TOTAL**           | **367** | **15**   | **104**   | **486** |

---

## Remote Repository

- **URL:** git@github.com:slashdot-iiserk/SAC_website.git
- **Branch:** (check with `git branch -a`)
