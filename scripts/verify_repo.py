#!/usr/bin/env python3
"""
Repository verification script to ensure documentation completeness,
link validity, and structural consistency across all app ideas.
"""

import os
import re
import sys

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root_dir)

    print("=== Starting Repository Verification ===")
    errors = []

    # 1. Identify all app directories
    app_dirs = sorted([d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d != 'scripts'])
    print(f"Total application directories found: {len(app_dirs)}")

    # 2. Verify each directory has README.md with core standard headers
    required_headers = ['## 概要', '## 主な機能', '## ロードマップ']
    for d in app_dirs:
        readme_path = os.path.join(d, 'README.md')
        if not os.path.exists(readme_path):
            errors.append(f"Missing README.md in directory: {d}")
            continue

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for header in required_headers:
            if header not in content:
                errors.append(f"{d}/README.md is missing section header: '{header}'")

    # 3. Check README.md and INDEX.md links and coverage
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()

    with open('INDEX.md', 'r', encoding='utf-8') as f:
        index_content = f.read()

    for d in app_dirs:
        if f"./{d}/" not in readme_content:
            errors.append(f"Directory '{d}' is not linked in root README.md")
        if f"./{d}/" not in index_content:
            errors.append(f"Directory '{d}' is not linked in root INDEX.md")

    # 4. Check INDEX.md sorting
    index_dirs = []
    for line in index_content.splitlines():
        match = re.search(r'\(\./([^/]+)/\)', line)
        if match:
            index_dirs.append(match.group(1))

    if index_dirs != sorted(index_dirs):
        errors.append("INDEX.md is not sorted alphabetically by directory name")

    # 5. Check for broken links in root README.md and INDEX.md
    for label, text in [('INDEX.md', index_content), ('README.md', readme_content)]:
        links = re.findall(r'\[(.*?)\]\((.*?)\)', text)
        for title, link in links:
            if link.startswith('./') and not os.path.exists(link):
                errors.append(f"Broken link in {label}: [{title}]({link})")

    if errors:
        print(f"\nVerification FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print("=== All Repository Verification Checks Passed Successfully! ===")

if __name__ == '__main__':
    main()
