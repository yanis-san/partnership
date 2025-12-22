#!/usr/bin/env python
"""
Générateur d'UUID pour URL Admin sécurisée
Plateforme d'Affiliation Torii
"""

import uuid
import secrets
import string
from pathlib import Path


def generate_admin_uuid():
    """Générer un UUID pour l'URL admin."""
    admin_id = uuid.uuid4()
    return f"admin-{admin_id}/"


def generate_secret_key(length=50):
    """Générer une clé secrète Django."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    secret = "".join(secrets.choice(chars) for _ in range(length))
    return secret


def setup_env_production():
    """Configuration interactive pour .env.prod"""
    print("=" * 60)
    print("🔐 Configuration Production - Plateforme Torii")
    print("=" * 60)
    print()

    # Générer l'admin URL
    print("1️⃣  ADMIN URL (sécurisé)")
    print("-" * 40)
    admin_url = generate_admin_uuid()
    print(f"✅ URL Admin générée: {admin_url}")
    print(f"   Ajouter dans .env.prod: ADMIN_URL={admin_url}")
    print()

    # Générer la clé secrète
    print("2️⃣  SECRET KEY (Django)")
    print("-" * 40)
    secret_key = generate_secret_key()
    print(f"✅ SECRET_KEY générée: {secret_key}")
    print(f"   Ajouter dans .env.prod: SECRET_KEY={secret_key}")
    print()

    # Demander les configs de l'utilisateur
    print("3️⃣  CONFIGURATION DE L'UTILISATEUR")
    print("-" * 40)

    config = {
        "ADMIN_URL": admin_url,
        "SECRET_KEY": secret_key,
    }

    domain = input("   📍 Domain (ex: yourdomain.com): ").strip()
    if domain:
        config["ALLOWED_HOSTS"] = f"{domain},www.{domain}"
    else:
        config["ALLOWED_HOSTS"] = "yourdomain.com,www.yourdomain.com"

    db_type = input("   🗄️  Type de BD (postgresql/sqlite): ").strip().lower()
    if db_type == "postgresql":
        db_user = input("      Utilisateur DB: ").strip()
        db_pass = input("      Mot de passe DB: ").strip()
        db_host = input("      Hôte DB (ex: localhost): ").strip()
        db_port = input("      Port DB (défaut: 5432): ").strip() or "5432"
        db_name = input("      Nom de la BD: ").strip()
        config["DATABASE_URL"] = (
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
    else:
        config["DATABASE_URL"] = "sqlite:///db.sqlite3"

    email = input("   📧 Email (pour notifications): ").strip()
    if email:
        config["ADMIN_EMAIL"] = email

    # Générer le fichier
    print()
    print("4️⃣  GÉNÉRATION DU FICHIER")
    print("-" * 40)

    env_content = f"""# ============================================
# PRODUCTION ENVIRONMENT CONFIGURATION
# Plateforme d'Affiliation Torii
# ============================================
# IMPORTANT: Ne jamais commiter ce fichier dans Git!
# Ajouter .env.prod dans .gitignore

# ============================================
# DJANGO CONFIGURATION
# ============================================
DEBUG=False
SECRET_KEY={config.get('SECRET_KEY')}
ALLOWED_HOSTS={config.get('ALLOWED_HOSTS', 'yourdomain.com,www.yourdomain.com')}

# ============================================
# ADMIN URL (UUID pour sécurité)
# ============================================
ADMIN_URL={config.get('ADMIN_URL')}

# ============================================
# BASE DE DONNÉES
# ============================================
DATABASE_URL={config.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/torii_db')}

# ============================================
# EMAIL CONFIGURATION
# ============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@instituttorii.com

# ============================================
# ADMIN NOTIFICATIONS
# ============================================
ADMIN_EMAIL={config.get('ADMIN_EMAIL', 'admin@yourdomain.com')}

# ============================================
# SÉCURITÉ
# ============================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
CSRF_COOKIE_SAMESITE=Lax
SESSION_COOKIE_AGE=86400

# ============================================
# WHITENOISE & STATIQUES
# ============================================
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles/
WHITENOISE_COMPRESS=True
WHITENOISE_AUTOREFRESH=False
WHITENOISE_MAX_AGE=31536000

# ============================================
# MEDIA FILES
# ============================================
MEDIA_URL=/media/
MEDIA_ROOT=/app/media/

# ============================================
# TIMEZONE
# ============================================
LANGUAGE_CODE=fr-fr
TIME_ZONE=Africa/Algiers

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO

# ============================================
# SENTRY (optionnel)
# ============================================
# SENTRY_DSN=https://your-key@sentry.io/project-id
"""

    env_path = Path(".env.prod")
    if env_path.exists():
        backup = Path(".env.prod.backup")
        env_path.rename(backup)
        print(f"✅ Ancien .env.prod sauvegardé en {backup}")

    with open(env_path, "w") as f:
        f.write(env_content)

    print(f"✅ Fichier .env.prod créé avec succès!")
    print()

    # Afficher les étapes suivantes
    print("5️⃣  PROCHAINES ÉTAPES")
    print("-" * 40)
    print("   1. Éditer .env.prod avec vos vraies valeurs")
    print(f"      - EMAIL_HOST_USER: votre email Gmail")
    print(f"      - EMAIL_HOST_PASSWORD: votre app password")
    print(f"      - DATABASE_URL: votre vrai URL de BD")
    print()
    print("   2. Ajouter .env.prod à .gitignore:")
    print("      echo '.env.prod' >> .gitignore")
    print()
    print("   3. Charger les variables d'environnement:")
    print("      export $(cat .env.prod | xargs)")
    print()
    print("   4. Appliquer les migrations:")
    print("      python manage.py migrate")
    print()
    print("   5. Collecter les statiques:")
    print("      python manage.py collectstatic --no-input")
    print()
    print("   6. Déployer!")
    print()
    print("=" * 60)
    print(f"📍 Admin accessible à: https://{domain}/{admin_url}")
    print("=" * 60)


if __name__ == "__main__":
    setup_env_production()
