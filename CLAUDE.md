# Medical Guidelines — SFAR/SRLF/HAS Fiche Project

## What this project is

A website + PDF "fiche" system that summarizes French anesthesia/critical-care
learned-society guidelines (SFAR, SRLF, HAS, GIHP, CNGOF, GFHT, SFMU, etc.) so
clinicians can rely on short, sourced, visually-clear summary sheets instead of
reading full guideline PDFs (often 50-150+ pages).

- Published website (single-page app, published via the Artifact tool):
  `https://claude.ai/code/artifact/63029698-e65d-4ebf-ab9a-9b93d29f2b26`
  (republished 2026-09-08 — the previous URL, 69853cb5-182e-461b-8642-ff69c37ddd16,
  stopped resolving; this one also declares the `db` capability the site's
  report/admin-decision feature needs — see `rules` in the publish call: only
  `admin_check` and `decisions` writes are admin-gated, `reports` stays default
  so any viewer can submit an error report).
- Delivered PDFs also live in `/Users/macbook/Downloads/claude/RFE_SFAR_2026/`
  on the user's machine (this repo's `output/` folder is the git-tracked copy).
- **61 of 160 SFAR library items are git-tracked (this repo's `site/app.js`
  `FICHE_HREF_MATCH`) as of 2026-09-11.** Track progress via that object's keys vs.
  `build/library_final.json` (the full 160-item index). Fiche 61
  (`urgences_transfusionnelles_obstetricales` — EFS table ronde 2000-2001, "Le
  traitement des urgences transfusionnelles obstétricales"; library index
  itself mislabels this item "Hémorragies du post-partum immédiat" / "2014",
  a divergence disclosed inside the fiche, not resolved) has its full 4-file
  site integration done (build/extract_content.py, build/assemble.py,
  site/template.html, site/app.js — assembled site/rfe_garde.html contains
  `id="content-urgences_transfusionnelles_obstetricales"`) and its PDF is in
  `output/`, but per an explicit instruction this run, it was **NOT published**
  to the live Artifact URL below — step 11 (publish safety gate) was
  deliberately skipped, pending the human decision on the KNOWN DRIFT issue
  below. `site/rfe_garde.html` in this git repo is therefore currently AHEAD
  of the live Artifact by this one fiche in addition to already being behind
  it by the 9 KNOWN DRIFT fiches — do not publish either direction without
  reconciling both facts first.
- **⚠ KNOWN DRIFT — git repo vs. live published Artifact (found 2026-09-11, unresolved,
  needs a human/session decision, do NOT silently fix by blindly publishing over it):**
  the live Artifact's `FICHE_HREF_MATCH` currently has **69** keys — **9 more than this
  git repo**, even after this session's addition. The 9 keys present live but absent
  from this repo (no fiche_*.py, no content_*.json, no git history at all) are:
  `aap_endoprotheses_coronaires`, `avc_precoce`, `douleur_postoperatoire`,
  `examens_preinterventionnels`, `infarctus_myocarde`, `monitorage_traumatise`,
  `recommandations_avk`, `tih_2002`, `traumatisme_cranien_grave_precoce`. This means an
  untracked session (not represented in `git log` on any branch checked) built and
  published up to 9 fiches directly to the Artifact without ever committing/pushing the
  underlying `fiche_*.py`/`content_*.json`/source files to this repo — the exact kind of
  loss this repo's step-13 "commit after every fiche" rule exists to prevent, except this
  time the *site* has the content and *git* is the one missing it (inverse of the
  earlier `/tmp` scratchpad incidents). **Before publishing anything to the Artifact
  URL above, always diff the live `FICHE_HREF_MATCH` against this repo's as part of the
  publish safety gate (step 11) — not just a grep for your own new marker** — a
  same-named different-content collision (see fiche 60, `voies_aeriennes_adulte`, this
  session: an untracked session had already built and published the SAME source document
  under the SAME key, independently arriving at the same 53-item/A-E grade tally) is
  exactly as real a risk as the marker-already-present case the existing step 11 already
  checks for. **This session did NOT publish** (the safety gate caught the
  `voies_aeriennes_adulte` collision) and did NOT attempt to reconstruct the other 8
  missing fiches (out of scope for one run) — a dedicated reconciliation session should
  either (a) pull each of the 9 live-only `content_*.json` blocks back into this repo
  (read the Artifact, extract each `id="content-<key>"` `<script>` block, reverse it into
  a committed file — no `fiche_*.py`/source PDF will exist for these unless also
  recovered), or (b) decide git is the source of truth going forward and accept the next
  publish will drop those 9 fiches from the live site (a real content-loss decision — get
  explicit sign-off first, do not decide this unilaterally).

## Standing quality bar — do not compromise on these

1. **Reproduce tables/figures verbatim** from the source (no logos). If a table
   or figure is a pure image with no text layer, render the source PDF page at
   200-250dpi with PyMuPDF (`fitz`) and transcribe it visually — do not guess
   or paraphrase.
2. **100% information coverage**, or an explicitly disclosed partial scope if a
   document is too large (state exactly what's excluded, in the fiche's own
   intro panel — never silently omit content).
3. **Triple-read + independent audit per document**: (a) build the fiche
   script, (b) do your own visual QA by rendering every page to PNG and
   reading it, (c) run a genuinely independent audit — either a fresh subagent
   given ONLY the source text (blind to your draft) that builds its own
   inventory and then diffs against the draft, or an equivalently rigorous
   self-check if subagents aren't available in this environment.
4. **Never fabricate or merge a composite grade/chip.** If a source has two
   differently-graded clauses in one sentence, split them into two rows. Before
   every build, run `grep -n '"[12][+-]/[12][+-]'` against the draft script as
   a safety net — must return no matches.
5. **Disclose source-internal inconsistencies, never silently resolve them.**
   If a source's own summary count doesn't match a direct tally, or a table
   contradicts body text, state both facts in the fiche and let the reader
   know — don't guess which one is "right."
6. **Visually verify every rendered page**, including page 1's header
   specifically — see the pagination bug below.

## Build pipeline (per fiche)

1. Find the source PDF URL in `build/library_final.json` (fields: `title`,
   `href`, `direct_pdf_url`, `exact_type`, `status`). Skip anything with
   `"status": "abrogé"`. Check the source's own page 1 for an obsolescence
   stamp before building (SFAR sometimes retires a document without updating
   this index — verified twice this session already, see git log).
2. Download: `curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" -o sources/X.pdf "<url>"`
   — sfar.org 403s a plain curl/WebFetch; the Chrome UA works. Some links are
   redirect wrappers (`/download/...?wpdmdl=NNN`) — follow with `-L`.
3. Extract text: PyMuPDF `fitz.open(...).get_text()` per page, concatenate to
   `sources/X.txt`. Read it in full to understand structure (numbered R1/R2
   recommendations? narrative-embedded prose? GRADE 1+/2+? a bespoke
   accord/vote scheme? — this corpus has used at least 7 distinct methodology
   conventions so far, see `build/fiche_aap_programmee.py` and
   `build/fiche_glycemie.py` docstrings for two examples of non-GRADE schemes).
4. Write `build/fiche_X.py` (reportlab). Copy the structural pattern from
   `build/fiche_aap_programmee.py` (dynamic pagination, `theme_table()` for
   sources with no numbering, `reco_table()` for GRADE-tagged rows,
   `KeepTogether` for heading+small-table pairs). **Reuse `build/style.py`'s
   shared helpers — do not duplicate colors/fonts.**
5. **CRITICAL BUG TO AVOID**: the `_count_pages()` helper (used to measure
   cumulative section page-counts before the final build) must write its
   throwaway measurement builds to a fresh `tempfile.mktemp()` path — NEVER to
   the same `OUT` path the final build uses. Reusing `OUT` for both was found
   to silently corrupt page 1's `header_band` (empty header, no title bar) in
   the final PDF. Copy `fiche_aap_programmee.py`'s `_count_pages()` exactly.
6. Build: `cd build && python3 fiche_X.py`. Check output page count.
7. Visually verify: render every page to PNG at 130-140dpi and read it
   (`fitz` `get_pixmap(dpi=130)`), including page 1's header specifically.
   If several pages are <60% full, try merging 1-2 adjacent SECTIONS via a
   combinator function, rebuild, and check the ACTUAL page count — revert if
   it doesn't help (this has happened before; don't assume a merge always
   reduces pages).
8. Independent audit: have a fresh context (subagent, or your own second pass
   with zero memory of the draft) build an inventory straight from the source
   text, then diff it against the draft's actual content. Apply real fixes.
9. Site integration — 4 files, always in this order:
   - `build/extract_content.py`: add `extract_X()` (monkeypatches the fiche
     module's `Paragraph`/`Table`/`grade_chip`/etc. to capture content as
     JSON — see any existing `extract_*()` for the pattern), plus a
     `__main__` block entry (module-reset tuple + call + json.dump).
   - `build/assemble.py`: add the `content_X.json` file-read + a
     `__CONTENT_X__` placeholder replace call.
   - `site/template.html`: add `<script id="content-X" type="application/json">__CONTENT_X__</script>`.
   - `site/app.js`: add an `X` entry to `RAW`, `FICHE_HREF_MATCH` (grep
     `library_final.json` to confirm your href/pdf-url needles match
     EXACTLY 1 entry — cross-contamination with a similarly-named older/newer
     document has happened before), and `DOC_META`.
10. Run `python3 extract_content.py && python3 assemble.py` from `build/`.
    Grep the freshly-assembled `site/rfe_garde.html` for your new
    `id="content-X"` marker to confirm it's present.
11. **Publish safety gate**: read the live Artifact first
    (`action: "read"` on the URL above), grep the saved baseline for ABSENCE
    of your new marker (confirms you're not clobbering a newer version you
    haven't seen), THEN publish `site/rfe_garde.html` to that same URL.
12. Copy the built PDF to `output/` (already the target dir if building from
    this repo) and to `/Users/macbook/Downloads/claude/RFE_SFAR_2026/` on the
    user's machine if you have filesystem access to it; otherwise just leave
    it in this repo's `output/`.
13. **Commit and push**: `git add -A && git commit -m "Add fiche NN: <title>" && git push`.
    Do this after EVERY fiche — this repo is the durability fix for two
    separate incidents this session where the interactive session's `/tmp`
    scratchpad silently lost files (14 fiche scripts + 11 PDFs + the library
    index vanished once during a long idle gap). Never let uncommitted work
    sit for long.

## If you're a scheduled/cloud routine run with no memory of prior sessions

- Start by reading `build/library_final.json` and diffing its 160 titles
  against `site/app.js`'s `FICHE_HREF_MATCH` keys to find unbuilt items.
- Prioritize acute/on-call clinical topics over routine/administrative ones,
  and prefer compact sources (under ~20 pages) you can fully build and audit
  in one run over very large ones (100+ pages) that need deliberate
  scope-limiting (already done for a few: sepsis, anaphylaxie — see their
  fiche scripts' docstrings for the scope-limiting pattern if you pick up a
  similarly huge document).
- If you hit usage/rate limits mid-fiche, stop gracefully after committing
  whatever is safely finished — do not leave the repo in a broken
  (non-building) state. The next scheduled run will continue.
- Do not ask the user for confirmation between fiches — standing instruction
  from the project owner is full autonomous continuation ("finis tout, sans
  me demander"), which extends to scheduled runs.
- Always finish a fiche's full pipeline (build → audit → integrate → publish
  → commit/push) before starting another, rather than leaving several
  half-integrated fiches at once.
