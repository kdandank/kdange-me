#!/usr/bin/env bash
# One-time setup after cloning.
# Run: ./setup.sh

set -euo pipefail

# 1. Activate committed git hooks
git config core.hooksPath .githooks
echo "✅  Git hooks configured (pre-commit + post-commit)."

# 2. Install dev dependencies
echo ""
if command -v conda &>/dev/null; then
  echo "   Conda detected. Creating environment from environment.yml..."
  conda env create -f environment.yml --quiet 2>/dev/null \
    || conda env update -f environment.yml --quiet
  echo "✅  Conda environment 'kd-portfolio' ready."
  echo "   Activate with: conda activate kd-portfolio"
elif python3 -m venv .venv >/dev/null 2>&1; then
  .venv/bin/pip install -r requirements-dev.txt -q
  echo "✅  Dev dependencies installed in .venv/"
  echo "   Activate with: source .venv/bin/activate"
else
  rm -rf .venv 2>/dev/null || true
  echo "⚠️  Could not create a virtual environment automatically."
  echo "   On Debian/Ubuntu, fix with: sudo apt install python3-venv python3-full"
  echo "   Then re-run ./setup.sh"
  echo ""
  echo "   Or install dependencies globally:"
  echo "     pip install -r requirements-dev.txt"
fi

echo ""
echo "All done. See README.md for next steps."
