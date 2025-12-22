#!/usr/bin/env python3
"""
Script pour télécharger les bibliothèques JavaScript essentielles
Utiliser: python download_js_libraries.py
"""

import os
import urllib.request
from pathlib import Path

# URLs des dernières versions
LIBRARIES = {
    "alpine.js": {
        "url": "https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js",
        "path": "static/js/alpine.min.js",
    },
    "htmx.js": {
        "url": "https://cdn.jsdelivr.net/npm/htmx.org@1.9.12",
        "path": "static/js/htmx.min.js",
    },
}


def download_file(url, filepath):
    """Télécharge un fichier et l'affiche"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    print(f"📥 Téléchargement: {os.path.basename(filepath)}")
    print(f"   URL: {url}")

    try:
        urllib.request.urlretrieve(url, filepath)
        file_size = os.path.getsize(filepath) / 1024  # En KB
        print(f"   ✅ Téléchargé: {file_size:.1f} KB")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def main():
    print("=" * 60)
    print("Téléchargement des bibliothèques JavaScript")
    print("=" * 60)

    success_count = 0
    for name, config in LIBRARIES.items():
        if download_file(config["url"], config["path"]):
            success_count += 1

    print("\n" + "=" * 60)
    print(
        f"Résultat: {success_count}/{len(LIBRARIES)} fichiers téléchargés ✅"
    )
    print("=" * 60)
    print("\n📝 Mettez à jour base.html avec:")
    print("   - {% static 'js/alpine.min.js' %}")
    print("   - {% static 'js/htmx.min.js' %}")


if __name__ == "__main__":
    main()
