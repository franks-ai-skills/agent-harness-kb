"""Validate this KB with Harness Forge's validator.

Usage, from the KB root, with Forge's locked environment:
    ../harness-forge/.venv/bin/python tools/validate.py [--forge ../harness-forge]

Forge owns the schemas; the copies in schemas/ must be byte-identical.
"""

import argparse
import json
import sys
from pathlib import Path


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

    errors = validate_kb(Path(__file__).resolve().parents[1])
    print(json.dumps({"ok": not errors, "error_count": len(errors), "errors": errors[:100]}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
