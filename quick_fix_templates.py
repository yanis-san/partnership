#!/usr/bin/env python
import os
import re

# Les fichiers à modifier
files = [
    "partnerships/templates/partnerships/partner-login.html",
    "partnerships/templates/partnerships/partner-dashboard-public.html",
    "partnerships/templates/partnerships/partner-dashboard-personal.html",
    "partnerships/templates/partnerships/partner-payment-history.html",
    "students/templates/students/partner-dashboard.html",
]

# Les remplacements à faire
replacements = [
    (r"{{ library\.", "{{ partner."),
    (r"{{ library }}", "{{ partner }}"),
    (r"'library-", "'partner-"),
    (r"'library'", "'partner'"),
    (r"library-dashboard", "partner-dashboard"),
    (r"library-login", "partner-login"),
    (r"library-payment", "partner-payment"),
    (r"Connexion Librairie", "Connexion Partenaire"),
    (r"Dashboard - \{\{ partner.name \}\}", "Dashboard - {{ partner.name }}"),
    (r"library_", "partner_"),
]

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[DONE] {filepath}")
        else:
            print(f"[SKIP] {filepath} (no changes)")
    else:
        print(f"[ERROR] {filepath} not found")

print("\n[SUCCESS] Done!")
