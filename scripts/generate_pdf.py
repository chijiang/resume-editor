#!/usr/bin/env python3
"""
Convert HTML resume to PDF format.
Uses browser-based rendering for high-quality output.
"""

import sys
import argparse
from pathlib import Path

# Try to import pdfkit (wkhtmltopdf wrapper) for simplicity
try:
    import pdfkit
    HAS_PDFKIT = True
except ImportError:
    HAS_PDFKIT = False

# Fallback: use Playwright for modern rendering
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def convert_with_pdfkit(html_path, output_path):
    """Convert HTML to PDF using pdfkit/wkhtmltopdf."""
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None
    }

    pdfkit.from_file(html_path, output_path, options=options)
    return True


def convert_with_playwright(html_path, output_path):
    """Convert HTML to PDF using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load HTML file
        html_url = f"file://{Path(html_path).absolute()}"
        page.goto(html_url, wait_until="networkidle")

        # Generate PDF
        page.pdf(
            path=output_path,
            format="A4",
            margin={
                "top": "0.75in",
                "right": "0.75in",
                "bottom": "0.75in",
                "left": "0.75in"
            },
            print_background=True
        )

        browser.close()
    return True


def main():
    parser = argparse.ArgumentParser(description='Convert HTML resume to PDF')
    parser.add_argument('html_file', help='Path to HTML resume file')
    parser.add_argument('output_pdf', help='Path to output PDF file')

    args = parser.parse_args()

    if not Path(args.html_file).exists():
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    print(f"Converting {args.html_file} to PDF...")

    success = False

    # Try pdfkit first (faster, simpler)
    if HAS_PDFKIT:
        try:
            print("Using pdfkit (wkhtmltopdf)...")
            success = convert_with_pdfkit(args.html_file, args.output_pdf)
        except Exception as e:
            print(f"pdfkit failed: {e}")
            success = False

    # Fallback to Playwright (better rendering)
    if not success and HAS_PLAYWRIGHT:
        try:
            print("Using Playwright (Chromium)...")
            success = convert_with_playwright(args.html_file, args.output_pdf)
        except Exception as e:
            print(f"Playwright failed: {e}")
            success = False

    if not success:
        print("Error: No PDF conversion tool available.")
        print("Install one of:")
        print("  - pdfkit: pip install pdfkit && brew install wkhtmltopdf")
        print("  - playwright: pip install playwright && playwright install chromium")
        sys.exit(1)

    print(f"PDF generated: {args.output_pdf}")


if __name__ == "__main__":
    main()
