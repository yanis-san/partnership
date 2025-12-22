# 🚀 Guide de Déploiement - Plateforme d'Affiliation Torii

## Stack Technologique

✅ **Frontend:**

- Alpine.js 3.x (interactivité, menu hamburger)
- HTMX 1.9 (requêtes asynchrones, confirmation d'étudiants)
- CSS personnalisé (pas de framework)

✅ **Backend:**

- Django 4.2+
- Python 3.11+
- Gunicorn (serveur WSGI)
- WhiteNoise (gestion statiques)

✅ **Base de données:**

- SQLite (développement)
- PostgreSQL recommandé (production)

---

## 📋 Prérequis Avant Déploiement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Créer un fichier .env en production
cp .env.example .env

# 3. Générer une nouvelle SECRET_KEY en production
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 🔧 Configuration Environnement Production

Créez un fichier `.env` avec:

```env
# Django
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Base de données (exemple PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/torii_db

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Admin
ADMIN_NAME=Votre Nom
ADMIN_EMAIL=admin@yourdomain.com

# Sécurité
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🔐 Commandes de Déploiement

```bash
# 1. Collectez les fichiers statiques (WhiteNoise les servira)
python manage.py collectstatic --no-input

# 2. Exécutez les migrations
python manage.py migrate

# 3. Créez un superuser
python manage.py createsuperuser

# 4. Vérifiez la config
python manage.py check --deploy

# 5. Démarrez Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 🐳 Déploiement avec Docker (Recommandé)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Collecter les statiques
RUN python manage.py collectstatic --no-input

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: torii_db
      POSTGRES_USER: torii_user
      POSTGRES_PASSWORD: strong_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"
    environment:
      DEBUG: "False"
      DATABASE_URL: postgresql://torii_user:strong_password@db:5432/torii_db
      SECRET_KEY: your-secret-key
      ALLOWED_HOSTS: localhost,127.0.0.1
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

volumes:
  postgres_data:
```

### Lancer avec Docker

```bash
# Démarrer les services
docker-compose up -d

# Créer un superuser
docker-compose exec web python manage.py createsuperuser

# Voir les logs
docker-compose logs -f web
```

---

## 🌐 Déploiement sur Heroku

### 1. Installez Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Téléchargez depuis https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Créez Procfile

```bash
web: gunicorn config.wsgi:application
release: python manage.py migrate
```

### 3. Créez .slugignore (optionnel)

```
*.pyc
__pycache__
.env
staticfiles
*.sqlite3
```

### 4. Déploiement

```bash
# Login Heroku
heroku login

# Créez l'app
heroku create your-app-name

# Configurez les variables d'environnement
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Déployez
git push heroku main

# Exécutez les migrations
heroku run python manage.py migrate

# Créez un superuser
heroku run python manage.py createsuperuser

# Ouvrez l'app
heroku open
```

---

## 🔄 Déploiement sur PythonAnywhere (Simple)

### 1. Créez un compte sur pythonanywhere.com

### 2. Clonez votre repo

```bash
cd /home/yourusername
git clone https://github.com/yourusername/irl_ad.git
```

### 3. Créez un virtual environment

```bash
mkvirtualenv --python=/usr/bin/python3.11 torii
pip install -r ~/irl_ad/requirements.txt
```

### 4. Configurez Django

Allez sur PythonAnywhere Dashboard → Web Apps → Add a new web app

- Sélectionnez "Manual configuration"
- Choisissez Python 3.11
- Configurez le virtual environment: `/home/yourusername/.virtualenvs/torii`
- Configurez le WSGI: `/home/yourusername/irl_ad/config/wsgi.py`

### 5. Configurez .env

```bash
cp /home/yourusername/irl_ad/.env.example /home/yourusername/irl_ad/.env
# Éditez le fichier avec vos variables
```

### 6. Collectez les statiques

```bash
workon torii
python ~/irl_ad/manage.py collectstatic --no-input
```

---

## 📊 Performance & Optimisations

### Avec WhiteNoise:

- ✅ Fichiers statiques compressés automatiquement
- ✅ Cache headers optimisés
- ✅ Pas besoin de serveur web supplémentaire (Nginx)
- ✅ Compression Gzip automatique
- ✅ Manifest staticfiles pour le versioning

### Optimisations recommandées:

```python
# Dans settings.py (déjà configuré)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Cela:

1. Génère des hashes uniques pour chaque fichier
2. Compresse tous les fichiers (JS, CSS)
3. Ajoute des headers de cache longs terme
4. Pas de rechargement du cache pendant 1 an

---

## ✅ Checklist de Sécurité Avant Production

- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` configuré correctement
- [ ] `SECRET_KEY` unique et fort
- [ ] HTTPS/SSL configuré
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `.env` ne pas commiter dans Git
- [ ] Database sécurisée avec mot de passe fort
- [ ] Emails configurés pour notifications admin
- [ ] Backups automatiques de la base de données

---

## 🐛 Troubleshooting Déploiement

### "Static files not served"

```bash
# Réappliquez la config WhiteNoise
python manage.py collectstatic --clear --noinput
```

### "ALLOWED_HOSTS error"

```env
# Vérifiez dans .env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-ip
```

### "Database connection refused"

```bash
# Vérifiez DATABASE_URL en .env
# Format: postgresql://user:password@host:port/dbname
```

### "Email not sending"

```bash
# Testez les paramètres email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

---

## 📈 Monitoring & Logs

### Avec Docker:

```bash
docker-compose logs -f web
```

### Avec Heroku:

```bash
heroku logs --tail
```

### Avec PythonAnywhere:

- Allez dans "Log files" sur le dashboard

---

## 🔄 Mise à Jour & Maintenance

```bash
# Mettez à jour les dépendances
pip install --upgrade -r requirements.txt

# Exécutez les migrations
python manage.py migrate

# Collectez les nouveaux statiques
python manage.py collectstatic --no-input

# Redémarrez l'application
# (automatique avec Docker/Heroku, manuel sur PythonAnywhere)
```

---

## 📚 Ressources Additionnelles

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/deployment/checklist/)
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/)
- [Gunicorn Settings](https://gunicorn.org/)
- [Alpine.js Docs](https://alpinejs.dev/)
- [HTMX Documentation](https://htmx.org/)

---

**Happy Deploying! 🚀**
