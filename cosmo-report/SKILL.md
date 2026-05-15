---
name: cosmo-report
description: >
  Generate a full Amazon COSMO × Rufus SP Prompts optimization report for a seller's ASIN(s).
  Use this skill whenever a seller uploads their SP Prompts xlsx data and asks for analysis,
  a report, COSMO scoring, Rufus optimization, listing improvement suggestions, or ad action plans.
  Also trigger when the user says things like "帮我分析广告报告", "做一份COSMO报告", "listing优化建议",
  "Rufus广告优化", "SP Prompts分析", or any request to review Amazon advertising Prompt data.
  This skill reads the xlsx input, classifies each Prompt by COSMO intent level (L1/L2/L3),
  scores Rufus-friendliness, detects product mismatches, and outputs a polished HTML report
  with listing rewrite examples and a prioritized ad action plan — all in plain language.
---

# COSMO × Rufus SP Prompts Report Skill

## What this skill does

Produces a complete, seller-ready COSMO optimization report as a **single HTML file** that can be downloaded and opened in any browser. The report includes:

1. **Health Score** — Rufus-friendliness score (0–100) per product line
2. **COSMO Intent Analysis** — classify each Prompt into L1/L2/L3 with full sales data
3. **Mismatch Detection** — find Prompts where Rufus is recommending a competitor or wrong product
4. **Listing Optimization** — partial before/after fixes + complete listing reference templates
5. **Ad Action Plan** — prioritized steps (🔴 urgent / 🟡 high / 🟢 medium) with exact console paths
6. **Plain-language Seller Guide** — step-by-step instructions for non-technical operators
7. **V1→V2 Comparison** — (returning sellers) show progress between reporting periods
8. **Periodic Reports Value** — demonstrate why regular diagnosis matters, invite next submission

---

## Workflow

> **Order is fixed**: Step 0 (Listing verification) → Step 1 (Read xlsx) → Step 2 (COSMO classification) → ... → Step 4 (HTML generation). See "CRITICAL: Listing Verification Rule" section below for the Step 0 / 0.5 details. Skipping Step 0 = report quality collapses.

### Step 1 — Read Input Data

The user will provide one or more of:
- SP Prompts xlsx files (exported from Amazon Ads console → Sponsored Products → Prompts)
- ASIN(s) or product line names for context
- Brand name

**Read the xlsx** using openpyxl. Look for these columns (order may vary):
```
Prompt Detail | Sample Response | Ad Name | ASIN | SKU |
Impressions | Clicks | CTR | Cost | CPC | Purchases | Sales | ACOS
```

**openpyxl row iteration** — iterate row by row to avoid MergedCell errors:
```python
import openpyxl
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
# Find header row, then iterate data rows
```

If columns are missing, infer from context. The `Sample Response` and `ASIN` columns may need to be filled manually by the seller (note this in the report).

**All dates in the report must use Chinese format** (e.g., `2026年3月10日`, `3月10日–4月9日`). Never write English month names (Mar, Apr, etc.) in any visible text.

### Step 2 — COSMO Intent Classification

For each Prompt row, classify its COSMO relation type and intent level. Read `references/cosmo_framework.md` for the full 15-relation taxonomy. Quick reference:

| Level | Relation Types | Prompt Pattern | Conversion |
|-------|---------------|----------------|------------|
| **L1 高典型性** | capable_of, used_for_func, used_to, xWant | "Does [brand] have [product] with [specific feature]?" | ★★★★★ |
| **L2 中典型性** | used_for_eve, used_for_aud, used_on, used_in_loc, used_with, used_by, used_as, xIs_a | "What [brand] product works for [scenario/audience]?" | ★★★☆☆ |
| **L3 低典型性** | is_a, xInterested_in | "Why choose [brand]?" / "[Brand] [product type]" | ★☆☆☆☆ |

**Mismatch detection**: If the `Sample Response` describes product features that don't match the `Ad Name` / ASIN being advertised → flag as ❌ Product Mismatch.

**Cross-model substitution**: Rufus responding to Product A's prompts using features of Product B in the same brand. Root cause: Product A listing lacks specific specs → COSMO borrows from the richer listing. Fix: add specs to Product A's listing directly.

**L3 rule**: Any Prompt classified as L3 should be flagged for immediate closure once CPC billing begins.

### Step 2.5 — Returning Seller: V1→V2 Comparison

If the seller has provided data from a **previous reporting period** (v1), generate a comparison section:

1. Calculate score change per product (v2 score – v1 score)
2. Identify the specific listing changes made between periods and which COSMO mechanism explains the improvement
3. Show a concrete example of the COSMO fix working (e.g., "U8PRO Bullet 3 now uses `capable of meeting ADA Standard 117.1 – 17.375-inch` → iX7-MT displaced from Rufus response within 14 days")
4. Use a green/teal accent for improvements, red for regressions
5. Include a "V1→V2 对比" banner card near the top of the report (after stat row, before health scores)

This section demonstrates the value of periodic reporting to the seller.

### Step 3 — Scoring

Compute a **Rufus Friendliness Score (0–100)** per product line:

| Dimension | Weight | How to Score |
|-----------|--------|--------------|
| capable_of 功能覆盖度 | 40% | % of L1 Prompts with specific numbers/specs in Sample Response (0–100) |
| Typicality 质量 | 30% | Average quality of Sample Response descriptions (vague=30, specific=80, with numbers=100) |
| 前80字符意图密度 | 15% | Do Ad Name titles contain key feature words in first 80 chars? |
| L2/L3场景覆盖 | 10% | Diversity of scenario/audience Prompts |
| Semantic Gap Risk | -5% | Deduct for each confirmed mismatch |

**Rating guide**: 0–40 = 🔴 Critical, 41–60 = 🟡 Needs Work, 61–80 = 🟢 Good, 81–100 = ✨ Excellent

### Step 4 — Generate HTML Report

Produce a single self-contained HTML file. Read `references/report_design.md` for the exact visual style, color palette, and component patterns to use (dark theme, DM Mono + Syne + Noto Sans SC fonts, red accent #e63946).

The report must contain these sections in order:

```
1.  Hero header — brand name, data period (Chinese format), prompt count, report date
2.  Stat row — 4 key metrics (products analyzed, prompts, L1 count, critical count)
3.  V1→V2 Comparison Banner — (returning sellers only) progress between periods
4.  Health Scores — score rings per product line + key alert boxes
5.  Prior Recommendations Tracking — (v2+) did the v1 fixes get implemented?
6.  COSMO Intent Analysis Table — 11-column table with real sales data, per product
7.  Key Insights — explain WHY some prompts convert and others don't
8.  Listing Optimization — partial before/after fixes + complete listing templates
9.  Ad Action Plan — numbered action items with 🔴/🟡/🟢 priority badges
10. Plain-language Seller Guide — step-by-step for non-technical operators
11. Summary Table — one-page priority checklist
12. Periodic Reports Value — demonstrate value of regular diagnosis
13. Next Report CTA — invite seller to submit next data
14. Partnership CTA — Cosle WeChat invitation (ray0117_)
15. Footer — attribution, citation, disclaimer
```

### Step 5 — Listing Optimization: Two-Layer Approach

Generate listing optimization in **two layers** for each product with issues:

**Layer 1 — Partial Fix Cards** (always include)
Show the 1–2 most impactful before/after rewrites. Focus on the highest-priority COSMO fix:
- Missing `capable of` format → rewrite to include it
- Vague adjectives → replace with specific numbers
- ADA height as fraction → convert to decimal + add "capable of meeting ADA Standard 117.1"

**Layer 2 — Complete Listing Reference Template** (placed after each Layer 1 card)
Use `<details>/<summary>` collapsible pattern (no JavaScript). Contains:

1. **Title** — complete optimized title, < 200 chars, brand + model + core feature keywords
2. **Five Bullet Points** — COSMO triple format, one bullet per key `capable_of` relation
3. **Image Suggestions** — main image (⭐ highlighted) + 4 supporting images
4. **Q&A Recommendations** — map actual running Rufus Prompts to answer templates

**Listing Rewrite Rules:**

**Golden Rule**: Specific numbers + precise specs = high typicality. Vague adjectives = low typicality.

Apply the COSMO triple format for Bullet Points:
```
[FEATURE LABEL]: [product] capable of [specific function] – [exact spec with numbers] for [use case]
```

**❌ Low typicality (avoid)**:
- "Powerful flush system"
- "Comfortable seat height"
- "Easy to install"

**✅ High typicality (target)**:
- `ADA COMFORT HEIGHT: capable of meeting ADA Standard 117.1 – 17.375-inch (17-3/8") floor-to-seat height, suitable for senior and mobility-limited users`
- `1000G MAP CERTIFIED FLUSH: capable of removing 1000 grams of solid waste in a single flush – 1.6 GPF full / 1.1 GPF half, MaP Premium certified`
- `FOAM SHIELD SPLASHBACK PROTECTION: capable of forming an airtight foam barrier before each flush – blocks bowl splashback, reduces cleaning frequency`

Always include:
- Specific numbers (dimensions, weights, quantities, GPF, certifications)
- Comparative specs ("6× thinner", ADA standard numbers)
- Action verbs + outcome

**Missing specs**: Use `[X]` placeholder and add a ⚠️ warning: "此处需卖家确认实际规格后填写"

**CRITICAL constraint — never fabricate numbers**:
- Do not invent PSI ratings, temperature ranges, percentages, or dimensions not found in the actual listing
- If a spec is unknown, use `[X]` — never guess or estimate

### Step 6 — Ad Action Items

Generate action items in priority order. Each item must include:
- Priority badge: 🔴 Urgent / 🟡 High / 🟢 Medium / ⚪ Low
- Exact Amazon console navigation path
- The specific change to make (copy-paste ready)
- How to verify success (what to check and when)
- Estimated time to complete

**Universal rules for ad actions**:
- Any L3 Prompt → recommend PAUSED immediately
- Any confirmed mismatch → fix Listing first, then verify Sample Response changes within 7–14 days
- High CTR + 0 conversion L1 Prompts → recommend Listing fix before increasing bid
- Verified conversion Prompts → recommend +20–30% bid increase

---

## CRITICAL: Listing Verification Rule (HARD GATE — non-negotiable)

**No verification = no diagnosis. Zero tolerance for fabricated or guessed Listing content.**

This is the single most important rule in this skill. A single false "Listing 缺少 X" claim destroys the credibility of the entire report — sellers will conclude the AI is hallucinating. The UNICOLY v1 case (2026-05-14) and EPLO v1 case both validated this: when the listing already says X but the report claims X is missing, the seller spots it instantly and loses trust in every other diagnosis.

### Step 0 (before ANY diagnosis) — Establish ground truth on Listing content

Execute this verification ladder **in order**. Stop at the first method that succeeds:

| Method | When to use | Reliability |
|--------|-------------|-------------|
| **(A) User provided directly** | User pasted Title + Bullet Points in conversation | ⭐⭐⭐⭐⭐ Highest |
| **(B) WebFetch** | `https://www.amazon.com/dp/[ASIN]` | ⚠️ Often returns only HTML head/scripts on Amazon — verify content is substantive before trusting |
| **(C) WebSearch** | `[Brand] [Product] amazon [ASIN]` — extracts snippets and partial bullet text | ⭐⭐⭐ Usually enough for spec keywords |
| **(D) Ask the user** | All of (B) and (C) failed or returned incomplete data | ⭐⭐⭐⭐⭐ Use this — do not proceed without it |

**Mandatory rule for method (D)**: If WebFetch returns insufficient content AND WebSearch lacks the Bullet Points text, **stop and ask the user to paste the Title + 5 Bullet Points for each ASIN**. Do not infer Listing content from the Ad Name column alone — the Ad Name is the title, not the Bullets, and diagnoses about "Bullet N lacks X" require seeing the actual Bullets.

### Step 0.5 — Mandatory Listing Verification Table

Before writing the HTML report, output to the user a verification table for review:

```
| ASIN | What the Listing actually contains | What the report will diagnose as missing | Source |
|------|-----------------------------------|-----------------------------------------|--------|
| B0XXX | "cold-rolled steel plate (SPCC)", "wall-mounted, prevent tipping", "tempered glass" | 钢板厚度 mm、单层承重 lbs、玻璃厚度 mm | User-provided 2026-05-14 |
| ... | ... | ... | ... |
```

The user must be able to scan this table and immediately spot any false-missing claims. Only proceed to HTML generation after this checkpoint.

### Hard prohibitions

- ❌ Never write "Listing 没有提到 X" / "Listing does not mention X" if X actually appears in the Listing text — instead write "Listing 第 N 点已有 X 关键词但缺少具体数字/规格支撑"
- ❌ Never invent specific numbers (lbs, mm, PSI, hours, percentages, certification names). Unknown → `[X]` + ⚠️ "待卖家确认"
- ❌ Never fabricate certification standards (ASTM F2057, ANSI Z97.1, etc.) that the Listing doesn't claim — these can create legal exposure for the seller. Format: "建议补充 [认证名] 认证（待卖家确认是否已通过）"
- ❌ Never assume a Bullet's content from its label alone — read the actual Bullet text

### Cross-model substitution detection

Watch for Rufus responding to one ASIN's prompts by describing a **different product in the same brand's lineup**. This is distinct from cross-brand substitution and requires checking the Sample Response text against the specific ASIN being advertised. Always state which ASIN's content is being borrowed when applicable.

---

## Output

Save the report as `[BrandName]_COSMO_Rufus优化报告.html` in the appropriate output directory and share it with the user.

Tell the user: "下载后直接用浏览器（Chrome/Safari/Edge）打开即可查看完整报告。"

### Pre-delivery HTML Sanity Check (mandatory)

Inline-styled HTML with Chinese text is very easy to break — a missing `">` between `style="..."` and the Chinese text content collapses entire sections silently (the browser treats Chinese as part of the unclosed attribute). UNICOLY v1 had this exact bug in the seller-guide step cards: `<div style="font-size:11px;color:#7b8299;预计 5 分钟</div>` instead of `<div style="font-size:11px;color:#7b8299;">预计 5 分钟</div>`.

Before reporting the file as ready, run this grep to detect malformed style attributes:

```bash
grep -nE 'style="[^"]*;[^>]*[一-龥]' [report.html]
# Empty result = clean. Any matches = unclosed style attribute leaking into Chinese text — fix immediately.
```

Also visually verify by opening the file (or having the user open it) and checking that:
- All 4 sections of the Plain-language Seller Guide step cards render
- The Summary Checklist table is full-width, not pushed off-screen
- All `<details>` collapsible blocks open correctly

---

## Reference Files

- `references/cosmo_framework.md` — Full 15-relation COSMO taxonomy with examples and typicality scoring
- `references/report_design.md` — HTML/CSS design system for the report (dark theme, components, color codes)

Read these when you need detail on classification rules or when writing the HTML output.
