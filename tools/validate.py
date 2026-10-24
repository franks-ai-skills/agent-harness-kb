"""Validate this KB with Harness Forge's validator, and check its release.

Usage, from the KB root, with Python 3.11 or newer and no installed packages
(Forge's validator brings its bundled dependencies):
    python3 -I -S tools/validate.py [--forge ../harness-forge]

Forge owns the schemas; the copies in schemas/ must be byte-identical.
The release check is this repository's own (the policy in CHANGELOG.md):
kb_version needs a dated section at the top of CHANGELOG.md, and the
snapshot paths may not differ from tag v<kb_version> once it exists.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# The paths Harness Forge copies into its snapshot (its tools/pin_snapshot.py).
SNAPSHOT_PATHS = ("docs", "rules", "schemas", "policy", "checks", "fixtures", "kb-manifest.json")
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def check_release(root: Path) -> tuple[list[str], list[str]]:
    """Return the release errors and notes for the KB checkout at ``root``."""
    root = Path(root)
    errors, notes = [], []
    version = json.loads((root / "kb-manifest.json").read_text(encoding="utf-8"))["kb_version"]
    if not VERSION.match(version):
        return [f"kb-manifest.json: kb_version {version!r} is not MAJOR.MINOR.PATCH"], notes
    changelog = root / "CHANGELOG.md"
    headings = re.findall(r"^## (.+)$", changelog.read_text(encoding="utf-8"), re.M) if changelog.is_file() else []
    if not headings or not re.fullmatch(rf"{re.escape(version)} \(\d{{4}}-\d{{2}}-\d{{2}}\)", headings[0]):
        found = f"## {headings[0]}" if headings else "none"
        errors.append(f"CHANGELOG.md: the first section must be '## {version} (YYYY-MM-DD)', found {found}")

    listed = _git(root, "tag", "--list", "v*")
    if listed.returncode != 0:
        return errors + [f"git tag --list: {listed.stderr.strip()}"], notes
    released = {tag: tuple(map(int, match.groups()))
                for tag in listed.stdout.split() if (match := VERSION.match(tag[1:]))}
    tag = f"v{version}"
    if tag not in released:
        if not released:
            notes.append("release comparison skipped: this checkout has no v<version> tags")
        elif tuple(map(int, VERSION.match(version).groups())) <= max(released.values()):
            latest = max(released, key=released.get)
            errors.append(f"kb-manifest.json: kb_version {version} is not tagged and not above the latest release {latest}")
        else:
            notes.append(f"{tag} is not tagged yet: tag the merge commit after the merge")
        return errors, notes

    commit = _git(root, "rev-parse", "--verify", f"{tag}^{{commit}}")
    if commit.returncode != 0:
        return errors + [f"git rev-parse {tag}: {commit.stderr.strip()}"], notes
    # Against the working tree, so local edits count; untracked files are listed separately.
    changed = set()
    for command in (("diff", "--name-only", commit.stdout.strip()), ("ls-files", "--others", "--exclude-standard")):
        result = _git(root, *command, "--", *SNAPSHOT_PATHS)
        if result.returncode != 0:
            return errors + [f"git {command[0]}: {result.stderr.strip()}"], notes
        changed.update(result.stdout.split())
    if changed:
        errors.append(f"{', '.join(sorted(changed))}: changed since release {tag}; raise kb_version and add its "
                      "CHANGELOG.md section")
    return errors, notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forge", default="../harness-forge", help="harness-forge checkout")
    arguments = parser.parse_args(argv)
    source = Path(arguments.forge).resolve() / "src"
    if not (source / "harness_forge" / "documents.py").is_file():
        print(f"validate.py: no harness-forge checkout at {arguments.forge}", file=sys.stderr)
        return 2
    sys.path.insert(0, str(source))
    from harness_forge.documents import validate_kb

    root = Path(__file__).resolve().parents[1]
    release_errors, notes = check_release(root)
    errors = validate_kb(root) + release_errors
    print(json.dumps({"ok": not errors, "error_count": len(errors), "errors": errors[:100], "notes": notes}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
