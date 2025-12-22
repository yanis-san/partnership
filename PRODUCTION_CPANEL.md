# 🚀 Étapes de Production sur cPanel - Django

## 📋 Avant de commencer

✅ Vérifier que tout fonctionne en développement  
✅ Tous les tests passés: `python manage.py check`  
✅ Git pushé avec les changements  
✅ cPanel accès disponible  

---

## 🔧 Étape 1: Préparation de l'Environnement en Production

### 1.1 - Télécharger le projet sur cPanel

```bash
# Via cPanel - File Manager ou via Git
# Exemple: /home/username/public_html/monapp/
# ou
# /home/username/myapp/

# Via terminal cPanel:
cd /home/username/public_html
git clone https://github.com/votre/repo.git
cd repo
```

### 1.2 - Créer un Virtual Environment Python

```bash
# Dans le répertoire du projet
python3 -m venv venv

# Activer le venv
source venv/bin/activate

# Vérifier que c'est activé (devrait afficher (venv))
which python
```

### 1.3 - Installer les dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer les requirements
pip install -r requirements.txt
```

### 1.4 - Vérifier l'installation

```bash
python manage.py check
# Devrait afficher: "System check identified no issues (0 silenced)."
```

---

## 🔐 Étape 2: Configuration du fichier `.env` en Production

### 2.1 - Créer `.env.prod` sur le serveur

```bash
# Copier depuis le template
cp .env.dist .env

# Éditer avec nano ou vi
nano .env
```

### 2.2 - Remplir les valeurs critiques

```env
# ============================================
# SÉCURITÉ
# ============================================
DEBUG=False
SECRET_KEY=<votre-clé-secrète-générée>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# ============================================
# BASE DE DONNÉES (cPanel MySQL)
# ============================================
DATABASE_URL=mysql://username:password@localhost:3306/db_name

# OU si PostgreSQL:
DATABASE_URL=postgresql://username:password@localhost:5432/db_name

# ============================================
# EMAIL
# ============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password

DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SERVER_EMAIL=server@yourdomain.com

# ============================================
# ADMIN
# ============================================
ADMINS=Admin <admin@yourdomain.com>

# ============================================
# SÉCURITÉ HTTPS
# ============================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# ============================================
# ADMIN URL (UUID)
# ============================================
ADMIN_URL=admin-<uuid-généré>/

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO

# ============================================
# STATIQUES & MEDIA
# ============================================
STATIC_URL=/static/
STATIC_ROOT=/home/username/public_html/staticfiles/
MEDIA_URL=/media/
MEDIA_ROOT=/home/username/public_html/media/

# ============================================
# LANGUE ET TIMEZONE
# ============================================
LANGUAGE_CODE=fr-fr
TIME_ZONE=Africa/Algiers
```

### 2.3 - Générer une SECRET_KEY robuste

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2.4 - Générer un UUID pour l'admin

```bash
python -c "import uuid; print(uuid.uuid4())"
```

---

## 🗄️ Étape 3: Configuration de la Base de Données

### 3.1 - Créer la base de données via cPanel

**Dans cPanel > Databases > MySQL Databases:**
- Créer une nouvelle base: `username_dbname`
- Créer un utilisateur: `username_dbuser`
- Assigner l'utilisateur à la base avec tous les privilèges

**Récupérer les infos:**
```
Hostname: localhost (ou 127.0.0.1)
Username: username_dbuser
Password: [générée automatiquement]
Database: username_dbname
```

### 3.2 - Créer le fichier `.env` avec les bonnes infos

```env
DATABASE_URL=mysql://username_dbuser:password@localhost:3306/username_dbname
```

### 3.3 - Tester la connexion

```bash
# Activer le venv si pas activé
source venv/bin/activate

# Test de migration
python manage.py migrate --dry-run
```

---

## 🗂️ Étape 4: Migrations et Données

### 4.1 - Appliquer toutes les migrations

```bash
# Vérifier les migrations en attente
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate
```

### 4.2 - Collecte des fichiers statiques

```bash
# Créer le répertoire s'il n'existe pas
mkdir -p ~/public_html/staticfiles/

# Collecter les statiques (va hasher et compresser)
python manage.py collectstatic --no-input --clear

# Vérifier que les fichiers sont là
ls -la ~/public_html/staticfiles/
```

### 4.3 - Vérifier les permissions

```bash
# Les fichiers statiques doivent être lisibles
chmod -R 755 ~/public_html/staticfiles/
chmod -R 755 ~/public_html/media/

# Le dossier venv doit être protégé
chmod -R 750 venv/
```

---

## 👤 Étape 5: Créer un Superuser Admin

### 5.1 - Créer le premier administrateur

```bash
# Interactif
python manage.py createsuperuser

# Ou non-interactif
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('admin', 'admin@domain.com', 'password123')
>>> exit()
```

### 5.2 - Test d'accès

```bash
# Vérifier que l'admin existe
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: admin>]>
>>> exit()
```

---

## ✅ Étape 6: Vérifications Avant Production

### 6.1 - Checks Django complets

```bash
python manage.py check --deploy
```

Chercher les avertissements (WARNINGS) et les corriger si critiques.

### 6.2 - Test des migrations

```bash
# Vérifier qu'aucune migration en attente
python manage.py showmigrations | grep "\[ \]"
# Ne devrait rien afficher
```

### 6.3 - Test des statiques

```bash
# Vérifier que les statiques sont collectés
ls -la ~/public_html/staticfiles/
# Devrait avoir css/, js/, admin/, etc.
```

### 6.4 - Test de l'email

```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test Production', 'Message test', 'noreply@yourdomain.com', ['admin@yourdomain.com'])
1  # Si 1 = succès
```

---

## 🎯 Étape 7: Configuration du WSGI

### 7.1 - Vérifier que `config/wsgi.py` est correct

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
```

### 7.2 - Tester le WSGI localement

```bash
# Créer un script de test
python -c "from config.wsgi import application; print('WSGI OK')"
```

---

## 🔌 Étape 8: Configuration cPanel (Passenger ou uWSGI)

### Option A: Passenger (Recommandé cPanel)

**Dans cPanel > Setup Python App:**

1. **Créer une nouvelle Python App:**
   - Sélectionner version Python (3.10+)
   - Sélectionner le répertoire du projet
   - Définir chemin WSGI: `config/wsgi.py`

2. **Configuration automatique:**
   - cPanel va créer les fichiers config automatiquement
   - Vérifier que le venv est utilisé

3. **Test:**
   - Aller à `https://yourdomain.com`
   - Devrait charger votre app Django

### Option B: uWSGI (si Passenger non disponible)

**Créer `uwsgi_params.ini`:**
```ini
[uwsgi]
socket = /tmp/django.sock
master = true
processes = 4
threads = 2
chmod-socket = 666
vacuum = true
max-requests = 1000
max-requests-jitter = 50
module = config.wsgi:application
py-autoreload = 1
```

**Tester:**
```bash
uwsgi --ini uwsgi_params.ini
```

---

## 🌐 Étape 9: Configuration DNS et HTTPS

### 9.1 - Vérifier le DNS

```bash
# Le domaine doit pointer vers l'IP du serveur cPanel
nslookup yourdomain.com

# Devrait afficher l'IP du serveur cPanel
```

### 9.2 - Activer SSL/HTTPS

**Dans cPanel > SSL/TLS Status:**
- Installer certificat gratuit Let's Encrypt
- Vérifier que HTTPS fonctionne
- Rediriger HTTP → HTTPS

### 9.3 - Mettre à jour `ALLOWED_HOSTS`

```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## 🚨 Étape 10: Monitoring et Logs

### 10.1 - Logs Django

```bash
# Créer répertoire pour logs
mkdir -p ~/logs/

# Les logs vont dans:
# /home/username/logs/django.log

# Voir les logs en temps réel:
tail -f ~/logs/django.log
```

### 10.2 - Logs cPanel

**Dans cPanel > Error Log:**
- Chercher les erreurs Django
- Vérifier les warnings

**Logs Passenger:**
```bash
# Sous /var/log/passenger/
# Vérifier que pas d'erreurs critiques
```

### 10.3 - Erreurs 500

Si erreur 500:
```bash
# Vérifier les logs Django
tail -50 ~/logs/django.log

# Tester manuellement
python manage.py shell
>>> from django.core.wsgi import get_wsgi_application
>>> app = get_wsgi_application()
```

---

## 📊 Étape 11: Optimisations

### 11.1 - Cache

```env
# Optionnel: utiliser Redis si disponible
REDIS_URL=redis://localhost:6379/0
```

### 11.2 - Compression WhiteNoise

```env
WHITENOISE_COMPRESS=True
WHITENOISE_MAX_AGE=31536000  # 1 an pour fichiers hashés
```

### 11.3 - Database Connection Pooling

```python
# settings.py
DATABASES['default']['CONN_MAX_AGE'] = 600
```

---

## ✨ Étape 12: Vérifications Finales

### Checklist de Production:

- [ ] `DEBUG=False` dans `.env`
- [ ] `SECRET_KEY` changée et complexe
- [ ] `ALLOWED_HOSTS` configuré
- [ ] Base de données connectée (`migrate` réussi)
- [ ] Email configuré (test envoyé)
- [ ] Statiques collectés dans `/staticfiles/`
- [ ] Superuser admin créé
- [ ] HTTPS/SSL actif
- [ ] `.env` en `.gitignore` (pas commité)
- [ ] Admin URL en UUID (pas `/admin/`)
- [ ] Site accessible via HTTPS
- [ ] CSS/JS chargent correctement
- [ ] Formulaires fonctionnent
- [ ] Email test reçu
- [ ] Logs moniteurés

---

## 🆘 Dépannage cPanel

### App ne démarre pas

```bash
# Redémarrer l'app via cPanel
# Ou via terminal:
touch tmp/restart.txt  # Pour Passenger

# Vérifier les logs
tail -50 /var/log/passenger/error.log
```

### Erreur 502 Bad Gateway

```bash
# Généralement = app a crashé
# Chercher l'erreur dans les logs Django
tail -50 ~/logs/django.log

# Relancer les migrations
python manage.py migrate
```

### Permissions refusées

```bash
# Fixer les permissions
chmod -R 755 ~/public_html/
chmod -R 750 venv/
chmod -R 755 staticfiles/
chmod -R 755 media/
```

### Static files 404

```bash
# Recollecter les statiques
python manage.py collectstatic --clear --no-input

# Vérifier que STATIC_ROOT est correct
ls -la ~/public_html/staticfiles/
```

---

## 📝 Notes Importantes

1. **Ne JAMAIS commiter `.env`** - Utiliser `.env.dist` comme template
2. **Backup régulier** - La base de données via cPanel Backups
3. **Monitoring** - Vérifier les logs régulièrement
4. **Updates** - Mettre à jour Django et packages régulièrement
5. **Secrets sécurisés** - Jamais en clair dans les logs/emails

---

## 🎉 Vous êtes en production!

Une fois tout testé et vérifié, votre app Django est en production sur cPanel! 

Pour les mises à jour futures:
```bash
# Maintenir une branche main stable
git pull origin main

# Activer venv et installer updates
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Migrations
python manage.py migrate

# Recollecter statiques
python manage.py collectstatic --no-input

# Redémarrer via cPanel
```
