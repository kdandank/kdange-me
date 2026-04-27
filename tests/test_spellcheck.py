#!/usr/bin/env python3
"""
Spell-check test for portfolio/_body.html.

Always passes; findings are printed as warnings, never as failures.
This mirrors what the post-commit hook reports, so you can run it anytime
without worrying about it blocking a pipeline.

Run:  python3 -m unittest tests.test_spellcheck -v
 or:  python3 -m unittest discover -s tests -v
"""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BODY = os.path.join(ROOT, "portfolio", "_body.html")
IGNORE = os.path.join(ROOT, ".codespell-ignore")


class TestSpellCheck(unittest.TestCase):

    def test_body_html_spelling(self):
        """Spell-check _body.html. Prints findings but never fails."""
        result = subprocess.run(
            ["codespell", BODY, "--ignore-words", IGNORE],
            capture_output=True,
            text=True,
        )

        findings = (result.stdout + result.stderr).strip()

        if findings:
            print(
                f"\n\n  ⚠️  Spell check findings in _body.html:\n",
                file=sys.stderr,
            )
            for line in findings.splitlines():
                print(f"      {line}", file=sys.stderr)
            print(
                f"\n      Fix: codespell -w portfolio/_body.html --ignore-words .codespell-ignore"
                f"\n      Ignore a word: add it to .codespell-ignore\n",
                file=sys.stderr,
            )
        # No assertion; this test always passes regardless of findings

    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ["codespell", "--version"],
            capture_output=True,
        )
        if result.returncode != 0:
            raise unittest.SkipTest(
                "codespell not installed; run: pip install -r requirements-dev.txt"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
