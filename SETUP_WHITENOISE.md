# SETUP_WHITENOISE.md

# Configuration correcte de WhiteNoise selon la doc officielle

## ✅ Configuration Django (4 étapes)

### 1. ✅ FAIT - Staticfiles configurés correctement

Dans `config/settings.py`:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 2. ✅ FAIT - WhiteNoise middleware activé

Dans `config/settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ICI - avant les autres middlewares!
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

### 3. ✅ FAIT - Compression et caching support

Dans `config/settings.py`:

```python
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

Cela:

- Compresse tous les fichiers (Gzip automatiquement)
- Génère des noms hashés (app.a4ef2389.css)
- Cache forever pour les fichiers hashés
- Combine compression + caching Django

### 4. ✅ FAIT - Development avec WhiteNoise

Dans `config/settings.py`:

```python
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  # ICI - avant staticfiles!
    ...
    'django.contrib.staticfiles',
    ...
]
```

Cela désactive le static handling Django en développement et utilise WhiteNoise.

---

## 🚀 Commandes de déploiement

### Avant production:

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Collecter les statiques (OBLIGATOIRE!)
python manage.py collectstatic --no-input

# 3. Exécuter les migrations
python manage.py migrate

# 4. Vérifier la config
python manage.py check --deploy
```

### Test en développement (sans DEBUG):

```bash
# Cela teste que WhiteNoise fonctionne correctement
python manage.py collectstatic --noinput
DEBUG=False python manage.py runserver
```

Les fichiers statiques doivent se charger normalement!

---

## 📁 Structure des fichiers statiques

Après `python manage.py collectstatic`:

```
staticfiles/
├── admin/
│   ├── css/
│   ├── js/
│   └── img/
├── app.db8f2edc0c8a.js        ← Fichier hashé
├── app.db8f2edc0c8a.js.br     ← Brotli compressé (si installé)
├── app.db8f2edc0c8a.js.gz     ← Gzip compressé
├── style.a4ef2389.css         ← Autre fichier hashé
└── staticfiles.json            ← Manifest des fichiers
```

WhiteNoise sert automatiquement la meilleure version (Gzip, Brotli, ou original).

---

## 🔧 Configuration recommandée

### requirements.txt (production):

```
Django>=4.2,<5.3
qrcode[pil]>=7.4.2
python-dotenv>=1.0.0
whitenoise[brotli]>=6.6.0  # Avec support Brotli
Pillow>=10.0.0
gunicorn>=21.0.0
```

### Commande Gunicorn (production):

```bash
python manage.py collectstatic --no-input && \
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 30
```

WhiteNoise servira les statiques automatiquement!

---

## ✅ Vérification que ça marche

```bash
# 1. Collectez les fichiers
python manage.py collectstatic --noinput

# 2. Démarrez le serveur avec DEBUG=False
DEBUG=False python manage.py runserver

# 3. Accédez à http://localhost:8000
# Les CSS/JS/images doivent se charger parfaitement!

# 4. Vérifiez dans l'inspecteur (F12):
# - Les fichiers doivent avoir des noms comme "app.db8f2edc0c8a.css"
# - Les headers doivent inclure "Content-Encoding: gzip" ou "br"
# - Le header "Cache-Control" doit être présent
```

---

## 🐛 Troubleshooting

### "ValueError: Missing staticfiles manifest entry"

- Assurez-vous que vous avez exécuté `python manage.py collectstatic --noinput`
- Vérifiez que les fichiers existent dans `staticfiles/`

### "Statiques ne se chargent pas en production"

- DEBUG doit être `False`
- `STATIC_ROOT` doit être correct
- WhiteNoise middleware doit être AVANT les autres middleware

### "Files not found during compression"

- Vérifiez que tous les fichiers CSS référencés existent
- Utilisez `python manage.py findstatic --verbosity 2 filename` pour déboguer

---

## 📚 Ressources

- [Documentation officielle WhiteNoise](https://whitenoise.readthedocs.io/)
- [Django staticfiles](https://docs.djangoproject.com/en/5.2/howto/static-files/)
- [Django deployment checklist](https://docs.djangoproject.com/en/5.2/deployment/checklist/)
