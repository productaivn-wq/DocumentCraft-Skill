# DocumentCraft

**Two roles in one skill:**
1. **Engine** — Markdown → PDF/DOCX with parallel multi-theme rendering.
2. **Playbook** — generic, project-agnostic patterns for shipping operator-grade structured documents.

> The Playbook is parameterised — every pattern uses `{placeholder}` slots so you can drop the skill into any new project (strategy report, GTM, board memo, RFC, due-diligence, market scan, …) and only fill in what applies. Concrete examples sit in `> Example:` callouts you can ignore.

## Quick Start

```bash
# Install
pip install -r requirements.txt
playwright install chromium

# All 6 outputs (3 PDF + 3 DOCX) from a markdown file
python core/scripts/craft.py all "path/to/report.md" --output-dir "./outputs"

# Single theme + format
python core/scripts/craft.py pdf  "report.md" --theme darkmode
python core/scripts/craft.py docx "report.md" --theme vibrant
```

## Available Themes

**PDF** (CSS via Playwright): `minimal` · `corporate` · `darkmode`
**DOCX** (Word Styles via python-docx): `classic` · `minimalist` · `vibrant`

## The Playbook (read before writing the markdown)

Codified in [`docs/SKILL.md`](docs/SKILL.md). Each pattern: **NAME · WHEN · TEMPLATE · optional Example.**

| § | Pattern | Use when |
|---|---|---|
| 2.1 | Narrative Arc | Deliverable > 5 pages |
| 2.2 | MECE Structural Axes | Document makes population claims |
| 2.3 | Top-N + Companion Split | A list grows past ~10 rows |
| 2.4 | Inline `[n]` Citation System | Reader might challenge a number |
| 2.5 | Cover-Page Dedup | Always |
| 2.6 | Bullet-vs-Prose | Paragraph has 3+ enumerable items |
| 2.7 | Page-Break + Line-Break Engineering | Always |
| 2.8 | Pre-Launch Numbering Discipline | Plan/forecast docs without actuals |
| 2.9 | Versioning + Archive Workflow | 3+ revisions expected |
| 2.10 | Brand / Naming Rebrand Workflow | Project rename mid-flight |
| 2.11 | Translation / Localisation Workflow | Same source, multiple languages |
| 2.12 | Iterative Review Loop | Always |
| 2.13 | Independent Coherence-Review Agent | Before external share |
| 2.14 | Parallel Agent Pattern | Multiple independent deliverables |
| 2.15 | Pre-Publish Checklist | Before any external share |

**Part 3** of `SKILL.md` is a YAML slot fill-in template — copy it into a new project's planning doc and fill `{slots}` to wire the skill up in one paste.

## Files

| File | Purpose |
|---|---|
| `docs/SKILL.md` | Engine reference + full project-agnostic playbook + slot fill-in template |
| `core/scripts/craft.py` | CLI entry point |
| `core/scripts/generate_pdf.py` | PDF generation (Playwright) |
| `core/scripts/generate_docx.py` | DOCX generation (python-docx) |
| `core/scripts/lib/md_parser.py` | Markdown → HTML |
| `core/scripts/lib/themes_pdf.py` | CSS themes |
| `core/scripts/lib/themes_docx.py` | Word Style themes |

## Version

**1.2.0** (2026-05-07) — Playbook refactored to be project-agnostic. See `SKILL.md` changelog.
