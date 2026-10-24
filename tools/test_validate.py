"""Tests for the release check in tools/validate.py.

Run from the KB root with Python 3.11 or newer and no installed packages:
    python3 -I -S tools/test_validate.py
"""

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
_specification = importlib.util.spec_from_file_location("validate", TOOLS / "validate.py")
validate = importlib.util.module_from_spec(_specification)
_specification.loader.exec_module(validate)

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
           "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.invalid", "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_CONFIG_NOSYSTEM": "1"}


class ReleaseCheckTest(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory(prefix="kb-release-")
        self.root = Path(self._directory.name)
        self.git("init", "-q", "-b", "main")
        self.write_release("0.1.0", "2026-10-16")
        (self.root / "rules").mkdir()
        (self.root / "rules" / "skills.yaml").write_text("rules: []\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("# KB\n", encoding="utf-8")
        self.commit("first release")

    def tearDown(self):
        self._directory.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True, text=True,
                              env=GIT_ENV).stdout

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def write_release(self, version: str, date: str, older: str = "") -> None:
        (self.root / "kb-manifest.json").write_text(json.dumps({"kb_version": version}) + "\n", encoding="utf-8")
        (self.root / "CHANGELOG.md").write_text(f"# Changelog\n\nPolicy.\n\n## {version} ({date})\n\n- Entry.\n{older}",
                                                encoding="utf-8")

    def check(self) -> tuple[list[str], list[str]]:
        return validate.check_release(self.root)

    def test_untagged_checkout_skips_the_comparison(self):
        errors, notes = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(notes, ["release comparison skipped: this checkout has no v<version> tags"])

    def test_released_content_passes(self):
        self.git("tag", "v0.1.0")
        self.assertEqual(self.check(), ([], []))

    def test_annotated_tag_passes(self):
        self.git("tag", "-a", "v0.1.0", "-m", "0.1.0")
        self.assertEqual(self.check(), ([], []))

    def test_committed_change_after_the_release_fails(self):
        self.git("tag", "v0.1.0")
        (self.root / "rules" / "skills.yaml").write_text("rules: [changed]\n", encoding="utf-8")
        self.commit("change a rule")
        errors, _ = self.check()
        self.assertEqual(len(errors), 1)
        self.assertIn("rules/skills.yaml: changed since release v0.1.0", errors[0])

    def test_local_edit_after_the_release_fails(self):
        self.git("tag", "v0.1.0")
        (self.root / "rules" / "skills.yaml").write_text("rules: [edited]\n", encoding="utf-8")
        errors, _ = self.check()
        self.assertIn("rules/skills.yaml: changed since release v0.1.0", errors[0])

    def test_untracked_snapshot_file_after_the_release_fails(self):
        self.git("tag", "v0.1.0")
        (self.root / "rules" / "new.yaml").write_text("rules: []\n", encoding="utf-8")
        errors, _ = self.check()
        self.assertIn("rules/new.yaml: changed since release v0.1.0", errors[0])

    def test_change_outside_the_snapshot_paths_passes(self):
        self.git("tag", "v0.1.0")
        (self.root / "AGENTS.md").write_text("# KB\n\nMore.\n", encoding="utf-8")
        self.commit("instructions only")
        self.assertEqual(self.check(), ([], []))

    def test_new_version_waits_for_its_tag(self):
        self.git("tag", "v0.1.0")
        (self.root / "rules" / "skills.yaml").write_text("rules: [changed]\n", encoding="utf-8")
        self.write_release("0.2.0", "2026-10-23", older="\n## 0.1.0 (2026-10-16)\n\n- Entry.\n")
        self.commit("release 0.2.0")
        self.assertEqual(self.check(), ([], ["v0.2.0 is not tagged yet: tag the merge commit after the merge"]))
        self.git("tag", "v0.2.0")
        self.assertEqual(self.check(), ([], []))

    def test_untagged_version_below_the_latest_release_fails(self):
        self.git("tag", "v0.2.0")
        errors, _ = self.check()
        self.assertEqual(errors, ["kb-manifest.json: kb_version 0.1.0 is not tagged and not above the latest release v0.2.0"])

    def test_unreleased_section_fails(self):
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## 0.1.0 (unreleased)\n\n- Entry.\n", encoding="utf-8")
        errors, _ = self.check()
        self.assertEqual(errors, ["CHANGELOG.md: the first section must be '## 0.1.0 (YYYY-MM-DD)', found ## 0.1.0 (unreleased)"])

    def test_section_for_another_version_first_fails(self):
        (self.root / "CHANGELOG.md").write_text("# Changelog\n\n## Unreleased\n\n- New.\n\n## 0.1.0 (2026-10-16)\n",
                                                encoding="utf-8")
        errors, _ = self.check()
        self.assertEqual(errors, ["CHANGELOG.md: the first section must be '## 0.1.0 (YYYY-MM-DD)', found ## Unreleased"])

    def test_malformed_version_fails(self):
        (self.root / "kb-manifest.json").write_text(json.dumps({"kb_version": "0.2"}) + "\n", encoding="utf-8")
        self.assertEqual(self.check(), (["kb-manifest.json: kb_version '0.2' is not MAJOR.MINOR.PATCH"], []))

    def test_git_failure_is_an_error(self):
        with tempfile.TemporaryDirectory(prefix="kb-no-git-") as directory:
            root = Path(directory)
            (root / "kb-manifest.json").write_text(json.dumps({"kb_version": "0.1.0"}) + "\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("# Changelog\n\n## 0.1.0 (2026-10-16)\n", encoding="utf-8")
            errors, notes = validate.check_release(root)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("git tag --list: "), errors)
        self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
