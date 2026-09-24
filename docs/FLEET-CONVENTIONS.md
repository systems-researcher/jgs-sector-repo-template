<!--
Copyright (c) 2026 JG Systems Consulting Ltd. MIT License (see ../LICENSE).
SPDX-License-Identifier: MIT
-->

# Fleet conventions

Rules for the industry knowledge-pack fleet: how sector repos are named, laid out,
owned, indexed, licensed, and gated. Every minted sector repo ships this file.

## Repo naming

Sector catalogue repos use the pattern `jgs-<sector>-knowledge-packs`, where
`<sector>` is the short sector slug (for example `se`, `med`, `aero`). The template
repository is `jgs-sector-repo-template`; it is not itself a sector catalogue and is
not installed as packs.

## Packs layout

Content lives under `packs/<slug>/`. Each pack directory holds at least `SKILL.md`
and `PACK.yaml`, plus the chapter and supporting files the pack-spec requires for
its kind (`content`, `signpost`, or `orchestrator`). Slugs are lowercase
`[a-z0-9-]+`.

## One sector orchestrator per repo

Each sector repo has exactly one orchestrator skill (`kind: orchestrator`). Its
directory slug is the sector command users type (for example `/se`, `/med`). The
orchestrator carries no source content; it routes free-text questions through the
routing map in its `SKILL.md` to the right pack(s).

## Sibling repos, never absorption

Sector repos are siblings of `jgs-se-knowledge-packs`. A new sector does not fold
into the SE catalogue. Packs do not migrate across sector boundaries by absorption;
if a pack belongs in another sector, it is authored or moved there under that
sector's release train.

## Release ownership

Each sector repo owns its own release train: version in `RELEASE-INFO.txt`,
website product YAMLs, changelog, tags, and CI. A green build in one sector does
not release another. The hub never cuts sector tags.

## Hub index contract

The hub indexes sector repos with links plus metadata only (name, slug, version,
status, short scope). The hub does not carry pack content, chapter text, or
installer copies of sector packs. Discovery points at the sector repo; install
runs against that repo.

## Licensing split

Pack content licence lives with the pack (`packs/<slug>/LICENSE` and per-pack
NOTICE attribution). Repository tooling, scaffolding, docs chrome, and gates are
MIT under the root `LICENSE`. Do not relicense pack content under the repo MIT
line.

## Link-policy host lockstep

`tooling/link-policy-hosts.txt` and the inline trusted-host set in
`.github/workflows/validate.yml` move in lockstep. Edit both or neither. At mint
time, `tooling/instantiate.py --add-host` is the sanctioned editor; after mint,
sector maintainers apply the same dual edit. A host present in only one place is
drift and fails the gate.

## Sector minimum bar

A sector earns its own repo when a single gate-green instantiation has all of:

1. **Content floor.** At least one redistributable full pack (tier 1, or tier 2/3
   with per-document licence capture), **or** a landing set of at least two
   signpost packs whose free-path rows link to shipped landing packs (in this
   fleet or the exemplar catalogue).
2. **Orchestrator coverage.** A named sector orchestrator whose routing map
   covers every content pack in the repo.
3. **Gates green.** `tooling/validate_pack.py`, `tooling/check_release.py`, and CI
   (`tooling/test_ci_gate.py` parity with `.github/workflows/validate.yml`) exit 0
   on the minted repo.

Below the bar the sector stays in programme backlog. Holding options are a
backlog row and, once the hub exists, a hub README mention. No empty repos and no
single-signpost-only forks.
