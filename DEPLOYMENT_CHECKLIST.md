# ✅ CHECKLIST DE DÉPLOIEMENT PRODUCTION

# Plateforme d'Affiliation Torii

## 📋 Avant le Déploiement

### Configuration de Base

- [ ] Fichier `.env.prod` créé avec `python setup_production.py`
- [ ] `DEBUG=False` dans `.env.prod`
- [ ] `SECRET_KEY` changée et complexe (24+ caractères)
- [ ] `ALLOWED_HOSTS` configuré avec vos domaines
- [ ] `ADMIN_URL` en UUID (ex: `admin-a1b2c3d4-e5f6/`)
- [ ] Fichier `.env.prod` dans `.gitignore`

### Base de Données

- [ ] PostgreSQL installé et en cours d'exécution
- [ ] Utilisateur et base de données créés
- [ ] `DATABASE_URL` correct dans `.env.prod`
- [ ] `python manage.py migrate --settings=config.settings` exécuté
- [ ] Backup prévu avant production

### Sécurité

- [ ] HTTPS/SSL activé
- [ ] Certificats SSL valides (Let's Encrypt)
- [ ] CSP headers configurés
- [ ] HSTS headers activés
- [ ] Cookies sécurisés (SECURE_SSL_REDIRECT, etc.)
- [ ] X-Frame-Options défini
- [ ] Rate limiting activé (optionnel mais recommandé)

### Fichiers Statiques

- [ ] `python manage.py collectstatic --no-input` exécuté
- [ ] Vérifier que `/staticfiles/` contient tous les fichiers
- [ ] WhiteNoise configuré dans MIDDLEWARE
- [ ] Cache headers testés (ETag, Last-Modified)
- [ ] Compression Gzip/Brotli vérifiée

### Email

- [ ] Serveur SMTP configuré
- [ ] Gmail app password généré (si Gmail)
- [ ] TEST: Email d'administrateur fonctionne
- [ ] EMAIL_HOST_USER et EMAIL_HOST_PASSWORD configurés
- [ ] DEFAULT_FROM_EMAIL défini

### Dépendances

- [ ] `pip install -r requirements.txt` exécuté
- [ ] Gunicorn 21.0+ installé
- [ ] WhiteNoise[brotli] 6.6+ installé
- [ ] Toutes les dépendances listées dans requirements.txt

---

## 🚀 Déploiement

### Étape 1: Préparer le Serveur

```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql nginx

# Créer user de service
sudo useradd -m torii_service
sudo -u torii_service mkdir -p /home/torii_service/app
```

### Étape 2: Déployer le Code

```bash
# Cloner/copier le projet
cd /home/torii_service/app
git clone <your-repo> .
# ou
cp -r /path/to/local/project .

# Créer venv
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
```

### Étape 3: Configurer l'Environnement

```bash
# Copier .env.prod
cp .env.prod.example .env.prod
# Éditer avec vos vraies valeurs
nano .env.prod
```

### Étape 4: Préparer les Statiques

```bash
export $(cat .env.prod | xargs)
python manage.py migrate
python manage.py collectstatic --no-input
```

### Étape 5: Configurer Gunicorn

```bash
# Créer service systemd
sudo nano /etc/systemd/system/gunicorn.service
```

Contenu:

```
[Unit]
Description=Gunicorn application server for Torii
After=network.target

[Service]
Type=notify
User=torii_service
Group=www-data
WorkingDirectory=/home/torii_service/app
EnvironmentFile=/home/torii_service/app/.env.prod
ExecStart=/home/torii_service/app/venv/bin/gunicorn \
    -c gunicorn_config.py \
    config.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### Étape 6: Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/torii
```

Utiliser la configuration fournie dans SETUP_PRODUCTION.md

```bash
sudo ln -s /etc/nginx/sites-available/torii /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Étape 7: SSL/HTTPS

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### Étape 8: Logs & Monitoring

```bash
# Logs Gunicorn
sudo journalctl -u gunicorn -f

# Logs Nginx
sudo tail -f /var/log/nginx/torii_access.log
sudo tail -f /var/log/nginx/torii_error.log

# Logs Django (si configuré)
tail -f /var/log/django/django.log
```

---

## ✅ Tests Post-Déploiement

### 1. Admin Panel

- [ ] Accéder à `https://yourdomain.com/admin-<uuid>/`
- [ ] Se connecter avec credentials
- [ ] Vérifier que les données sont là
- [ ] Créer un utilisateur test
- [ ] Modifier un utilisateur test

### 2. Site Public

- [ ] Page d'accueil charge correctement
- [ ] CSS/JS chargent (pas d'erreurs 404)
- [ ] Responsive design fonctionne (mobile/tablet)
- [ ] Hamburger menu fonctionne (Alpine.js)
- [ ] Formulaires HTMX répondent correctement

### 3. Base de Données

- [ ] Connexion BD réussit
- [ ] Migrations appliquées
- [ ] Données visibles dans admin
- [ ] Utilisateurs testables

### 4. Fichiers Statiques

- [ ] CSS/images chargent rapidement
- [ ] JS minimifiés
- [ ] Cache headers corrects (`Cache-Control: max-age=...`)
- [ ] Compression active (gzip/brotli)

### 5. Email

- [ ] Tester envoi d'email de contact
- [ ] Vérifier qu'un email de test est reçu
- [ ] Vérifier l'adresse `from`

### 6. Sécurité

- [ ] Pas de DEBUG=True dans les logs
- [ ] HTTPS/SSL valide
- [ ] CSP headers présents
- [ ] Admin URL en UUID (pas `/admin/`)
- [ ] Cookies sécurisés

---

## 🔍 Dépannage

### Statiques ne chargent pas (404)

```bash
# Recollecter
sudo systemctl stop gunicorn
export $(cat .env.prod | xargs)
python manage.py collectstatic --clear --no-input
sudo systemctl start gunicorn

# Vérifier les fichiers
ls -la staticfiles/
```

### Admin pas accessible

```bash
# Vérifier l'URL dans settings
cat .env.prod | grep ADMIN_URL

# Vérifier les logs
sudo journalctl -u gunicorn -n 50
```

### Database connection error

```bash
# Vérifier la connexion
export $(cat .env.prod | xargs)
python -c "from django.core.management import execute_from_command_line; execute_from_command_line(['manage.py', 'dbshell'])"

# Ou directement
psql $DATABASE_URL
```

### Email non envoyé

```bash
# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test Subject', 'Test Message', 'noreply@yourdomain.com', ['admin@yourdomain.com'])
1  # Si 1, succès. 0 = erreur
```

### Performance lente

```bash
# Vérifier les workers Gunicorn
ps aux | grep gunicorn

# Vérifier la charge serveur
top
free -h
df -h

# Activer cache Redis (optionnel)
# pip install django-redis
# CACHES dans settings.py
```

---

## 📊 Monitoring Recommandé

### Logs

- Accès Nginx: `/var/log/nginx/torii_access.log`
- Erreurs Nginx: `/var/log/nginx/torii_error.log`
- Gunicorn: `sudo journalctl -u gunicorn`
- Django: `/var/log/django/django.log` (si configuré)

### Alertes

- Disk space < 10%
- Memory usage > 80%
- Uptime monitoring
- SSL certificate renewal (Let's Encrypt auto)

### Services

- Gunicorn: `systemctl status gunicorn`
- Nginx: `systemctl status nginx`
- PostgreSQL: `systemctl status postgresql`

---

## 🔐 Maintenance Régulière

### Quotidien

- [ ] Vérifier logs des erreurs
- [ ] Vérifier la charge serveur
- [ ] Vérifier l'espace disque

### Hebdomadaire

- [ ] Backup de la BD (script cron)
- [ ] Vérifier les utilisateurs inactifs
- [ ] Vérifier les paiements en attente

### Mensuel

- [ ] Update des dépendances Python
- [ ] Renouvellement SSL check
- [ ] Review des logs de sécurité

### Annuel

- [ ] Audit de sécurité complet
- [ ] Plan de disaster recovery
- [ ] Review de la capacité serveur

---

## 📞 Contacts & Documentation

- Documentation: `/md/SETUP_PRODUCTION.md`
- Configuration: `.env.prod`
- Logs: `/var/log/`
- Backup: `/home/torii_service/backups/`

---

⚡ **Bon déploiement!** ⚡
