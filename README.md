# kdange.me Portfolio

Personal portfolio for **Kshitiz Dange (KD)** at [www.kdange.me](https://www.kdange.me).

---

## First-time setup

Run this once after cloning. It configures git hooks and installs dev dependencies:

```bash
./setup.sh
```

`setup.sh` detects your environment and does the right thing:

| Environment | What it does |
|---|---|
| Conda available | Creates the `kd-portfolio` conda env from `environment.yml` |
| No conda | Creates a `.venv` virtual environment via `python3 -m venv` |

After it runs, activate your environment before running tests or the spell checker:

```bash
# conda
conda activate kd-portfolio

# or pip/venv
source .venv/bin/activate
```

After pushing to GitHub for the first time, run this once to configure branch protection and squash-merge-only:

```bash
./setup-github.sh owner/repo   # e.g. ./setup-github.sh kdandank/kdange-me-portfolio
```

Requires the `gh` CLI to be authenticated (`gh auth login`).

---

## Editing content

**All editable content lives in one file:**

```
portfolio/_body.html
```

This is the only file to touch for copy, sections, experience, skills, etc. Both the static site and the WordPress theme read from it.

After editing, rebuild the static entry point:

```bash
python3 portfolio/build.py
```

Then commit normally; the pre-commit hook rebuilds and stages `index.html` automatically.

**Do not edit `index.html` directly.** It is generated and will be overwritten on the next build.

---

## Project structure

```
portfolio/
  _body.html        ← EDIT THIS: all page sections (nav → footer)
  build.py          ← generates index.html from _body.html
  index.html        ← GENERATED: static site entry (GitHub Pages)
  index.php         ← WordPress theme entry (includes _body.html at runtime)
  functions.php     ← WordPress asset enqueuing
  style.css         ← styles (includes WordPress theme header)
  script.js         ← animations and interactivity

tests/
  test_sync.py      ← 9 tests: build system + pre-commit hook scenarios
  test_spellcheck.py← spell check (always passes; prints findings as warnings)

.github/
  workflows/
    deploy.yml      ← push to main: sync check → deploy to GitHub Pages
    pr-checks.yml   ← PR to main: test suite must pass before merge

.githooks/
  pre-commit        ← blocks direct edits to index.html; rebuilds on _body.html changes
  post-commit       ← spell-checks _body.html after every commit (never blocks)

.codespell-ignore   ← allowed words for spell checker (proper names, acronyms)
environment.yml     ← conda environment definition
requirements-dev.txt← pip dev dependencies (codespell)
setup.sh            ← one-time local setup (run after clone)
setup-github.sh     ← one-time GitHub branch protection + squash-merge config
```

---

## Running tests

```bash
python3 -m unittest discover -s tests -v
```

**test_sync.py** (9 tests; these must pass; PR merges are blocked if they fail):
- `_body.html` has all expected section markers
- `index.html` is correctly assembled from `_body.html`
- `index.php` includes `_body.html`
- Editing `_body.html` triggers auto-rebuild of `index.html` (hook scenario 1)
- Staging `index.html` directly is blocked by the hook (hook scenario 2)
- Staging unrelated files passes through silently (hook scenario 3)
- Removing the `_body.html` include from `index.php` is blocked

**test_spellcheck.py** (1 test; always passes; findings are informational):
- Spell-checks `_body.html` and prints any issues to stderr
- Skips automatically if `codespell` is not installed

---

## Local development

```bash
cd portfolio
python3 -m http.server 8080
# open http://localhost:8080
```

---

## Deployment

### GitHub Pages (active)

1. Push to `main`; the workflow runs automatically.
2. First time only: go to **Settings → Pages → Source** and select `GitHub Actions`.
3. Add your custom domain (`kdange.me`) under **Settings → Pages → Custom domain**.
4. Add a `CNAME` DNS record pointing `www.kdange.me` → `<your-github-username>.github.io`.

---

## CI

| Trigger | Workflow | What it does |
|---|---|---|
| PR → `main` | `pr-checks.yml` | Runs 9-test suite; merge blocked until green |
| Push to `main` | `deploy.yml` | Rebuilds + validates sync, then deploys to GitHub Pages |

The `deploy.yml` sync check is a safety net for the rare case the pre-commit hook was bypassed (e.g. `--no-verify`).
