---
name: DocumentCraft
description: "Markdown-to-PDF/DOCX rendering engine plus a generic, project-agnostic playbook for shipping operator-grade structured documents. Wraps python-docx and Playwright; teaches narrative arcs, MECE axes, citation systems, page-break engineering, companion-file split, brand rebrand, translation, and review loops."
version: 1.3.0
status: active
updated: 2026-05-08
---

# DocumentCraft

**Two roles in one skill:**
1. **Engine** — Markdown → PDF/DOCX with parallel multi-theme rendering.
2. **Playbook** — generic, parameterised rules for *what to put inside* any structured document (strategy, pre-feasibility, GTM, board memo, technical RFC, due-diligence, market scan, …).

> The Playbook is **project-agnostic**. Every pattern is described as a template with `{placeholder}` slots; concrete examples sit in `> Example:` callouts you can ignore if irrelevant. Drop the skill into any new project and only fill in the slots that apply.

---

## Part 1 — Engine

### Process
1. **Parse** — Markdown → structural HTML via the `markdown` library.
2. **Theme** — Inject visual theme (CSS for PDF, Word Styles for DOCX).
3. **Render** — Generate via Playwright (PDF) or python-docx (DOCX).
4. **Parallelize** — Optional concurrent multi-theme rendering.

### Capabilities

| Capability | Status | Description |
|---|---|---|
| **PDF Generation** | ✅ Active | Markdown → HTML → PDF via headless Chromium |
| **DOCX Generation** | ✅ Active | Markdown → HTML → DOCX via python-docx + htmldocx |
| **YAML Frontmatter**| ✅ Active | Parses meta tags for cover pages & document settings |
| **Auto Cover Page** | ✅ Active | Synthesizes cover page if `title` is in frontmatter |
| **Table of Contents**| ✅ Active | Auto-generates TOC if `toc: true` in frontmatter |
| **Pagination**      | ✅ Active | Bottom margin page numbering for PDF/DOCX |
| **Syntax Highlight**| ✅ Active | Code block syntax highlighting via codehilite |
| **Custom Brand Color**| ✅ Active | Dynamic HEX override via `--brand-color` |
| **Multi-Theme** | ✅ Active | 3 built-in themes per format |
| **Parallel Rendering** | ✅ Active | Concurrent multi-version output |
| **Table Borders** | ✅ Active | Automatic 'Table Grid' style for DOCX |
| **Font Consistency** | ✅ Active | Forces base font across Normal, List, Tables, Heading 1–4 |

### Themes

**PDF (CSS):** `minimal` · `corporate` · `darkmode`
**DOCX (Word Styles):** `classic` · `minimalist` · `vibrant`

### Usage

### Usage

```bash
python core/scripts/craft.py pdf  "report.md" --theme darkmode --output-dir ./outputs --brand-color "#FF5733"
python core/scripts/craft.py docx "report.md" --theme vibrant
python core/scripts/craft.py all  "report.md"           # all themes both formats, parallel
```

### Prerequisites
- Python 3.10+ · `pip install -r requirements.txt` · `playwright install chromium`

### Key files
| File | Purpose |
|---|---|
| `core/scripts/craft.py` | CLI entry point |
| `core/scripts/generate_pdf.py` | PDF engine (Playwright) |
| `core/scripts/generate_docx.py` | DOCX engine (python-docx) |
| `core/scripts/lib/md_parser.py` | Markdown → HTML |
| `core/scripts/lib/themes_pdf.py` | CSS theme definitions |
| `core/scripts/lib/themes_docx.py` | Word Style definitions |

---

## Part 2 — Playbook (project-agnostic patterns)

Every pattern below has the same shape:
> **NAME** · **WHEN** · **TEMPLATE** · *Optional* `> Example:` from real engagements.

Pick the patterns that apply, fill the `{slots}`, ignore the rest.

---

### 2.1 Narrative Arc

**WHEN.** Whenever the deliverable is more than 5 pages. Encyclopedic dumps don't get read; arcs do.

**TEMPLATE.** Pick a sequence of 4–9 parts. Each part starts on its own page, ends with a one-line pointer to a companion file (if one exists).

Two reusable arc templates:

| Arc length | When to use | Generic shape |
|---|---|---|
| **Slim 4-part** | Exec / one-meeting consumption (~10–15 pages) | (1) Who · (2) Their journey · (3) What the market offers · (4) Where the gap is |
| **Full 8-part** | Audience needs the operating math too (~20+ pages) | (1) Why now · (2) Where we play · (3) What we sell · (4) How we win · (5) How we go to market · (6) What it earns · (7) What can break it · (8) What's next |

**Other arc shapes** that fit the same template:
- Investment memo: thesis · market · team · product · economics · risks · ask
- Technical RFC: problem · constraints · options considered · proposal · trade-offs · rollout · open questions
- Due-diligence: business · market · financials · team · legal · risks · recommendation
- Post-mortem: timeline · root cause · contributing factors · what went well · what to fix · action items

> Example: AI E-Learning Hub VN used the slim 4-part for its main pre-feasibility report (TA + reasons / customer journey / market offer / market gap), with the full 8-part content lifted into a separate Operating Plan companion.

---

### 2.2 MECE Structural Axes

**WHEN.** Whenever the report makes claims about a population (customers, competitors, products, risks) and the reader needs to trust nothing was missed and nothing double-counted.

**TEMPLATE.** Declare 2–3 axes in §0. Each axis has N **mutually exclusive** cells that **collectively exhaust** the population. Use the same labels everywhere — main report and every companion.

```
Axis 1: {dimension_name}     → {N₁ cells, disjoint, complete}
Axis 2: {dimension_name}     → {N₂ cells, disjoint, complete}
Axis 3: {dimension_name}     → {N₃ cells, disjoint, complete}
```

Common axis dimensions:
- **Buyer** (role × age, role × geography, segment × use-case)
- **Offer** (price tier, SKU, plan)
- **Competitor** (archetype, business model, distribution channel)
- **Risk** (likelihood × impact, type × time-horizon)
- **Initiative** (now / next / later, must-have / should-have / nice-to-have)

> Example: AI E-Learning Hub used (1) TA = buyer role × age (3 cells), (2) SKU = price point (4 cells), (3) Archetype = competitor type (10 cells A1–A10). Each ranked competitor in the workbook traces to exactly one archetype label in the report.

---

### 2.3 Top-N + Companion Split

**WHEN.** A list grows past ~10 rows OR contains data that needs ongoing maintenance.

**TEMPLATE.**
- **Main report** carries top-N + counts + 1-line summary per row.
- **Companion workbook** (`.xlsx` + `.docx` + `.pdf` exports) holds the full list with live formulas.
- Each part of the main report ends with: `Full {thing} in {Companion}.xlsx / sheet {Sheet}`.

Common companion types:
- `Operating_Plan` — sizing, ARPU, milestones, risks, roadmap
- `Competitors_List` — ranked list + scoring methodology + per-axis matrix
- `Sources_and_Links` — hyperlinked URLs by category + Index sheet
- `Detailed_Tables` — every reference table the main report references
- `Domain_Tracks` — week-by-week deliverables / per-segment plans

> Example: AI E-Learning Hub VN ships 5 companion workbooks; main report is 12 pages; sum of companions is ~80 pages of detail kept out of the main flow.

---

### 2.4 Inline `[n]` Citation System

**WHEN.** Any document where a reader might challenge a number or claim.

**TEMPLATE.**
- Every numerical claim and every named source carries an inline `[n]` marker.
- Render `[n]` as small-bold accent-colour text after the claim:
  > "{claim with number} **[n]**"
- The full list resolves in:
  - Appendix A of the main document — table of (n / source title / URL / used-in section)
  - A canonical `References_Master.csv` (one row per ref)

**CSV schema:**
```
ref_no,claim_or_number,source_title,source_url,source_category,used_in_section
```

When a primary source URL can't be obtained, mark `NEEDS_RESEARCH` and provide secondary corroborating URLs.

> Example: 69 inline references in the AI E-Learning Hub report; multi-ref like `[14, 15, 16]` for triangulated claims.

---

### 2.5 Cover-Page Dedup

**WHEN.** Always.

**TEMPLATE.** Cover = exactly 3 lines. Don't repeat the brand.

```
{BRAND_FULL_NAME}                    ← brand line, 22pt bold
{Document type — version}            ← report-type + version, 14pt
{One-line purpose / arc preview}     ← scannable subtitle, 11pt italic
```

Below the 3-line cover, an "at-a-glance" table with 5–8 rows: Product · Thesis · KPI · TAs/segments · Pricing · Distribution · Status · Prepared for.

---

### 2.6 Bullet-vs-Prose Rule

**WHEN.** A paragraph contains 3+ enumerable items.

**TEMPLATE.** Break into a bold lead-in + N separate bullets, each with its own bold sub-lead.

```
**{Section header.}**
• **{1. Reason name.}** — {prose evidence}.
• **{2. Reason name.}** — {prose evidence}.
• **{3. Reason name.}** — {prose evidence}.
```

The lead phrase carries the scan; the prose carries the proof. Never bury 5 enumerated reasons inside one paragraph.

---

### 2.7 Page-Break + Line-Break Engineering

**WHEN.** Always — defaults in python-docx and docx-js leave headings orphaned and tables split mid-row.

**TEMPLATE.** Apply globally in theme files OR per-element.

| Problem | python-docx fix | docx-js fix | CSS (PDF) fix |
|---|---|---|---|
| Heading orphaned at page bottom | `paragraph_format.keep_with_next = True` on H1/H2/H3 | `keepNext: true` | `h1, h2, h3 { break-after: avoid; }` |
| Heading wraps mid-line | `paragraph_format.keep_together = True` | `keepLines: true` | `h1, h2, h3 { break-inside: avoid; }` |
| Section starts mid-page | `paragraph_format.page_break_before = True` on H1 | `pageBreakBefore: true` | `h1 { break-before: page; }` |
| Table row splits mid-cell | `row.cant_split = True` on every TableRow | `cantSplit: true` | `tr { break-inside: avoid; }` |
| Header row missing after page break | `tr.tblHeader = True` on the first row | `tableHeader: true` | `thead { display: table-header-group; }` |
| Word breaks awkwardly in narrow column | Widen column or pick shorter label | Same | Same |

**Bake into theme files** so every project inherits these automatically — `themes_docx.py` Word styles include `keep_with_next` + `page_break_before` on Heading 1; `themes_pdf.py` CSS includes the four `break-*: avoid` rules.

---

### 2.8 Pre-Launch Numbering Discipline

**WHEN.** Plan/forecast documents shared before the project / product / quarter has actuals.

**TEMPLATE.**
- Mark the cover and every numbered table: **"Plan, not actuals — as of {date}."**
- Keep "Actual" columns literally blank (`—`) by design.
- Footnote: *"All figures are forward-looking plan; revisit at {trigger event} for actuals."*

Avoid implying past performance you don't have. A reader who only skims the milestones table should immediately see this is forecast.

---

### 2.9 Versioning + Archive Workflow

**WHEN.** Any project that will go through 3+ revisions.

**TEMPLATE.**
```
{project_root}/
├── (current canonical files: {Brand}_{Module}.{ext})
├── _archive_{YYYY-MM-DD}/    ← every superseded version + obsolete-name files
├── README.md                  ← index / file map / edit workflow
└── CLEANUP_*.bat              ← one-click deleter
```

The cleanup script must:
1. List the candidate files.
2. **Verify each is also in `_archive_*/`** before deleting.
3. **Refuse** if any safety copy is missing.
4. Self-delete after success.

Pattern works on Windows (.bat wrapping PowerShell), macOS (.command wrapping bash), Linux (.sh).

---

### 2.10 Brand / Naming Rebrand Workflow

**WHEN.** Project rename mid-flight; product rename; team-merger renaming; deliverable handoff to a different sponsor.

**TEMPLATE.**
1. **Update source code** — global cell-walk replace across all `.js` / `.py` / `.md` source files.
2. **Walk every cell of every `.xlsx`** — openpyxl iterate-and-replace preserves styling.
3. **Rename outputs** — `{old}_*` → `{new}_*` for every deliverable.
4. **Re-export** every `.xlsx` to `.docx` + `.pdf` via LibreOffice headless.
5. **Verify zero residue:** `pdftotext output.pdf - | grep -ic '{old_brand}'` must equal `0` for every PDF.
6. **Update README** to record the rename + the archive location.

Watch for: cached `node_modules` that don't reload edits, `__pycache__` Python caches, hyperlinks pointing at old filenames inside cells.

---

### 2.11 Translation / Localisation Workflow

**WHEN.** Same source, multiple language outputs.

**TEMPLATE.**

**Keep verbatim** (do NOT translate):
- Inline `[n]` reference markers
- Numbers, prices, percentages, dates
- Brand and file names
- Technical acronyms widely used in target-market business (KPI, ARPU, B2B2C, CJM, ERRC, MECE, CAC, LTV, SKU, …)
- Strategy framework terms (Right-to-Win, Where-to-Play, Red/Blue Ocean, Strategy Canvas — recognised English MBA terms in most markets)
- Tool / channel / platform names (LinkedIn, Discord, ChatGPT, …)
- Domain-specific identifiers (`A1`–`A10` archetype codes, SKU IDs, …)

**Translate:**
- All prose, callouts, bullet text, table cell labels, descriptions, section titles.

**Voice rules:**
- Match the source register (operator-grade / academic / casual). Don't slide into bureaucratic.
- Avoid literal calques — paraphrase when needed.
- Native diacritics / scripts — don't strip.
- For a CJM table, keep target-language search queries in the buyer's voice (e.g. Vietnamese "Khóa học AI cho HR" stays Vietnamese even in the English original).

Output filename pattern: `{Brand}_{Module}_{LANG}.docx` (e.g., `*_VI.docx`, `*_JA.docx`).

---

### 2.12 Iterative Review Loop

**WHEN.** Always — never ship the first render.

**TEMPLATE.**
```
1. Render PDF.
2. pdftoppm -jpeg -r 95 -f {page} -l {page} report.pdf preview
3. Inspect preview-NN.jpg with vision-capable tool.
4. Find: orphaned heading? split row? word break? bad spacing? typo?
5. Fix in source.
6. Re-render. Goto 2.
```

Spot-check minimum: page 1 (cover), every page where a new Part starts, any page with a tall table, last page (appendix).

---

### 2.13 Independent Coherence-Review Agent

**WHEN.** Before shipping anything that will be read by external stakeholders or board-level audiences.

**TEMPLATE.** Spawn a fresh agent with no prior context. Give it the final PDF + the references CSV + a checklist:

1. **Scope match** — does the document cover only the agreed parts?
2. **Inline references** — spot-check 10–15 `[n]` markers; do they cite real claims and resolve in the master CSV?
3. **Numbering consistency** — same source → same `[n]`; no orphan markers.
4. **Companion pointers** — every "see Companion X" actually exists?
5. **Flow / story arc** — coherent narrative or stitched tables?
6. **MECE check** — do the declared axes partition the population without overlap?
7. **Numerical accuracy** — spot-check 5 key numbers against the source URLs.
8. **Tone & concision** — operator-grade or wordy?
9. **Cross-companion traceability** — every pointer accurate?
10. **Critical issues** — list up to 3 concrete fixes.

Output verdict: **SHIP / SHIP-WITH-FIXES / REJECT**. Apply fixes; re-verify.

---

### 2.14 Parallel Agent Pattern

**WHEN.** Building multiple independent deliverables (e.g., main report + N companion workbooks).

**TEMPLATE.** Spawn agents concurrently rather than sequentially. Each agent:
- Receives a self-contained prompt with all required content embedded.
- Writes to a known output path.
- Re-exports source format to derived formats (e.g., `.xlsx` → `.docx` + `.pdf`).
- Copies to the workspace folder.
- Returns a summary (file sizes + tricky-decision notes).

Typical fan-out: 1 agent per companion file = N parallel jobs.

---

### 2.15 Pre-Publish Checklist

**WHEN.** Before any external share.

```
[ ] Cover dedup rule observed (3 lines, no brand-name repetition)
[ ] Every Part starts on a fresh page
[ ] No table row splits mid-cell across pages
[ ] No headings orphaned at page bottom
[ ] Every numerical claim has an [n] reference
[ ] Every [n] resolves in the references appendix / master CSV
[ ] Every "see Companion X" pointer names a workbook + sheet that exist
[ ] "Plan, not actuals" labels in place if pre-launch
[ ] Page header / footer correct (brand, version, "Page X of Y")
[ ] All companion files reflect same brand, same numbers, same axis labels
[ ] pdftotext output.pdf - | grep -ic '{old_brand_to_remove}' returns 0
[ ] README updated to reflect current state
[ ] Old versioned files moved to _archive_YYYY-MM-DD/
```

---

## Part 3 — Slot fill-in template (copy into a new project)

When starting a new project, copy this block into the project's planning doc and fill in the `{slots}`. The skill then has everything it needs to produce ship-grade deliverables.

```yaml
project:
  brand: "{Brand Name}"
  brand_short: "{BRAND_SHORT}"      # for headers, e.g. "ACME VN"
  filename_prefix: "{Brand_Module}" # for output filenames
  language: "{en | vi | ja | ...}"
  prepared_for: "{Sponsor name}"
  date: "{YYYY-MM}"

document:
  type: "{Pre-feasibility | GTM | Investment memo | RFC | DD | Post-mortem | …}"
  version: "v{N}"
  arc:
    template: "slim-4-part | full-8-part | custom"
    parts:
      - "{Part 1 title}"
      - "{Part 2 title}"
      - …

axes:
  - name: "{Axis 1 name, e.g. Buyer — role × age}"
    cells: ["{Cell 1}", "{Cell 2}", …]
  - name: "{Axis 2 name, e.g. Offer — price tier}"
    cells: ["{Cell 1}", "{Cell 2}", …]
  - name: "{Axis 3 name, e.g. Competitor — archetype}"
    cells: ["{A1 — Label}", "{A2 — Label}", …]

companions:
  - name: "{Companion_Name}"
    formats: [xlsx, docx, pdf]
    holds: "{what's inside}"
  - …

references:
  csv: "{Brand}_References_Master.csv"
  count_target: "{rough N}"

theme:
  pdf: "minimal | corporate | darkmode"
  docx: "classic | minimalist | vibrant"
  brand_colour_hex: "{1F4E78}"
  alt_row_colour_hex: "{EAF2FA}"

review:
  coherence_agent: "yes | no"
  pre_publish_checklist: "required"

archive:
  folder: "_archive_{YYYY-MM-DD}/"
  cleanup_script: "CLEANUP_old_branded_files.bat"
```

---

## Architecture

```
                    ┌─────────────┐
                    │  craft.py   │  (CLI entry point)
                    │  (argparse) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼                         ▼
     ┌────────────────┐       ┌──────────────────┐
     │ generate_pdf.py│       │ generate_docx.py │
     │  (Playwright)  │       │  (python-docx)   │
     └───────┬────────┘       └────────┬─────────┘
             │                         │
     ┌───────┴────────┐       ┌────────┴─────────┐
     │ themes_pdf.py  │       │ themes_docx.py   │
     │ (CSS strings)  │       │ (Word Styles)    │
     └───────┬────────┘       └────────┬─────────┘
             │                         │
             └────────────┬────────────┘
                          ▼
                  ┌───────────────┐
                  │ md_parser.py  │
                  │ (markdown lib)│
                  └───────────────┘
```

---

## Traceability Integration

Final outputs (PDF/DOCX) and the `References_Master.csv` are designed to be ingested by the **TraceabilityGraph**. 
- The CSV allows the graph to establish `CITES` edges between codebase nodes and specific document claims.
- The compiled documents act as high-level Artifact nodes.

---
## Roadmap (suggested next-build extensions)

| Idea | Why | How |
|---|---|---|
| `[n]` resolver pass | Auto-link inline citations to the references table | Markdown extension that rewrites `[n]` → numbered hyperlinks; build References table from a YAML front-matter source |
| Companion orchestrator | Build main + N companions in one shot | New `craft.py bundle` command taking a manifest of `.md` + `.xlsx` files |
| Page-break theme defaults | Apply §2.7 rules globally | Update `themes_docx.py` Word styles to include `keep_with_next` + `page_break_before` on Heading 1; emit `cant_split` on every table row; same for `themes_pdf.py` CSS |
| Pre-publish lint | Catch playbook violations before render | `craft.py lint report.md` runs §2.15 checklist against the source markdown |
| Translation pipeline | Same source, multiple language outputs | `craft.py translate report.md --to vi --keep-acronyms KPI,ARPU,…` |
| Coherence-review preset | Bake §2.13 audit into a reusable script | `craft.py review report.pdf --master-refs References_Master.csv` |
| Project bootstrapper | Spin up the slot-fill template + folder skeleton | `craft.py init {project} --template strategy-report` writes the full structure |

---

## Changelog

- **1.3.0** (2026-05-08) — Dynamic Engine upgrade! Added YAML frontmatter parsing, automatic Cover Page generation (via `title`/`subtitle`/`brand`), dynamic `--brand-color` CLI overrides, auto-generated Table of Contents (`toc: true`), global pagination/page numbers, and syntax highlighting for code blocks.
- **1.2.0** (2026-05-07) — Refactored the Playbook to be **project-agnostic**. Every pattern now uses `{slot}` syntax with optional `> Example:` callouts. Added Part 3 (slot fill-in YAML template) so any new project can be wired up in one paste. Original engagement-specific examples preserved as illustrations only.
- **1.1.0** (2026-05-07) — Added Part 2 (Playbook): narrative arc, MECE axes, top-N + companion pattern, inline citation system, cover dedup, bullet-vs-prose rule, page/line-break engineering, pre-launch numbering, versioning/archive, brand rebrand, translation workflow, iterative review loop, coherence-review agent, parallel agent pattern, pre-publish checklist, roadmap.
- **1.0.0** — Initial engine release (PDF + DOCX generation, 3 themes per format, parallel rendering).
