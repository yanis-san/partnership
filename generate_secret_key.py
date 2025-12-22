#!/usr/bin/env python3
"""
Script pour générer une SECRET_KEY sécurisée pour Django
Utiliser: python generate_secret_key.py
"""

from django.core.management.utils import get_random_secret_key


def main():
    secret_key = get_random_secret_key()

    print("\n" + "=" * 70)
    print("🔐 NOUVELLE SECRET_KEY GÉNÉRÉE")
    print("=" * 70)
    print(f"\nSECRET_KEY={secret_key}\n")
    print("=" * 70)
    print("Instructions:")
    print("=" * 70)
    print("1. Ouvrez .env.production")
    print("2. Remplacez cette ligne:")
    print("   SECRET_KEY=generate-a-new-key-with-django-core-management-utils")
    print("   par:")
    print(f"   SECRET_KEY={secret_key}")
    print("\n3. Gardez cette clé SECRÈTE!")
    print("4. Ne la commitez JAMAIS dans Git")
    print("5. Utilisez un gestionnaire de secrets en production")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    import django
    import os

    # Configure Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    main()
