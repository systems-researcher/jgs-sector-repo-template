<!--
Copyright (c) 2026 JG Systems Consulting Ltd. - MIT License (see LICENSE).
SPDX-License-Identifier: MIT
-->

<h1 align="center">__REPO_NAME__</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT%20(tooling)-blue" alt="License: MIT (tooling)">
  <img src="https://img.shields.io/badge/version-0.1.0-green" alt="Version 0.1.0">
  <img src="https://img.shields.io/badge/type-template-orange" alt="Template repository">
</p>

<p align="center">
  <strong>Starting point for a sector knowledge-pack catalogue. This repository is a
  TEMPLATE: it is not installed as packs. Mint your own sector repo from it.
  (Minted repos: replace this section with your catalogue introduction.)</strong>
</p>

**Copyright (c) 2026 JG Systems Consulting Ltd. - MIT License (tooling); pack content under each source's own licence (see [NOTICE](NOTICE)).**

---

## What it is

This repo is the source template for the industry knowledge-pack fleet: one repo per
engineering sector, each an installable catalogue of knowledge-pack skills for coding
agents, with a single orchestrator that routes free-text sector questions to the right
packs. The template carries the legal root, the pack specification, the validators and
CI gates, and the installer, so a minted repo starts compliant and gated.

Minting copies the tree, substitutes four identity tokens (`__SECTOR_SLUG__`,
`__SECTOR_NAME__`, `__SECTOR_ORCH__`, `__REPO_NAME__`) in file contents and path names,
and refuses to finish if any token survives in the output. Fleet-wide naming, layout,
and release rules: [docs/FLEET-CONVENTIONS.md](docs/FLEET-CONVENTIONS.md).

## How to mint

```bash
python tooling/instantiate.py --sector <slug> --name "<name>" --orch <slug> --target <path>
```

- `--sector`: short sector slug (lowercase, hyphenated, e.g. `med-device`). Sets
  `__SECTOR_SLUG__` and the repo name `jgs-<sector>-knowledge-packs`.
- `--name`: sector display name (e.g. `"Medical Device"`). Sets `__SECTOR_NAME__`.
- `--orch`: orchestrator command slug (e.g. `med`). Sets `__SECTOR_ORCH__`; users type
  `/<orch> <question>` after install.
- `--target`: destination directory. It must not already exist or must be empty.

Options:

- `--add-host HOST` (repeatable): adds a link-policy host to
  `tooling/link-policy-hosts.txt` and the trusted inline set in
  `.github/workflows/validate.yml` in one step. Use it when your sector's vetted
  sources live on a host the template does not already list.
- `--dry-run`: prints the full plan (files, token hits, host additions) and writes
  nothing.

After a successful mint:

```bash
cd <path>
git init -b main && git add -A && git commit -m "chore: mint from sector-repo template"
python install.py --dry-run
```

## What the template carries

- **Legal root:** [LICENSE](LICENSE) (MIT, tooling and scaffolding only),
  [NOTICE](NOTICE), [COPYRIGHT](COPYRIGHT), [SECURITY.md](SECURITY.md),
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [CONTRIBUTING.md](CONTRIBUTING.md),
  [CITATION.cff](CITATION.cff).
- **Spec docs:** [docs/PACK-SPEC.md](docs/PACK-SPEC.md) (the pack contract),
  [docs/SOURCE-VETTING.md](docs/SOURCE-VETTING.md) (source eligibility and tiers),
  [docs/LICENSING.md](docs/LICENSING.md) (two-layer licence model and the link
  policy), [docs/skill-usage.md](docs/skill-usage.md), and
  [docs/FLEET-CONVENTIONS.md](docs/FLEET-CONVENTIONS.md) (fleet rules every minted
  repo ships).
- **Validators:** `tooling/validate_pack.py` (pack structure), `tooling/build_pack.py`,
  `tooling/check_release.py` (release gate), plus capability-map, classification, and
  overlap checks.
- **CI:** [.github/workflows/validate.yml](.github/workflows/validate.yml), kept in
  parity with the local gate by `tooling/test_ci_gate.py`.
- **Installer:** `install.py` / `install.sh` / `install.ps1` with a host-parity guard
  (`tooling/test_install_guard.py`).
- **Orchestrator stub:** `packs/__SECTOR_ORCH__/`, an explicit `/<orch> <question>`
  router that carries no source content; point its routing map at your packs.
- **Empty catalogue stubs:** [SKILLS.md](SKILLS.md), [catalog.json](catalog.json),
  `docs/packs.html`, [CHANGELOG.md](CHANGELOG.md), [RELEASE-INFO.txt](RELEASE-INFO.txt)
  at version 0.1.0.

## Gates

Run all three from the repo root:

```bash
python tooling/validate_pack.py --all   # every pack matches docs/PACK-SPEC.md
python tooling/check_release.py         # release readiness: files, versions, leaks, links, index, headers
python tooling/test_ci_gate.py          # proves CI (.github/workflows/validate.yml) checks the same things
```

CI green is not release-ready: `check_release.py` is the pre-tag gate. It prints a
`RELEASE CHECK: PASS (v<version> @ <sha>)` receipt; run it before tagging and confirm
the sha matches the commit you tag. A minted repo is release-ready only when all three
gates exit 0 (see the mint bar in [docs/FLEET-CONVENTIONS.md](docs/FLEET-CONVENTIONS.md)).

## Smoke proof

```bash
python tooling/test_instantiate.py
```

Mints a throwaway sector into a temp directory and runs all three gates against the
minted output, then asserts zero token residue. Exits 0 with `SMOKE PROOF PASS`.

## Licence

Two separable layers:

- **Tooling and scaffolding:** [MIT](LICENSE) (JG Systems Consulting Ltd.).
- **Pack content:** each pack carries its source's own licence, declared in
  `packs/<slug>/LICENSE` and `packs/<slug>/PACK.yaml`, independent of the repo's MIT
  licence. Attributions live in [NOTICE](NOTICE); the model is set out in
  [docs/LICENSING.md](docs/LICENSING.md).
