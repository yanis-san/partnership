# 🚀 GUIDE DE DÉPLOIEMENT EN PRODUCTION

**Version:** 1.0
**Date:** 20/11/2025
**État:** PRÊT POUR DÉPLOIEMENT

---

## 📋 TABLE DES MATIERES

1. [Pré-requis](#pré-requis)
2. [Configuration Production](#configuration-production)
3. [Sécurité](#sécurité)
4. [Déploiement](#déploiement)
5. [Post-Déploiement](#post-déploiement)
6. [Maintenance](#maintenance)
7. [Troubleshooting](#troubleshooting)

---

## 1️⃣ PRÉ-REQUIS

### Avant de Déployer

- [ ] Serveur Linux (Ubuntu 22.04+ ou CentOS 8+) recommandé
- [ ] Domaine configuré avec DNS pointant vers le serveur
- [ ] Certificat SSL/TLS (Let's Encrypt gratuit)
- [ ] Python 3.10+
- [ ] PostgreSQL 13+ (ou MySQL 8+)
- [ ] Nginx ou Apache
- [ ] Git pour les déploiements

### Installation de Base

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3-pip postgresql nginx git

# CentOS
sudo yum install python3.10 pip postgresql nginx git
```

---

## 2️⃣ CONFIGURATION PRODUCTION

### 2.1 Fichier `.env.production`

Créer `/home/app/.env.production`:

```bash
# ===== DJANGO =====
DEBUG=False
SECRET_KEY=<GÉNÉRER_AVEC_django-insecure_...>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# ===== DATABASE =====
# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecole_affiliation
DB_USER=affiliation_user
DB_PASSWORD=<RANDOM_PASSWORD_32_CHARS>
DB_HOST=localhost
DB_PORT=5432

# ===== EMAIL =====
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=<GOOGLE_APP_PASSWORD>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# ===== ADMIN NOTIFICATIONS =====
ADMIN_NAME=Admin Principal
ADMIN_EMAIL=admin@yourdomain.com

# ===== SECURITY =====
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# ===== LOGGING =====
LOG_LEVEL=INFO
LOG_FILE=/var/log/django/app.log
```

#### Générer SECRET_KEY Sécurisée

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Générer Google App Password

1. Aller sur https://myaccount.google.com/apppasswords
2. Sélectionner "Mail" et "Windows Computer" (ou Linux)
3. Copier le mot de passe généré

### 2.2 Configuration Database PostgreSQL

```bash
# Connexion au serveur PostgreSQL
sudo su - postgres
psql

# Créer la base de données
CREATE DATABASE ecole_affiliation;

# Créer l'utilisateur
CREATE USER affiliation_user WITH PASSWORD 'PASSWORD_TRÈS_SÉCURISÉ';

# Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE ecole_affiliation TO affiliation_user;

# Quitter
\q
exit
```

### 2.3 Structure de Répertoires

```
/home/app/
├── ecole_affiliation/          # Repository Django
│   ├── config/
│   ├── partnerships/
│   ├── students/
│   ├── manage.py
│   └── ...
├── venv/                        # Virtual Environment
├── logs/
│   ├── django.log
│   ├── access.log
│   └── error.log
├── media/                       # Uploads (receipts)
│   └── receipts/
├── staticfiles/                 # Fichiers statiques collectés
└── .env.production
```

### 2.4 Installation Application

```bash
# Créer utilisateur app
sudo useradd -m -d /home/app app
sudo usermod -s /bin/bash app
sudo chown -R app:app /home/app

# Se connecter comme app
sudo su - app

# Cloner repository
git clone https://github.com/votre-org/ecole-affiliation.git
cd ecole_affiliation

# Créer virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements-prod.txt

# Créer répertoires
mkdir -p logs media/receipts staticfiles
```

### 2.5 Migrations Database

```bash
# Depuis /home/app/ecole_affiliation/
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Créer superuser
python manage.py createsuperuser
```

---

## 3️⃣ SÉCURITÉ

### 3.1 Configuration Nginx (Reverse Proxy)

Créer `/etc/nginx/sites-available/ecole-affiliation`:

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Limits
    client_max_body_size 10M;
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

    # Static files
    location /static/ {
        alias /home/app/ecole_affiliation/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /home/app/ecole_affiliation/media/;
        expires 7d;
    }

    # Django Application
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Login rate limiting
    location /partnerships/login/ {
        limit_req zone=login_limit burst=10 nodelay;
        proxy_pass http://django;
        proxy_set_header Host $host;
    }
}
```

Activer:
```bash
sudo ln -s /etc/nginx/sites-available/ecole-affiliation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3.2 Certificate SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
sudo systemctl enable certbot.timer
```

### 3.3 Gunicorn Service

Créer `/etc/systemd/system/ecole-affiliation.service`:

```ini
[Unit]
Description=Écol Affiliation Django Application
After=network.target postgresql.service

[Service]
Type=notify
User=app
Group=app
WorkingDirectory=/home/app/ecole_affiliation

Environment="PATH=/home/app/ecole_affiliation/venv/bin"
EnvironmentFile=/home/app/.env.production

ExecStart=/home/app/ecole_affiliation/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    --access-logfile /home/app/ecole_affiliation/logs/access.log \
    --error-logfile /home/app/ecole_affiliation/logs/error.log \
    --log-level info \
    config.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Démarrer:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ecole-affiliation
sudo systemctl start ecole-affiliation
sudo systemctl status ecole-affiliation
```

### 3.4 Permissions & Sécurité Fichiers

```bash
# Database credentials
chmod 600 /home/app/.env.production
sudo chown app:app /home/app/.env.production

# Logs
sudo mkdir -p /var/log/django
sudo chown app:app /var/log/django
sudo chmod 755 /var/log/django

# Media files
chmod 755 /home/app/ecole_affiliation/media
chmod 644 /home/app/ecole_affiliation/media/receipts/*
```

---

## 4️⃣ DÉPLOIEMENT

### 4.1 Initial Deployment

```bash
# 1. SSH au serveur
ssh app@your-server.com

# 2. Activer venv
cd ~/ecole_affiliation
source venv/bin/activate

# 3. Charger .env
export $(cat ../.env.production | xargs)

# 4. Migrations
python manage.py migrate

# 5. Recollect static files
python manage.py collectstatic --no-input

# 6. Redémarrer
sudo systemctl restart ecole-affiliation
```

### 4.2 Déploiements Continus (Git)

```bash
# Créer script de déploiement /home/app/deploy.sh
#!/bin/bash
set -e

cd ~/ecole_affiliation
git fetch origin
git reset --hard origin/main

source venv/bin/activate
export $(cat ../.env.production | xargs)

pip install -r requirements-prod.txt
python manage.py migrate --no-input
python manage.py collectstatic --no-input

sudo systemctl restart ecole-affiliation
echo "✅ Deployment completed at $(date)"
```

Rendre exécutable:
```bash
chmod +x deploy.sh
```

Utiliser avec CI/CD (GitHub Actions):
```yaml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        run: ssh app@server './deploy.sh'
```

---

## 5️⃣ POST-DÉPLOIEMENT

### 5.1 Vérifications

```bash
# 1. Health check
curl -I https://yourdomain.com/

# 2. Admin accessible
curl -I https://yourdomain.com/admin/

# 3. API endpoints OK
curl https://yourdomain.com/api/health/

# 4. SSL certificate valid
curl -v https://yourdomain.com 2>&1 | grep "subject="

# 5. Logs without errors
tail -f /var/log/django/error.log
```

### 5.2 Test Emails

```bash
# Depuis Django shell
python manage.py shell
from students.email_service import *
from partnerships.models import Partner

partner = Partner.objects.first()
send_payment_confirmation_email(partner.payments.first(), None)
```

### 5.3 Monitoring Setup

Installer Sentry (optionnel):

```bash
pip install sentry-sdk

# Dans settings.py:
import sentry_sdk
sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/PROJECT",
    traces_sample_rate=0.1,
    environment="production"
)
```

---

## 6️⃣ MAINTENANCE

### 6.1 Backups Quotidiens

Créer `/home/app/backup.sh`:

```bash
#!/bin/bash

DB_NAME="ecole_affiliation"
DB_USER="affiliation_user"
BACKUP_DIR="/home/app/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/app/ecole_affiliation/media/

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +30 -delete

# Upload to S3 (optionnel)
# aws s3 sync $BACKUP_DIR s3://your-bucket/backups/
```

Créer cron job:
```bash
# Éditer crontab
crontab -e

# Ajouter (quotidien à 2h du matin):
0 2 * * * /home/app/backup.sh >> /home/app/logs/backup.log 2>&1
```

### 6.2 Logs Rotation

```bash
# /etc/logrotate.d/django
/home/app/ecole_affiliation/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 app app
    sharedscripts
    postrotate
        systemctl reload ecole-affiliation > /dev/null 2>&1 || true
    endscript
}
```

### 6.3 Health Checks

Créer endpoint `/api/health/` dans URLs:

```python
# partnerships/views.py
from django.http import JsonResponse

def health_check(request):
    try:
        from django.db import connection
        connection.ensure_connection()
        return JsonResponse({'status': 'healthy', 'database': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

---

## 7️⃣ TROUBLESHOOTING

### Issue: Emails ne s'envoient pas

```bash
# 1. Vérifier configuration
grep EMAIL .env.production

# 2. Tester SMTP
python3 -c "
import smtplib
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('your@email.com', 'app_password')
print('✅ SMTP OK')
s.quit()
"

# 3. Vérifier logs
tail -f /var/log/django/error.log | grep -i email
```

### Issue: Static files 404

```bash
# Recollect static files
python manage.py collectstatic --no-input --clear

# Vérifier ownership
ls -la staticfiles/
sudo chown -R app:app staticfiles/
```

### Issue: Database connection error

```bash
# Tester connexion PostgreSQL
psql -h localhost -U affiliation_user -d ecole_affiliation

# Vérifier credentials dans .env
grep DB_ .env.production
```

### Issue: High CPU/Memory

```bash
# Vérifier processus Gunicorn
ps aux | grep gunicorn

# Augmenter workers dans service:
ExecStart=... --workers 8 ...

# Restart
sudo systemctl restart ecole-affiliation
```

---

## ✅ CHECKLIST FINAL PRE-DÉPLOIEMENT

### CRITIQUE - Doit être configuré

- [ ] SECRET_KEY généré et unique (>50 caractères)
- [ ] DEBUG = False en production
- [ ] ALLOWED_HOSTS configuré avec domaine réel
- [ ] Database PostgreSQL/MySQL configurée
- [ ] Email credentials valides (SMTP)
- [ ] ADMINS tuple configuré (emails admins)
- [ ] SSL/TLS certificate en place
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] Backup strategy en place

### IMPORTANT - À vérifier

- [ ] Migrations appliquées (python manage.py migrate)
- [ ] Static files collectés
- [ ] Superuser créé
- [ ] Logs directory accessible
- [ ] Media directory permissions (755)
- [ ] Database backups fonctionnent
- [ ] Service Gunicorn démarre au boot
- [ ] Nginx reverse proxy configuré
- [ ] Rate limiting activé
- [ ] Security headers présents

### TEST - Avant de passer en production

- [ ] Page d'accueil accessible
- [ ] Admin login fonctionne
- [ ] Inscription étudiant fonctionne
- [ ] Email d'inscription envoyé
- [ ] Login partenaire fonctionne
- [ ] Upload reçu fonctionne
- [ ] Dashboard partenaire accessible
- [ ] Historique paiements visible
- [ ] SSL certificate valide
- [ ] Pas d'erreurs dans les logs

---

**Prêt pour le déploiement! 🚀**

Pour toute question ou issue: consulter `/var/log/django/error.log`
