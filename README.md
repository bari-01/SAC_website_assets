# SAC Website Assets

Processed assets, tools, and structured data for the **Student Activity Center (SAC) website** at IISER Kolkata.

## Quick Start

```bash
# Process new assets
cd tools
./run.sh ../assets

# Or process with specific options
./run.sh ../assets --skip-rename
```

## Repository Contents

```
SAC_website_assets/
├── processed/                    # Website-ready assets
│   ├── <Club_Name>/             # 10 cultural clubs
│   │   ├── *.md                 # Parsed markdown (OBs, events, achievements)
│   │   ├── *.webp               # Compressed images (q85, max 2400px)
│   │   └── *_images/            # Extracted images from DOCX/PDF
│   └── assets_map.jsonl         # Master index (382 entries)
│
├── tools/                        # Python processing pipeline
│   ├── pyproject.toml           # UV project (Python 3.12)
│   ├── process_assets.py        # Main orchestrator
│   ├── image_converter.py       # Images → WebP
│   ├── docx_parser.py           # DOCX → Markdown + images
│   ├── pdf_parser.py            # PDF → Markdown + images
│   ├── file_renamer.py          # Linux-friendly names
│   └── run.sh                   # Quick runner
│
└── AGENTS.md                     # AI agent reference guide
```

## Clubs Included

| Club                | Images | Markdown | Key Content                    |
| ------------------- | ------ | -------- | ------------------------------ |
| AARSHI - Drama      | 35     | 1        | OBs, IICM gold medals, events  |
| Arts Club           | 6      | 1        | Logos, OBs                     |
| Campus Radio (IKCR) | 92     | 2        | CEO/CFO/COO/PRO, events, logos |
| IKQC - Quiz         | 24     | 1        | Events, IICM achievements      |
| Literary            | 9      | 1        | OBs with contacts              |
| Movie Club          | 33     | 2        | Screenings, OBs                |
| Music Club          | 28     | 1        | IICM, events, OBs              |
| Nature Club         | 10     | 1        | Eco trails, OBs                |
| Nrutya - Dance      | 91     | 1        | IICM 2023-25, detailed OBs     |
| PIXEL - Photo       | 39     | 4        | Equipment, portfolios          |

**Total:** 367 images, 15 markdown files, 104 extracted images from documents

## Data Format

### Markdown Files

Each club markdown contains:

- Club introduction/mission
- Current Office Bearers (names, roles, phone, email)
- Previous OBs (historical)
- Events with descriptions
- IICM achievements and competition results
- Structured tables

### Images

- Format: WebP (quality 85, max 2400px)
- Names: Linux-friendly (underscores, no spaces)
- Structure: `club/category/filename.webp`

### Assets Map

`assets_map.jsonl` - One JSON entry per file:

```json
{
  "path": "Club_Name/category/file.webp",
  "club": "Club_Name",
  "category": "category",
  "filename": "file.webp",
  "extension": "webp",
  "type": "image"
}
```

## Adding New Assets

1. Extract new zip to `assets/` folder
2. Run `cd tools && ./run.sh ../assets`
3. New files appear in `processed/`
4. Push to this repository

## Remote

- **URL:** git@github.com:slashdot-iiserk/SAC_website_assets.git
- **Parent repo:** [SAC_website](https://github.com/slashdot-iiserk/SAC_website)
