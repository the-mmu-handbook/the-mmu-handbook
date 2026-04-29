#!/usr/bin/env python3
"""
MMU Handbook — Browser Check Script
Usage: python3 scripts/browser_check.py [chapters_dir]

Runs Playwright/Chromium checks against all chapter HTML files.
Must be run after audit.py passes — this is gate 2.

Checks (all auto-inferred chapter count):
  B1  Print CSS: sidebar hidden + body margin reset
  B2  Print PDF: generated and non-empty (>100 KB)
  B3  Active chapter highlight correct (data-c == chapter number)
  B4  TOC anchor links all resolve
  B5  Sidebar anchor links all resolve
  B6  figcaption computed text-align == left
  B7  Figure IDs sequential (DOM order)
  B8  No JS console errors
  B9  Cross-chapter navigation: click Ch1→ChN, verify active updates
  B10 index.html card count == N

Requires: pip install playwright && playwright install chromium --with-deps
"""

import re, sys, json, os, time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium --with-deps")
    sys.exit(1)


CHAPTERS_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/claude/repo/chapters/')
REPO_DIR     = CHAPTERS_DIR.parent

PDF_MIN_KB   = 100   # minimum PDF size to count as non-empty


def chapter_files():
    return sorted(CHAPTERS_DIR.glob('chapter-*-WITH-FIGURES.html'))


def block_fonts(page):
    """Block Google Fonts to avoid network wait."""
    page.route('**fonts.googleapis.com**', lambda r: r.abort())
    page.route('**fonts.gstatic.com**',    lambda r: r.abort())


def load_chapter(browser, path):
    page = browser.new_page()
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('pageerror', lambda err: errors.append(str(err)))
    block_fonts(page)
    page.goto(f'file://{path.resolve()}')
    page.wait_for_load_state('load')
    return page, errors


def check_chapter(browser, path, N, pdf_dir):
    chnum = int(re.search(r'chapter-(\d+)', path.name).group(1))
    issues = []

    page, js_errors = load_chapter(browser, path)

    try:
        # B1: Print CSS rules present in stylesheet (emulate_media computed style
        #     is unreliable in Playwright; verify rules exist in CSS source instead)
        print_check = page.evaluate('''() => {
            let hasSidebarHide = false, hasMarginReset = false;
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.conditionText && rule.conditionText.includes("print")) {
                            const t = rule.cssText;
                            if ((t.includes("mmu-sidebar") || t.includes("#sb"))
                                && t.includes("display") && t.includes("none"))
                                hasSidebarHide = true;
                            if (t.includes("body") && t.includes("margin-left")
                                && t.includes("0"))
                                hasMarginReset = true;
                        }
                    }
                } catch(e) {}
            }
            return { hasSidebarHide, hasMarginReset };
        }''')
        if not print_check['hasSidebarHide']:
            issues.append("B1: @media print missing sidebar display:none rule")
        if not print_check['hasMarginReset']:
            issues.append("B1: @media print missing body margin-left:0 reset rule")

        # B2: Print PDF
        pdf_path = pdf_dir / f'chapter-{chnum:02d}.pdf'
        page.pdf(path=str(pdf_path), format='A4',
                 margin={'top':'18mm','bottom':'18mm','left':'20mm','right':'20mm'})
        pdf_kb = os.path.getsize(pdf_path) // 1024
        if pdf_kb < PDF_MIN_KB:
            issues.append(f"B2: PDF too small ({pdf_kb} KB, expected >{PDF_MIN_KB} KB)")

        # B3: Active chapter highlight
        active = page.evaluate(f'''() => {{
            const block = document.querySelector(".sb-ch.active");
            const active_num = block ? parseInt(block.getAttribute("data-c")) : null;
            return {{ active_num, correct: active_num === {chnum} }};
        }}''')
        if not active['correct']:
            issues.append(f"B3: Active chapter wrong — got {active['active_num']}, expected {chnum}")

        # B4: TOC broken anchors
        toc_broken = page.evaluate('''() =>
            [...document.querySelectorAll('#TOC a[href^="#"]')]
            .filter(a => !document.getElementById(a.getAttribute('href').slice(1)))
            .map(a => a.getAttribute('href'))
        ''')
        if toc_broken:
            issues.append(f"B4: Broken TOC anchors: {toc_broken[:3]}")

        # B5: Sidebar broken anchors
        sidebar_broken = page.evaluate('''() =>
            [...document.querySelectorAll('nav a[href^="#"]')]
            .filter(a => !document.getElementById(a.getAttribute('href').slice(1)))
            .map(a => a.getAttribute('href'))
        ''')
        if sidebar_broken:
            issues.append(f"B5: Broken sidebar anchors: {sidebar_broken[:3]}")

        # B6: figcaption computed text-align
        bad_align = page.evaluate('''() =>
            [...document.querySelectorAll('figcaption')]
            .filter(c => getComputedStyle(c).textAlign !== 'left').length
        ''')
        if bad_align:
            issues.append(f"B6: {bad_align} figcaption(s) not left-aligned (computed style)")

        # B7: Figure IDs sequential
        fig_ids = page.evaluate(f'''() =>
            [...document.querySelectorAll('figure[id^="fig-{chnum}-"]')]
            .map(f => parseInt(f.id.split('-').pop()))
        ''')
        if fig_ids:
            expected = list(range(1, len(fig_ids) + 1))
            if fig_ids != expected:
                issues.append(f"B7: Figure IDs not sequential — got {fig_ids[:6]}")

        # B8: JS errors (filter out blocked external resources — fonts etc.)
        real_errors = [e for e in js_errors
                       if not any(s in e for s in [
                           'ERR_FAILED', 'net::', 'fonts.googleapis', 'fonts.gstatic',
                           'Failed to load resource'
                       ])]
        if real_errors:
            issues.append(f"B8: JS errors: {real_errors[:2]}")

    finally:
        page.close()

    return chnum, issues


def check_cross_navigation(browser, chapter_files):
    """B9: Navigate from first chapter to last via sidebar click."""
    issues = []
    first = chapter_files[0]
    last  = chapter_files[-1]
    last_num = int(re.search(r'chapter-(\d+)', last.name).group(1))

    page, _ = load_chapter(browser, first)
    try:
        link = page.locator(f'a[href*="{last.name}"]').first
        if link.count() == 0:
            issues.append(f"B9: Link to {last.name} not found in sidebar of {first.name}")
        else:
            link.click()
            page.wait_for_load_state('load')
            active_num = page.evaluate('''() => {
                const b = document.querySelector(".sb-ch.active");
                return b ? parseInt(b.getAttribute("data-c")) : null;
            }''')
            landed = page.evaluate('()=>location.pathname.split("/").pop()')
            if last.name not in landed:
                issues.append(f"B9: Navigation landed on {landed!r}, expected {last.name}")
            if active_num != last_num:
                issues.append(f"B9: Active not updated after nav — got {active_num}, expected {last_num}")
    finally:
        page.close()

    return issues


def check_index(browser, N):
    """B10: index.html card count == N."""
    issues = []
    index_path = REPO_DIR / 'index.html'
    if not index_path.exists():
        return ["B10: index.html not found"]

    page = browser.new_page()
    block_fonts(page)
    page.goto(f'file://{index_path.resolve()}')
    page.wait_for_load_state('load')

    try:
        # Count chapter cards — look for chapter links
        card_count = page.evaluate('''() =>
            document.querySelectorAll('a[href*="chapter-"][href*=".html"]').length
        ''')
        # Deduplicate (each chapter link might appear once)
        unique_chapters = page.evaluate('''() => {
            const links = [...document.querySelectorAll('a[href*="chapter-"][href*=".html"]')];
            return new Set(links.map(a => a.getAttribute('href').match(/chapter-(\d+)/)?.[1]))
                   .size;
        }''')
        if unique_chapters != N:
            issues.append(f"B10: index.html shows {unique_chapters} chapter links, expected {N}")
    finally:
        page.close()

    return issues


def main():
    files = chapter_files()
    if not files:
        print(f"ERROR: No chapter files in {CHAPTERS_DIR}"); sys.exit(1)

    N = len(files)
    pdf_dir = REPO_DIR / '_pdf_check'
    pdf_dir.mkdir(exist_ok=True)

    print("MMU Handbook — Browser Check (Playwright)")
    print(f"Chapters:  {N}  (auto-inferred)")
    print(f"Chromium:  headless")
    print('=' * 72)

    total_issues = clean_count = 0
    rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Per-chapter checks (B1–B8)
        for path in files:
            chnum, issues = check_chapter(browser, path, N, pdf_dir)
            rows.append((chnum, issues))
            status = '✅' if not issues else '❌'
            print(f"\n{status}  Chapter {chnum:02d}")
            if not issues:
                print("     All browser checks passed.")
            for i in issues:
                print(f"     ⚠  {i}")
            if not issues: clean_count += 1
            else:          total_issues += len(issues)

        # B9: Cross-chapter navigation
        nav_issues = check_cross_navigation(browser, files)
        print(f"\n{'✅' if not nav_issues else '❌'}  Cross-chapter navigation (B9)")
        for i in nav_issues:
            print(f"     ⚠  {i}")
            total_issues += 1

        # B10: index.html
        idx_issues = check_index(browser, N)
        print(f"\n{'✅' if not idx_issues else '❌'}  index.html (B10)")
        for i in idx_issues:
            print(f"     ⚠  {i}")
            total_issues += 1

        browser.close()

    # Cleanup PDFs
    import shutil
    shutil.rmtree(pdf_dir)

    print()
    print('=' * 72)
    print(f"SUMMARY: {clean_count}/{N} chapters clean, {total_issues} total issues")
    print()

    if '--json' in sys.argv:
        print(json.dumps([{'chapter': c, 'clean': not i, 'issues': i} for c, i in rows], indent=2))

    return 0 if total_issues == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
