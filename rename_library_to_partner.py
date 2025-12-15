#!/usr/bin/env python
"""Script pour renommer tous les références 'library' en 'partner' dans le code"""
import os
import re

# Files to process
FILES = [
    'partnerships/views.py',
    'partnerships/admin.py',
    'partnerships/models_audit.py',
    'students/views.py',
    'students/forms.py',
]

# Replacement rules (regex patterns and replacements)
REPLACEMENTS = [
    # Python code - class names and model references
    (r'\bLibrary\b(?!.*Lib)', 'Partner'),
    (r'\blibrary\b', 'partner'),
    (r'\.library(?!_)', '.partner'),
    (r'\[\'library\'\]', "['partner']"),
    (r'\["library"\]', '["partner"]'),
]

def process_file(filepath):
    """Process a single file"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Apply replacements
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Processed: {filepath}")
        return True
    else:
        print(f"⏭️  No changes: {filepath}")
        return False

# Process all files
if __name__ == '__main__':
    count = 0
    for filepath in FILES:
        if process_file(filepath):
            count += 1
    print(f"\n✅ Processed {count}/{len(FILES)} files with changes")
