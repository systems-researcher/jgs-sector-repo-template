#!/usr/bin/env python3
"""Mint a jgs-<sector>-knowledge-packs repo from this template.

Stdlib only. Copies the template tree, renames tokenized paths, substitutes
the four identity tokens in UTF-8 text files and output path names, edits
link-policy hosts in lockstep, and refuses to leave any token behind.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

TOKENS = ["__SECTOR_SLUG__", "__SECTOR_NAME__", "__SECTOR_ORCH__", "__REPO_NAME__"]
EXCLUDE_DIRS = {".git", "__pycache__", ".superpowers"}
EXCLUDE_FILES = {"tooling/instantiate.py", "tooling/test_instantiate.py"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOKEN_RE = re.compile("|".join(re.escape(t) for t in TOKENS))


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sector", required=True, help="short sector slug, e.g. med-device")
    p.add_argument("--name", required=True, help="sector display name, e.g. 'Medical Device'")
    p.add_argument("--orch", required=True, help="orchestrator command slug, e.g. med")
    p.add_argument("--target", required=True, help="destination directory for the minted repo")
    p.add_argument("--add-host", action="append", default=[], metavar="HOST",
                   help="extra link-policy host (repeatable; added to hosts file and CI set)")
    p.add_argument("--dry-run", action="store_true", help="print the plan; write nothing")
    return p.parse_args(argv)


def validate_args(args):
    for slug in (args.sector, args.orch):
        if not SLUG_RE.match(slug):
            sys.exit("error: slugs must match ^[a-z0-9]+(-[a-z0-9]+)*$: %r" % slug)
    target = Path(args.target).resolve()
    if target.exists() and any(target.iterdir()) and not args.dry_run:
        sys.exit("error: target exists and is not empty: %s" % target)
    return target


def iter_template(root):
    """Yield relative paths of everything to copy, honoring the exclusion lists."""
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if str(rel).replace("\\", "/") in EXCLUDE_FILES:
            continue
        yield rel, path


def renamed(rel, mapping):
    """Path with tokens replaced in every segment."""
    return Path(*[TOKEN_RE.sub(lambda m: mapping[m.group(0)], part) for part in rel.parts])


def substitute(text, mapping):
    for token, value in mapping.items():
        text = text.replace(token, value)
    return text


def minted_hosts(hosts_text):
    return {line.strip() for line in hosts_text.splitlines()
            if line.strip() and not line.strip().startswith("#")}


def apply_hosts(target, hosts):
    """Append hosts to the hosts file and the workflow inline set, idempotently."""
    hosts_file = target / "tooling" / "link-policy-hosts.txt"
    workflow = target / ".github" / "workflows" / "validate.yml"
    htext = hosts_file.read_text(encoding="utf-8")
    existing = minted_hosts(htext)
    wtext = workflow.read_text(encoding="utf-8")
    for host in hosts:
        if host in existing:
            continue
        htext = (htext.rstrip("\n") + "\n" + host) if htext.strip() else host + "\n"
        pattern = re.compile(r"(TRUSTED_HOSTS\s*=\s*frozenset\(\{)(.*?)(\}\))", re.S)
        match = pattern.search(wtext)
        if not match:
            sys.exit("error: TRUSTED_HOSTS frozenset literal not found in workflow")
        inner = match.group(2)
        if ('"%s"' % host) not in inner:
            wtext = wtext[:match.end(2)] + ' "%s",' % host + wtext[match.end(2):]
        existing.add(host)
    hosts_file.write_text(htext, encoding="utf-8")
    workflow.write_text(wtext, encoding="utf-8")


def residue_scan(target):
    """Return (bad_paths, bad_files): token hits in path names or UTF-8 contents."""
    bad_paths, bad_files = [], []
    for path in sorted(target.rglob("*")):
        rel = str(path.relative_to(target))
        if TOKEN_RE.search(rel):
            bad_paths.append(rel)
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                continue
            if TOKEN_RE.search(text):
                bad_files.append(rel)
    return bad_paths, bad_files


def main(argv):
    args = parse_args(argv)
    target = validate_args(args)
    repo_name = "jgs-%s-knowledge-packs" % args.sector
    mapping = {
        "__SECTOR_SLUG__": args.sector,
        "__SECTOR_NAME__": args.name,
        "__SECTOR_ORCH__": args.orch,
        "__REPO_NAME__": repo_name,
    }
    root = Path(__file__).resolve().parent.parent
    plan = list(iter_template(root))
    print("mint %s -> %s (%d files)" % (repo_name, target, len(plan)))
    for rel, src in plan:
        dst = renamed(rel, mapping)
        hits = ""
        if src.is_file():
            try:
                text = src.read_text(encoding="utf-8")
                found = sorted({t for t in TOKENS if t in text})
                if found:
                    hits = "  [%s]" % ", ".join(found)
            except (UnicodeDecodeError, ValueError):
                pass
        print("  %s -> %s%s" % (rel, dst, hits))
    if args.add_host:
        print("  hosts += %s (hosts file + workflow inline set)" % ", ".join(args.add_host))
    if args.dry_run:
        print("dry-run: nothing written")
        return 0
    if target.exists():
        shutil.rmtree(target)
    for rel, src in plan:
        dst = target / renamed(rel, mapping)
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = src.read_text(encoding="utf-8")
        except (UnicodeDecodeError, ValueError):
            shutil.copy2(src, dst)
            continue
        dst.write_text(substitute(text, mapping), encoding="utf-8")
    if args.add_host:
        apply_hosts(target, args.add_host)
    bad_paths, bad_files = residue_scan(target)
    if bad_paths or bad_files:
        print("error: token residue", file=sys.stderr)
        for rel in bad_paths:
            print("  path: %s" % rel, file=sys.stderr)
        for rel in bad_files:
            print("  file: %s" % rel, file=sys.stderr)
        shutil.rmtree(target)
        return 1
    assert not (target / "packs" / "__SECTOR_ORCH__").exists(), "old tokenized path present"
    print("minted. next steps:")
    print("  cd %s" % target)
    print("  git init -b main && git add -A && git commit -m 'chore: mint from sector-repo template'")
    print("  python install.py --dry-run")
    print("  build your first pack under packs/ (see docs/PACK-SPEC.md), then add it to the orchestrator routing map")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
