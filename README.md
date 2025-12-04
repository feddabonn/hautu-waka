# Hautū Waka Build System

A modular build system that separates content from structure. Edit JSON files, run the build script, get a single HTML file.

## Directory Structure

```
hautu-waka-build/
├── data/
│   ├── intro.json      # Introduction section content
│   ├── stages.json     # The 6 stages with overlay content
│   ├── tools.json      # All 13 tools
│   ├── muscles.json    # All 27 muscles by dimension
│   └── sources.json    # Mycorrhizal network sources
├── template.html       # HTML structure, styles, JavaScript
├── build.py            # Combines data + template → output
├── docs/               # Generated files go here (for GitHub Pages)
│   └── hautu-waka.html
└── README.md           # This file
```

## Requirements

- Python 3.6 or later (no external packages needed)
- The diagram image file (`HautuWakaProcess.png`)

## Usage

### 1. Edit content

Open any JSON file in the `data/` folder and edit:

**intro.json** — Change the hook, add paragraphs, update attribution

**stages.json** — Edit stage descriptions, reflection questions, adjust hotspot positions

**tools.json** — Update tool descriptions, add video URLs, modify which muscles each tool develops

**muscles.json** — Edit muscle descriptions, update intro text

**sources.json** — Add readings, update links, reorganise categories

### 2. Run the build

```bash
python build.py
```

Or on some systems:

```bash
python3 build.py
```

### 3. Test the output

Open `docs/hautu-waka.html` in a browser. The diagram image needs to be in the same folder as the HTML file.

### 4. Deploy

Copy both files to your web server:
- `hautu-waka.html`
- `HautuWakaProcess.png`

Or embed via iframe:
```html
<iframe src="hautu-waka.html" width="100%" height="800px" frameborder="0"></iframe>
```

---

## Editing Guide

### Adding a video to a tool

In `tools.json`, find the tool and add the YouTube embed URL:

```json
{
  "id": "emotional-culture-deck",
  "name": "Emotional Culture Deck",
  "description": "...",
  "video": "https://www.youtube.com/embed/VIDEO_ID_HERE",
  ...
}
```

### Adjusting stage hotspot positions

In `stages.json`, each stage has a `hotspot` object:

```json
"hotspot": {
  "x_percent": 12,    # Distance from left edge (%)
  "y_percent": 18,    # Distance from top edge (%)
  "width_percent": 18, # Width of clickable area (%)
  "height_percent": 28 # Height of clickable area (%)
}
```

Adjust these values to match where the stage circles appear in your diagram.

### Adding a new source category

In `sources.json`, add to the `categories` array:

```json
{
  "id": "new-category",
  "name": "New Category Name",
  "description": "What this category contains.",
  "items": [
    {
      "name": "Item Name",
      "author": "Author Name",
      "link": "https://example.com"
    }
  ]
}
```

### Adding a new tool

In `tools.json`, add a new object to the array:

```json
{
  "id": "new-tool-id",
  "name": "New Tool Name",
  "description": "What the tool does...",
  "stages": ["whakariterite", "te-kitenga"],
  "muscles": ["muscle-id-1", "muscle-id-2"],
  "video": null,
  "source": "Where it came from"
}
```

Then update `stages.json` to include the tool ID in the relevant stages' `tools` arrays.

### Adding a new muscle

In `muscles.json`, find the appropriate dimension and add to its `muscles` array:

```json
{
  "id": "new-muscle-id",
  "name": "New Muscle Name",
  "description": "What this capability means...",
  "tools": ["tool-id-1", "tool-id-2"]
}
```

Then update `tools.json` to include the muscle ID in the relevant tools' `muscles` arrays.

---

## Modifying the Design

### Changing colours

Open `template.html` and find the CSS section. Look for colour values like:
- `#1A7F8E` — Teal (links, interactive elements)
- `#156A77` — Dark teal (hover states)
- `#333333` — Dark grey (primary text)
- `#666666` — Medium grey (secondary text)
- `#FAFAFA` — Light grey (background)

### Changing fonts

In `template.html`, find the Google Fonts link and the `font-family` declaration:

```html
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
body {
    font-family: 'Raleway', sans-serif;
}
```

Replace with another Google Font.

### Changing section order

In `template.html`, find the HTML section blocks and reorder them. Update the navigation links to match.

---

## Troubleshooting

**Hotspots aren't aligned with the diagram**
- Adjust the `x_percent`, `y_percent`, `width_percent`, `height_percent` values in `stages.json`
- The percentages are relative to the image dimensions

**Links between tools and muscles don't work**
- Check that IDs match exactly (case-sensitive, hyphenated)
- Tool IDs in `muscles.json` must match IDs in `tools.json`
- Muscle IDs in `tools.json` must match IDs in `muscles.json`

**Build script fails**
- Check JSON syntax — missing commas, unmatched brackets
- Use a JSON validator (many free ones online)
- Python error messages usually indicate which file has issues

**Diagram doesn't show**
- Make sure `HautuWakaProcess.png` is in the same folder as the HTML file
- Check the filename matches exactly (case-sensitive on some systems)

---

## Version History

**December 2025 (v2)**
- Restructured from overlay-heavy to scrolling page
- Separated content (JSON) from structure (template)
- Added build script for modular editing
