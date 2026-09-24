---
name: __SECTOR_ORCH__
kind: orchestrator
disable-model-invocation: true
description: "Orchestrator (not a knowledge pack): routes a free-text __SECTOR_NAME__ question to the right catalogue pack(s), reads them with you, and answers with pack and chapter citations. Runs only on explicit `/__SECTOR_ORCH__ <question>`; carries no source content. Use when you do not know which `/pack` to ask."
---

<!-- argument-hint: [free-text __SECTOR_NAME__ question] -->

# __SECTOR_NAME__ Orchestrator: routes questions to the right knowledge packs

**This is an orchestrator, not a knowledge pack.** It carries **no source content**.
On explicit `/__SECTOR_ORCH__ <question>` it matches your question to installed catalogue packs,
reads them, and answers with pack and chapter citations.

## When to use
**Prerequisites:** none: plain Markdown; works on any host that loads Agent Skills. Pair it with the packs it routes to.

`/__SECTOR_ORCH__` answers __SECTOR_NAME__ questions by consulting installed packs. It is an
entry point, not a knowledge base. Use it when you do not already know which `/<slug>`
to open.

## How /__SECTOR_ORCH__ answers

### Modes

| Mode | When | Gate |
|---|---|---|
| Narrow consult | One Topics row matches, at most one agency named, no compare/contrast/survey verb | None. Best single pack. End with "Also relevant" runners-up. |
| Broad consult | Two or more Topics rows, two or more agencies, or a compare/contrast/survey verb | One plan approval naming packs and why, then run to done. Disagreements under "Where the sources differ"; never average or blend. |
| Deliverable | An artifact verb (draft, write, produce, prepare, build, review, verify) plus a Deliverables row name or keyword | Plan approval, then stage pauses after Draft and after Review (Verify is last). |

### Routing

1. Match Topics keywords case-insensitively, with synonym judgement.
2. Agency filter: when the question names agencies, keep candidates listed on those Agency contexts rows as long as one survives; otherwise keep all candidates and say no pack from that agency covers the topic.
3. Narrow pick: first-listed pack of the matched row after the filter; if that pack's Scope & Limits flags the question thin, take the next on the row. The consult stays narrow (no gate).
4. Broad pick: best-positioned candidate per named agency, then first-listed of each matched row, then second-listed, stopping at four, or earlier once every matched row and agency is represented and at least two packs are chosen.
5. No match: name the three closest Topics rows, suggest a rephrase or a direct `/<slug>`, and make **no __SECTOR_NAME__ claims**.

### Reading

A pack lives at `../<slug>/` from this folder (native installs put members side by side). For each selected pack: read its `SKILL.md` index; open at most two chapters from its Topic Index / Chapter Index; open one support file (`glossary.md`, `patterns.md`, or `cheatsheet.md`) only for term, technique, or decision-rule questions. At most four packs total. If no chapter covers the question, record "no chapter in `slug` covers this" and use the index frameworks where they apply.

Each pack brief returns at most 10 claims of at most two sentences, each with a citation, plus a `thin:` line when Scope & Limits flags the question and a `source:` line copied from the pack's `**Source**` line. No claim from outside its pack.

### Citations and Sources

Cite only files read this session, in these forms: `[slug chNN]`, `[slug index]`,
`[slug glossary|patterns|cheatsheet]`. Drop uncited claims. Agreeing claims merge into one statement carrying every citation. Where the packs are silent, say so; no fallback to model memory. Every answer ends with a **Sources** block listing each pack's slug, its `**Source**` line, and its licence. Content-pack licences come from the Licences table, else the label `Public Domain (US Government work)`. Signpost lines read `MIT (signpost)`. Non-commercial and share-alike terms appear in full.

### Deliverable stage chains

The matched Deliverables row is the chain. Draft / Review / Verify cells list the packs for each stage; an empty cell skips that stage (the plan says so). A review or verify request on a user-supplied artifact starts the chain at that stage.

- **Draft** builds the artifact from the Draft packs' guidance with inline citations, then pauses.
- **Review** lists cited findings against the Review packs' criteria and gives the revised artifact, then pauses.
- **Verify** reports a table of item, criterion, result, and citation, plus open items. It edits nothing and offers fixes as a follow-up.

Output goes in the reply unless the user names a file. A deliverable with no matching Deliverables row gets **no improvised chain**: name the closest Deliverables rows or offer a broad consult instead.

### Edge cases

- Bare `/__SECTOR_ORCH__` with no argument: print usage and three example questions drawn from the Topics rows.
- Sub-agent failure: rerun that brief in the main thread.
- Thin-pack step-down: if the selected pack's Scope & Limits flags the question thin, take the next pack on the row; the consult stays narrow.

## Routing map

<!-- ROUTING-MAP:BEGIN -->
### Topics
| Topic | Keywords | Packs (best first) |
|---|---|---|

### Agency contexts
| Agency | Keywords | Packs |
|---|---|---|

### Deliverables
| Deliverable | Keywords | Draft | Review | Verify |
|---|---|---|---|---|

### Licences
| Pack | Licence |
|---|---|
<!-- ROUTING-MAP:END -->

## Host modes

Pick the highest mode the host can run:

| Mode | When | Behaviour |
|---|---|---|
| Fan-out | Sub-agents available | One brief per pack in parallel; main thread composes the answer. On sub-agent failure, rerun that brief in the main thread. |
| Sequential | No sub-agents, member files readable | Same briefs one at a time; write each pack's notes before opening the next. |
| Index-only | Transform installs (Codex, Gemini, Cursor rules) | Read sibling index files when readable. Cite `[slug index]` only, name chapters as follow-ups, and label the answer `index-level: chapter bodies not installed`. |
| Route-only | No member file readable | Report the routing decision and the `/slug` commands only. Make **no __SECTOR_NAME__ claims**. |

**Native-root fallback.** When the skill folder is not revealed, try
`~/.claude/skills/`, `~/.openclaw/skills/`, `~/.copilot/skills/`, each with and
without the `__REPO_NAME__/` namespace. Transform index files live at
`~/.codex/prompts/<slug>.md`, `~/.gemini/commands/__REPO_NAME__/<slug>.toml`,
and `./.cursor/rules/<slug>.mdc`.

Narrow consults read in the main thread on every host. A missing routed pack is
noted and skipped; if none remain, fall back to route-only.

## Scope & Limits

- No __SECTOR_NAME__ claim without a citation from a pack file read this session.
- The map is curated, not exhaustive. Agency rows are a filter, not an endorsement.
- At most six packs per Topics row. At most four packs read per answer.
- Deliverable stage chains come only from Deliverables rows; empty cells skip that stage.
- `/__SECTOR_ORCH__` never overwrites an existing file without a yes at a gate.

---
*Orchestrator content © JG Systems Consulting Ltd. (MIT). Pack names and source titles
are identified for routing only; each pack keeps its own licence.*
