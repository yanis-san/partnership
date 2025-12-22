# 📦 Guide d'Installation Production - Plateforme Torii

## 1️⃣ Configuration de l'Environnement Production

### Étape 1: Générer une clé secrète Django

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copier et garder cette clé précieusement!
```

### Étape 2: Générer un UUID pour l'URL Admin

```bash
python -c "import uuid; print(uuid.uuid4())"
# Exemple: a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
```

### Étape 3: Créer le fichier `.env.prod`

Copier le fichier `.env.prod` fourni et remplir les valeurs:

```env
SECRET_KEY=<clé-secrète-générée>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ADMIN_URL=admin-<uuid-généré>/
DATABASE_URL=postgresql://user:password@host:5432/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
ADMIN_EMAIL=admin@yourdomain.com
```

### Étape 4: Charger les variables d'environnement

```bash
# Linux/Mac
export $(cat .env.prod | xargs)

# Windows PowerShell
Get-Content .env.prod | ForEach-Object {
    if ($_ -notmatch "^#" -and $_.Trim()) {
        $key, $value = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($key, $value)
    }
}
```

---

## 2️⃣ Base de Données Production

### Option A: PostgreSQL (Recommandé)

```bash
# Installation
sudo apt-get install postgresql postgresql-contrib

# Créer utilisateur et base
sudo -u postgres psql
CREATE USER torii_user WITH PASSWORD 'your-strong-password';
CREATE DATABASE torii_db OWNER torii_user;
ALTER ROLE torii_user SET client_encoding TO 'utf8';
ALTER ROLE torii_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE torii_user SET default_transaction_deferrable TO on;
ALTER ROLE torii_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE torii_db TO torii_user;
\q
```

### Option B: Heroku PostgreSQL

```bash
heroku addons:create heroku-postgresql:standard-0
# Le DATABASE_URL est automatiquement défini
```

### Appliquer les migrations

```bash
python manage.py migrate --settings=config.settings
```

---

## 3️⃣ Fichiers Statiques & WhiteNoise

### Collecter les fichiers statiques

```bash
python manage.py collectstatic --no-input
```

Cela va:

- Copier tous les fichiers statiques dans `/staticfiles/`
- Créer une version compressée (Gzip/Brotli)
- Générer un fichier de manifest avec hash des fichiers
- Cela se fait avec WhiteNoise automatiquement

### Vérifier la structure

```
staticfiles/
├── admin/
├── css/
├── js/
│   ├── alpine.min.js
│   ├── htmx.min.js
│   └── ...
└── staticfiles.json  # Manifest généré
```

---

## 4️⃣ Déploiement avec Gunicorn

### Installer dépendances

```bash
pip install -r requirements.txt
```

### Lancer le serveur

```bash
# Commande simple
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Avec configuration de performance
gunicorn -c gunicorn_config.py config.wsgi:application

# En arrière-plan avec supervisor
sudo systemctl restart gunicorn  # Après configuration de /etc/systemd/system/gunicorn.service
```

---

## 5️⃣ Configuration Nginx (Production)

### Créer `/etc/nginx/sites-available/torii`

```nginx
upstream gunicorn {
    server unix:/run/gunicorn.sock;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;  # Redirect to HTTPS
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Compression
    gzip on;
    gzip_types text/plain text/css text/javascript application/json;

    # Client max upload size
    client_max_body_size 10M;

    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files (WhiteNoise gère ceci, mais on peut le mettre en cache Nginx)
    location /static/ {
        alias /app/staticfiles/;
        expires 365d;
        add_header Cache-Control "public, immutable";
        add_header X-Served-By "WhiteNoise";
    }

    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Logs
    access_log /var/log/nginx/torii_access.log;
    error_log /var/log/nginx/torii_error.log;
}
```

### Activer le site

```bash
sudo ln -s /etc/nginx/sites-available/torii /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 6️⃣ SSL/HTTPS avec Let's Encrypt

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Générer certificat
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Renouvellement automatique (cron)
sudo certbot renew --quiet
```

---

## 7️⃣ Email Configuration

### Gmail (avec app password)

1. Activer 2FA sur le compte Google
2. Générer un "App Password" pour Gmail
3. Ajouter dans `.env.prod`:
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # App password
   ```

### SendGrid (alternative)

```bash
pip install django-sendgrid-v5
```

```env
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=SG.xxxxxxxxxxxx
```

---

## 8️⃣ Monitoring & Logs

### Logs Gunicorn

```bash
sudo tail -f /var/log/gunicorn.log
```

### Logs Django

```bash
sudo tail -f /var/log/django/django.log
```

### Logs Nginx

```bash
sudo tail -f /var/log/nginx/torii_access.log
sudo tail -f /var/log/nginx/torii_error.log
```

### Sentry pour error tracking (optionnel)

```bash
pip install sentry-sdk
```

```python
# Dans settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

---

## 9️⃣ Checklist de Sécurité

- [ ] `DEBUG = False` dans settings.py
- [ ] `SECRET_KEY` changée et complexe
- [ ] `ALLOWED_HOSTS` configuré correctement
- [ ] `ADMIN_URL` en UUID (pas "/admin/")
- [ ] HTTPS/SSL activé
- [ ] Cookies sécurisés (SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE)
- [ ] CSP headers configurés
- [ ] Email notifications pour les administrateurs
- [ ] Database backups programmés
- [ ] Rate limiting activé
- [ ] Logging configuré
- [ ] `.env.prod` dans `.gitignore`
- [ ] Monitoring/alertes en place
- [ ] Certificats SSL renouvelés régulièrement

---

## 🔟 Dépannage

### Statiques non servies

```bash
# Recollecter
python manage.py collectstatic --clear --no-input

# Vérifier WhiteNoise
python manage.py runserver --wsgi wsgi.WhiteNoiseWSGI
```

### Admin inaccessible

```bash
# Vérifier l'URL dans settings
echo $ADMIN_URL

# Ou dans Django
python manage.py shell
>>> import os; print(os.getenv('ADMIN_URL', 'admin/'))
```

### Database connection error

```bash
# Tester la connexion
psql $DATABASE_URL

# Vérifier les variables
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
```

### Email not sending

```bash
# Tester l'envoi
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message test', 'from@example.com', ['to@example.com'])
1  # Si 1, succès
```

---

## 📞 Support

Pour toute question ou problème:

- Consulter les logs
- Vérifier les variables d'environnement
- S'assurer que toutes les migrations sont appliquées
- Tester en développement d'abord
