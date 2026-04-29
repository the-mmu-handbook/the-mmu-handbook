#!/usr/bin/env python3
"""
MMU Handbook — PDF Generator
Usage: python3 scripts/generate_pdfs.py [--output DIR]

Generates one PDF per chapter using Playwright/Chromium.
Chapter count is auto-inferred from the chapters/ directory.

Requirements: pip install playwright && playwright install chromium --with-deps
"""

import re, sys, os, argparse
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: pip install playwright && playwright install chromium --with-deps")
    sys.exit(1)

CHAPTERS_DIR = Path(os.environ.get('CHAPTERS_DIR', 'chapters/'))
PRINT_CSS = """
.sb-toggle, #mmu-sidebar, #sb { display: none !important; }
body {
    margin: 0 !important;
    margin-left: 0 !important;
    max-width: none !important;
    font-family: 'IBM Plex Sans', Arial, sans-serif !important;
}
figure { page-break-inside: avoid; }
h2, h3 { page-break-after: avoid; }
"""


def get_chapter_title(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return 'MMU Handbook'


def generate_chapter_pdf(browser, path, output_dir):
    chnum = int(re.search(r'chapter-(\d+)', path.name).group(1))
    html = path.read_text()
    title = get_chapter_title(html)

    page = browser.new_page()
    # Block external resources (fonts, etc.) to avoid network wait
    page.route('**fonts.googleapis.com**', lambda r: r.abort())
    page.route('**fonts.gstatic.com**',    lambda r: r.abort())
    page.route('**google-analytics.com**', lambda r: r.abort())

    page.goto(f'file://{path.resolve()}')
    page.wait_for_load_state('load')

    # Inject print CSS to hide sidebar and reset margins
    page.add_style_tag(content=PRINT_CSS)

    out_path = output_dir / f'chapter-{chnum:02d}.pdf'
    page.pdf(
        path=str(out_path),
        format='A4',
        print_background=True,
        margin={'top': '18mm', 'bottom': '20mm', 'left': '20mm', 'right': '20mm'},
        display_header_footer=True,
        header_template=(
            f'<div style="font-size:9px;color:#888;width:100%;'
            f'padding:5px 20px;text-align:left;">'
            f'MMU Handbook &nbsp;|&nbsp; {title}</div>'
        ),
        footer_template=(
            '<div style="font-size:9px;color:#888;width:100%;'
            'padding:5px 20px;text-align:center;">'
            '<span class="pageNumber"></span> / <span class="totalPages"></span>'
            '</div>'
        ),
    )
    size_kb = os.path.getsize(out_path) // 1024
    page.close()
    return size_kb


def main():
    parser = argparse.ArgumentParser(description='Generate MMU Handbook PDFs')
    parser.add_argument('--output', default='pdfs/', help='Output directory')
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    chapter_files = sorted(CHAPTERS_DIR.glob('chapter-*-WITH-FIGURES.html'))
    N = len(chapter_files)  # auto-inferred

    if N == 0:
        print(f"ERROR: No chapter files found in {CHAPTERS_DIR}")
        sys.exit(1)

    print(f"MMU Handbook — PDF Generator")
    print(f"Chapters: {N}  (auto-inferred)")
    print(f"Output:   {output_dir.resolve()}")
    print('=' * 60)

    total_kb = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for i, path in enumerate(chapter_files, 1):
            chnum = int(re.search(r'chapter-(\d+)', path.name).group(1))
            print(f"  [{i:2d}/{N}] Ch{chnum:02d} ... ", end='', flush=True)
            try:
                kb = generate_chapter_pdf(browser, path, output_dir)
                total_kb += kb
                print(f"{kb} KB ✓")
            except Exception as e:
                print(f"FAILED: {e}")
        browser.close()

    print('=' * 60)
    print(f"Done: {N} PDFs, {total_kb // 1024:.1f} MB total")
    print(f"Output: {output_dir.resolve()}")


if __name__ == '__main__':
    main()
