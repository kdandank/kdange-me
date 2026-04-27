#!/usr/bin/env python3
"""
Tests for the portfolio build/sync system.

Covers the three scenarios demonstrated manually during setup:
  1. Editing _body.html and committing triggers auto-rebuild of index.html
  2. Staging index.html directly (without _body.html) is blocked by the hook
  3. Staging files unrelated to the portfolio passes through silently

Plus structural integrity checks that run as part of CI.

Run:  python3 -m unittest discover -s tests
 or:  python3 -m pytest tests/
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTFOLIO = os.path.join(ROOT, "portfolio")


# ── Helpers ──────────────────────────────────────────────────────────────────

def git(args, cwd, **kwargs):
    return subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        **kwargs,
    )


def make_isolated_repo():
    """
    Clone the relevant files into a fresh temp git repo with hooks configured.
    Returns the path to the temp dir; caller must shutil.rmtree it.
    """
    tmpdir = tempfile.mkdtemp()
    for item in (".githooks", "portfolio", "setup.sh"):
        src = os.path.join(ROOT, item)
        dst = os.path.join(tmpdir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    git(["init"], tmpdir)
    git(["config", "user.email", "test@test.com"], tmpdir)
    git(["config", "user.name", "Test"], tmpdir)
    git(["config", "core.hooksPath", ".githooks"], tmpdir)
    git(["add", "."], tmpdir)
    git(["commit", "-m", "init", "--no-verify"], tmpdir)
    return tmpdir


def run_hook(tmpdir):
    hook = os.path.join(tmpdir, ".githooks", "pre-commit")
    return subprocess.run(hook, cwd=tmpdir, capture_output=True, text=True)


# ── Structural integrity ──────────────────────────────────────────────────────

class TestStructure(unittest.TestCase):

    def test_body_html_has_all_sections(self):
        """_body.html must contain every section marker."""
        with open(os.path.join(PORTFOLIO, "_body.html")) as f:
            content = f.read()
        markers = [
            "<!-- NAV -->", "<!-- HERO -->", "<!-- ABOUT -->",
            "<!-- EXPERIENCE -->", "<!-- SKILLS -->", "<!-- PROJECTS -->",
            "<!-- EDUCATION -->", "<!-- CONTACT -->",
        ]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_index_html_contains_body_content(self):
        """index.html must be the assembled output (GENERATED comment + body)."""
        with open(os.path.join(PORTFOLIO, "index.html")) as f:
            content = f.read()
        self.assertIn("GENERATED", content)
        self.assertIn("<!-- NAV -->", content)
        self.assertIn('src="script.js"', content)

    def test_php_includes_body_html(self):
        """index.php must reference _body.html via a PHP include."""
        with open(os.path.join(PORTFOLIO, "index.php")) as f:
            content = f.read()
        self.assertRegex(content, r"include.*_body\.html")


# ── Build system ─────────────────────────────────────────────────────────────

class TestBuild(unittest.TestCase):

    def test_build_is_idempotent(self):
        """Running build.py when nothing changed must report 'up to date'."""
        result = subprocess.run(
            ["python3", "portfolio/build.py"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("up to date", result.stdout)

    def test_body_change_rebuilds_index_html(self):
        """Modifying _body.html and running build.py must update index.html."""
        body_path = os.path.join(PORTFOLIO, "_body.html")
        html_path = os.path.join(PORTFOLIO, "index.html")

        with open(body_path) as f:
            original_body = f.read()
        with open(html_path) as f:
            original_html = f.read()

        marker = "<!-- TEST-MARKER-DO-NOT-COMMIT -->"
        try:
            with open(body_path, "w") as f:
                f.write(original_body.replace("<!-- NAV -->", f"<!-- NAV -->{marker}", 1))

            result = subprocess.run(
                ["python3", "portfolio/build.py"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("built from _body.html", result.stdout)

            with open(html_path) as f:
                new_html = f.read()
            self.assertIn(marker, new_html)

        finally:
            with open(body_path, "w") as f:
                f.write(original_body)
            subprocess.run(
                ["python3", "portfolio/build.py"],
                cwd=ROOT, capture_output=True,
            )


# ── Pre-commit hook scenarios ─────────────────────────────────────────────────

class TestPreCommitHook(unittest.TestCase):
    """
    Each test runs the hook in a fresh isolated git repo so tests are
    independent and leave the real repo untouched.
    """

    # Scenario 1: the one you want to always be able to run:
    # Editing _body.html triggers auto-rebuild and re-stage of index.html
    def test_body_edit_triggers_rebuild_and_restage(self):
        tmpdir = make_isolated_repo()
        try:
            body = os.path.join(tmpdir, "portfolio", "_body.html")
            with open(body, "a") as f:
                f.write("\n<!-- HOOK-TEST -->")
            git(["add", "portfolio/_body.html"], tmpdir)

            result = run_hook(tmpdir)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("rebuilt and staged", result.stdout)

            staged = git(["diff", "--cached", "--name-only"], tmpdir).stdout
            self.assertIn("portfolio/index.html", staged)
        finally:
            shutil.rmtree(tmpdir)

    # Scenario 2:
    # Staging index.html directly (without _body.html) must be blocked
    def test_direct_index_html_edit_is_blocked(self):
        tmpdir = make_isolated_repo()
        try:
            html = os.path.join(tmpdir, "portfolio", "index.html")
            with open(html, "a") as f:
                f.write("\n<!-- DIRECT EDIT -->")
            git(["add", "portfolio/index.html"], tmpdir)

            result = run_hook(tmpdir)

            self.assertNotEqual(result.returncode, 0)
            combined = result.stdout + result.stderr
            self.assertIn("generated", combined.lower())
        finally:
            shutil.rmtree(tmpdir)

    # Scenario 3:
    # Staging files unrelated to the portfolio passes through silently
    def test_unrelated_file_passes_silently(self):
        tmpdir = make_isolated_repo()
        try:
            unrelated = os.path.join(tmpdir, "notes.txt")
            with open(unrelated, "w") as f:
                f.write("unrelated\n")
            git(["add", "notes.txt"], tmpdir)

            result = run_hook(tmpdir)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "")
        finally:
            shutil.rmtree(tmpdir)

    # Bonus: removing the include from index.php must also be blocked
    def test_php_missing_include_is_blocked(self):
        tmpdir = make_isolated_repo()
        try:
            php_path = os.path.join(tmpdir, "portfolio", "index.php")
            with open(php_path) as f:
                content = f.read()
            with open(php_path, "w") as f:
                f.write(re.sub(r".*include.*_body\.html.*\n", "", content))
            git(["add", "portfolio/index.php"], tmpdir)

            result = run_hook(tmpdir)

            self.assertNotEqual(result.returncode, 0)
            combined = result.stdout + result.stderr
            self.assertIn("_body.html", combined)
        finally:
            shutil.rmtree(tmpdir)


if __name__ == "__main__":
    unittest.main(verbosity=2)
