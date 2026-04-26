---
name: deck
description: Generate, edit, and manage PowerPoint decks using OCTAVE company branding templates with shape-based diagrams. Use when the user needs to create presentations, edit existing decks, or reference existing slides.
model: opus
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebSearch, WebFetch
---

# Deck Generator — OCTAVE Branded

Generate and edit PowerPoint (.pptx) decks using OCTAVE company branding templates via `python-pptx`, with visually rich shape-based layouts.

## Skill Directory

All paths below are relative to this skill's directory.
- **Plugin mode (recommended):** `${CLAUDE_PLUGIN_ROOT}/skills/deck/` — works on both Claude Code and VS Code when installed as a plugin.
- **Standalone mode:** resolve relative to this file's location in the workspace.

Determine the skill directory at the start of every generation script:
```python
import os

# Plugin mode: CLAUDE_PLUGIN_ROOT is set automatically when installed as a plugin
SKILL_DIR = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
if SKILL_DIR:
    SKILL_DIR = os.path.join(SKILL_DIR, "skills", "deck")

# Fallback: find skill dir by scanning common locations
if not SKILL_DIR or not os.path.isfile(os.path.join(SKILL_DIR, "recipes.py")):
    for candidate in [
        os.path.join(os.getcwd(), "plugins", "base-tools", "skills", "deck"),
        os.path.join(os.getcwd(), ".claude", "skills", "deck"),
        os.path.expanduser("~/.claude/skills/deck"),
    ]:
        if os.path.isfile(os.path.join(candidate, "recipes.py")):
            SKILL_DIR = candidate
            break
```

## Commands

| Usage | What it does |
|-------|-------------|
| `/base-tools:deck` | Generate new deck from current conversation context |
| `/base-tools:deck "topic or instructions"` | Generate a deck on a specific topic |
| `/base-tools:deck edit <path> "instructions"` | Edit specific slides in an existing deck |
| `/base-tools:deck add <path> "instructions"` | Add new slides to an existing deck |
| `/base-tools:deck refer <path>` | Read existing deck into context |
| `/base-tools:deck refer <path> "create a new deck based on this"` | Reference one deck to create another |

For Windows paths, auto-convert: `C:\Users\...` → `/mnt/c/Users/...` (WSL only).

## Step 1: Understand the Context

Before generating, clarify:
1. **Audience?** (technical, business, mixed)
2. **How many slides?** Respect any stated limit strictly.
3. **Purpose?** (submission, demo, pitch, internal review)
4. **Real workflow?** Ask about actual people, pain points, context — don't assume.

## Step 2: Choose Template

Templates are **user-provided** — they are not included in the repo. Place your `.pptx` template files in the `templates/` directory next to this `SKILL.md`.

At runtime, scan the templates directory and present what's available:
```python
import glob
templates = glob.glob(os.path.join(SKILL_DIR, "templates", "*.pptx"))
for i, t in enumerate(templates, 1):
    print(f"{i}. {os.path.basename(t)}")
```

Ask the user which template to use (skip if only one exists or already specified).

> **Setup:** Copy your company `.pptx` templates into the `templates/` directory alongside this skill. The skill auto-detects any `.pptx` files placed there.

### Template Spec Guidelines

When working with a template for the first time, inspect its layouts:
```python
prs = Presentation(template_path)
for i, layout in enumerate(prs.slide_layouts):
    print(f"[{i}] {layout.name}")
    for ph in layout.placeholders:
        print(f"    PH{ph.placeholder_format.idx}: {ph.name}")
```
Use this to determine which layout indices and placeholder indices are available. Always clear unused placeholders.

## Step 3: Plan the Deck

Present a slide-by-slide outline before coding. Wait for user approval.

```
DECK PLAN: [Title] — [N] slides

| # | Title | Key Message | Visual Approach |
|---|-------|-------------|-----------------|
| 1 | ... | one sentence takeaway | brief layout idea |
```

If the plan exceeds the slide count, propose merges. Iterate until approved.

## Step 4: Generate the Deck

### Load Helpers & Create Deck
```python
import os
exec(open(os.path.join(SKILL_DIR, "recipes.py")).read())

# For NEW decks — removes template sample slides, gives clean starting point:
prs = new_deck(os.path.join(SKILL_DIR, "templates", "<template_filename>"))

# For EDITING existing decks — load as-is:
prs = Presentation("<path>")
```

### Available Helpers

See [recipes.py](recipes.py) for full implementation. Summary:

| Helper | Purpose |
|--------|---------|
| `sf(run, size, bold, color, italic)` | Style a font run |
| `box(sl, l, t, w, h, text, fill, fc, fs, bold, align, radius)` | Filled rounded rectangle with text |
| `obox(sl, l, t, w, h, text, border_color, fc, fs, bold, align, radius, border_width)` | Outlined box (white fill, colored border) |
| `mbox(sl, l, t, w, h, lines, fill, ...)` | Multi-line box — lines = [(text, size, bold, color), ...] |
| `txt(sl, l, t, w, h, text, fs, color, bold, align, italic)` | Text box |
| `mtxt(sl, l, t, w, h, lines, align)` | Multi-line text box — lines = [(text, size, bold, color), ...] |
| `ar(sl, l, t, w, h)` | Right arrow |
| `ad(sl, l, t, w, h)` | Down arrow |
| `circ(sl, l, t, sz, fill, text, fc, fs)` | Circle with optional text |
| `icon_box(sl, l, t, w, h, icon_text, title, desc, icon_color, icon_size)` | Card with icon circle + title + description |
| `accent_bar(sl, l, t, w, color, thickness)` | Thin accent bar for visual hierarchy |
| `badge(sl, l, t, text, color, fc, fs)` | Pill-shaped badge/tag |
| `connector(sl, l1, t1, l2, t2, color, width)` | Line connector between points |
| `hline(sl, l, t, w, color)` | Horizontal line |
| `stbl(sl, data, l, t, w, h, cw)` | Styled table (green header, alternating rows) |
| `bullets(sl, l, t, w, h, items, fs, color, bullet_color, spacing)` | Bulleted list — items = list of strings or [(text, size, bold, color), ...] |
| `img(sl, path, l, t, w, h)` | Add image — provide w or h (or both); aspect ratio preserved if only one given |
| `new_deck(template_path)` | Load template with sample slides removed — use for all new decks |
| `set_title(sl, title_text)` | Set slide title + **remove** unused placeholders (idx 1, 10) from XML |

### Font & Color Palette
**Font:** All helpers automatically apply `FONT = "Lato"` (brand font) via `sf()`. No need to set font manually.

**Colors:** `G` (brand green), `DG` (dark green), `W` (white), `BK` (near black), `MG` (gray), `LG` (light gray), `BLU` (blue), `ORG` (orange), `PRP` (purple), `RED` (red), `TEAL` (teal), `DRED` (dark red)

### Design Approach
Use helpers freely to compose visually rich slides. There are no fixed recipes — design each slide to fit its content. Mix and match shapes creatively:
- **Cards with icon circles** for features, benefits, pain points
- **Color-coded boxes with accent bars** for grouped content
- **Numbered circles + arrows** for flows and sequences
- **Outlined boxes** for callouts, quotes, highlighted sections
- **Badges** for labels, categories, status indicators
- **Connectors and arrows** for architecture and data flow diagrams
- **Tables** for structured comparisons

### Key Constraints
- **Slide dimensions:** 13.33" x 7.50" — keep ALL content within bounds with comfortable margins
- **Font sizes:** Titles 28-36pt, headings 13-14pt, body 11-12pt, captions 10pt. Never below 10pt.
- **Max 6 items per slide.** Keep text concise — slides support the speaker.
- **Always use `new_deck(template_path)` for new decks** — never bare `Presentation()`. This loads the template with sample slides removed.
- **NEVER delete slides manually** — no `del prs.slides._sldIdLst[...]`, no slide removal. Rebuild from scratch with `new_deck()` instead.
- **Respect slide count limits** strictly.
- **python-pptx must be installed** — `pip3 install --break-system-packages python-pptx`

## Step 5: Editing Existing Decks

### CRITICAL: Never Delete Slides
**NEVER use `del prs.slides._sldIdLst[...]` or any slide deletion method** — this corrupts the PPTX internal XML relationships and produces files that PowerPoint reports as "not repairable". python-pptx has NO safe slide deletion API.

**Safe editing approaches (choose one):**
- **Replace/reorder slides:** Rebuild the ENTIRE deck from scratch using the template. Read the existing deck first to extract content, then generate a fresh deck.
- **Minor text edits:** Edit in-place via `prs.slides[idx]` shapes — modify text, colors, positions on existing slides.
- **Add slides:** Append with `prs.slides.add_slide(prs.slide_layouts[1])`.

**When user says "edit slide 3" or "remove slide 5" or "replace slides 2-4":** Always rebuild from scratch. Never attempt to delete or reorder slides in-place.

### Read Existing Deck
```python
prs = Presentation("<path>")
for i, slide in enumerate(prs.slides):
    print(f"--- Slide {i+1}: {slide.slide_layout.name} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                if para.text.strip(): print(f"  {para.text}")
        if shape.has_table:
            for row in shape.table.rows:
                print("  | " + " | ".join(cell.text for cell in row.cells) + " |")
```

## Step 6: Output

- **Default path:** User's Downloads folder
- **Filename:** `OCTAVE_<topic>_<date>.pptx`
- Report slide count and ask if user wants adjustments.
- If PermissionError, save with `_v2.pptx` suffix.
