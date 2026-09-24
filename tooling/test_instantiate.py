#!/usr/bin/env python3
"""Smoke proof: mint a throwaway sector into a temp dir and run its gates.

Assert-based, stdlib only. Exits 0 when the minted repo passes validate_pack
--all, test_validate_pack.py, check_release.py, and test_ci_gate.py, with
zero token residue.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "tooling" / "instantiate.py"
TOKENS = ["__SECTOR_SLUG__", "__SECTOR_NAME__", "__SECTOR_ORCH__", "__REPO_NAME__"]
TOKEN_RE = None  # built below without importing the script


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return result


def build_token_re():
    import re
    return re.compile("|".join(re.escape(t) for t in TOKENS))


def residue(minted):
    regex = build_token_re()
    hits = []
    for path in minted.rglob("*"):
        rel = str(path.relative_to(minted))
        if regex.search(rel):
            hits.append("path: " + rel)
        if path.is_file():
            try:
                if regex.search(path.read_text(encoding="utf-8")):
                    hits.append("file: " + rel)
            except (UnicodeDecodeError, ValueError):
                pass
    return hits


def main():
    import re
    global TOKEN_RE
    TOKEN_RE = build_token_re()
    tmp = Path(tempfile.mkdtemp(prefix="sector-mint-"))
    target = tmp / "jgs-smoke-knowledge-packs"
    try:
        dry = run([sys.executable, str(SCRIPT), "--sector", "smoke", "--name", "Smoke",
                   "--orch", "smoke", "--target", str(target), "--dry-run"], cwd=ROOT)
        assert dry.returncode == 0, dry.stderr
        assert not target.exists(), "dry-run created the target"
        assert "dry-run: nothing written" in dry.stdout, dry.stdout

        real = run([sys.executable, str(SCRIPT), "--sector", "smoke", "--name", "Smoke",
                    "--orch", "smoke", "--target", str(target),
                    "--add-host", "example.gov"], cwd=ROOT)
        assert real.returncode == 0, real.stderr
        assert (target / "packs" / "smoke" / "PACK.yaml").is_file(), "orchestrator dir not renamed"
        assert not (target / "packs" / "__SECTOR_ORCH__").exists(), "tokenized path remains"
        hosts = (target / "tooling" / "link-policy-hosts.txt").read_text(encoding="utf-8")
        assert "example.gov" in hosts, "host not added to hosts file"
        wf = (target / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        assert '"example.gov"' in wf, "host not added to inline TRUSTED_HOSTS"
        hits = residue(target)
        assert not hits, "token residue: %r" % hits

        # Path components joined: brief listed ["tooling", "script.py"] as path
        # parts; subprocess needs one script path argument.
        for gate in (["tooling/validate_pack.py", "--all"],
                     ["tooling/test_validate_pack.py"],
                     ["tooling/check_release.py"],
                     ["tooling/test_ci_gate.py"]):
            result = run([sys.executable] + gate, cwd=target)
            assert result.returncode == 0, "%s failed:\n%s%s" % (
                " ".join(gate), result.stdout, result.stderr)
        print("SMOKE PROOF PASS")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
