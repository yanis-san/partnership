#!/usr/bin/env python
import os
import re
import glob

# Find all HTML template files with 'library' in the name or content
template_dirs = [
    "partnerships/templates/partnerships",
    "students/templates/students"
]

replacements = [
    (r"{{ library\.", "{{ partner."),
    (r"{{ library }}", "{{ partner }}"),
    (r"'library-", "'partner-"),
    (r"'library'", "'partner'"),
    (r"library-dashboard", "partner-dashboard"),
    (r"library-login", "partner-login"),
    (r"library-payment", "partner-payment"),
    (r"Connexion Librairie", "Connexion Partenaire"),
    (r"library_", "partner_"),
    (r"Tableau de Bord - ", "Tableau de Bord - "),
]

files_processed = 0
files_modified = 0

for template_dir in template_dirs:
    if not os.path.exists(template_dir):
        continue

    for filepath in glob.glob(os.path.join(template_dir, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Only process files that contain 'library' or have 'library' in the name
        if 'library' not in content and 'library' not in filepath:
            continue

        original_content = content

        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[UPDATED] {filepath}")
            files_modified += 1

        files_processed += 1

print(f"\n[SUMMARY] Processed {files_processed} files, modified {files_modified}")
