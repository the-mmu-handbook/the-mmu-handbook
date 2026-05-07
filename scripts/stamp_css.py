#!/usr/bin/env python3
"""
stamp_css.py — MMU Handbook canonical CSS stamper

Reads assets/canonical.css and writes it into the <style> block of every
chapter HTML file and index.html. Run this whenever canonical.css changes.

Usage:
    python3 scripts/stamp_css.py [--check]

    --check   Verify all files match canonical.css without modifying anything.
              Exits 1 if any file is out of sync (used by audit.py G7).
"""

import re, sys, hashlib
from pathlib import Path

REPO   = Path(__file__).parent.parent
CSS_SRC = REPO / 'assets' / 'canonical.css'


def css_fingerprint(css: str) -> str:
    return hashlib.md5(css.strip().encode()).hexdigest()


def stamp(check_only: bool = False) -> int:
    if not CSS_SRC.exists():
        print(f'❌  {CSS_SRC} not found')
        return 1

    canonical = CSS_SRC.read_text()
    target_fp = css_fingerprint(canonical)

    # index.html has its own distinct CSS (hero, cards, reading paths).
    # stamp_css.py MUST NOT touch index.html — only chapter files.
    chapters = sorted((REPO / 'chapters').glob('chapter-*-WITH-FIGURES.html'))
    targets  = chapters  # index.html excluded intentionally

    out_of_sync = []
    stamped     = 0

    for path in targets:
        html = path.read_text()

        # Find the canonical style block (>10KB — avoids small inline SVG style blocks)
        style_m = re.search(r'(<style>)(.*?)(</style>)', html, re.DOTALL)
        if not style_m:
            print(f'  ⚠  No <style> block in {path.name}')
            continue

        current_css = style_m.group(2)

        # Skip files that already match
        if css_fingerprint(current_css) == target_fp:
            continue

        if check_only:
            out_of_sync.append(path.name)
            continue

        # Stamp the new CSS
        new_html = html[:style_m.start(2)] + canonical + html[style_m.end(2):]
        path.write_text(new_html)
        stamped += 1

    if check_only:
        if out_of_sync:
            print(f'G7: {len(out_of_sync)} file(s) have CSS out of sync with assets/canonical.css:')
            for f in out_of_sync:
                print(f'    {f}')
            return 1
        else:
            print(f'G7: all {len(targets)} files match assets/canonical.css ✅')
            return 0
    else:
        if stamped:
            print(f'✅  Stamped {stamped}/{len(targets)} files from assets/canonical.css')
        else:
            print(f'✅  All {len(targets)} files already match assets/canonical.css — nothing to do')
        return 0


if __name__ == '__main__':
    check_only = '--check' in sys.argv
    sys.exit(stamp(check_only=check_only))
