#!/usr/bin/env python3
"""
Generates index.html from the HTML wrapper defined here + _body.html.

  Edit content : portfolio/_body.html
  Edit HTML wrapper: the HEAD / FOOT strings below
  Rebuild      : python3 portfolio/build.py   (or just commit _body.html)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

HEAD = """\
<!DOCTYPE html>
<!-- GENERATED: do not edit directly. Edit _body.html, then run: python3 build.py -->
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kshitiz Dange | Product Leader</title>
  <meta name="description" content="Kshitiz Dange (KD), Product Leader specializing in Platform Products and HPC. Open to remote, Boston, and Bay Area opportunities." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="icon" type="image/png" href="assets/images/favicon.png" />
  <link rel="stylesheet" href="style.css" />
</head>
<body>
"""

FOOT = """\
  <script src="script.js"></script>
</body>
</html>
"""


def build():
    body_path = os.path.join(HERE, "_body.html")
    out_path = os.path.join(HERE, "index.html")

    if not os.path.exists(body_path):
        print(f"ERROR: {body_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(body_path) as f:
        body = f.read()

    result = HEAD + body + FOOT

    # No-op if nothing changed (keeps mtime stable)
    if os.path.exists(out_path):
        with open(out_path) as f:
            if f.read() == result:
                print("✓  index.html already up to date.")
                return

    with open(out_path, "w") as f:
        f.write(result)
    print("✅  index.html built from _body.html.")


if __name__ == "__main__":
    build()
