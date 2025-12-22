# ✅ Configuration Django-Environ Complète

## 📋 Résumé des Modifications

### 1. **Remplacement de `python-dotenv` par `django-environ`**

#### Avant (python-dotenv):

```python
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default-value")
```

#### Après (django-environ):

```python
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = env('SECRET_KEY', default='...')
```

### 2. **Avantages de `django-environ`**

✅ **Type casting automatique**

- `env.int('PORT')` → convertit en entier
- `env.bool('DEBUG')` → convertit en booléen
- `env.list('HOSTS')` → convertit en liste

✅ **Support des URLs de base de données**

- `env.db()` → parse automatiquement `DATABASE_URL`
- Supporte PostgreSQL, MySQL, SQLite, etc.

✅ **Support du cache**

- `env.cache_url()` → parse Redis/Memcache URLs

✅ **Meilleure gestion des erreurs**

- Lève `ImproperlyConfigured` si clé requise manquante

✅ **Plus léger et spécialisé pour Django**

---

## 📦 Fichiers Créés/Modifiés

### 1. **requirements.txt**

```
Django>=4.2,<5.3
django-environ>=0.10.0     ← Nouveau
qrcode[pil]>=7.4.2
whitenoise[brotli]>=6.6.0
Pillow>=10.0.0
gunicorn>=21.0.0
psycopg2-binary>=2.9.0
```

### 2. **config/settings.py** (Refactorisé)

**Load des variables:**

```python
import environ
env = environ.Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    # ... etc
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
```

**Utilisation partout:**

```python
# Types casting automatique
DEBUG = env('DEBUG')                                    # bool
SECRET_KEY = env('SECRET_KEY', default='...')         # str
EMAIL_PORT = env.int('EMAIL_PORT', default=587)       # int
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[]) # list

# Database avec URL
DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')
}
DATABASES['default']['CONN_MAX_AGE'] = 600

# Cache Redis (optionnel)
if REDIS_URL := env('REDIS_URL', default=''):
    CACHES = {'default': env.cache_url('REDIS_URL')}

# Email avec parsing ADMINS
ADMINS = env.list('ADMINS', default=['Admin <admin@domain.com>'])
ADMINS = [(name.strip(), email.strip('>')) for name, email in ...]
```

### 3. **.env** (Développement)

```env
DEBUG=True
SECRET_KEY=django-insecure-dev-only
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
LOG_LEVEL=DEBUG
```

### 4. **.env.dist** (Template pour production)

```env
# SECURITY
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com

# DATABASE (choix)
DATABASE_URL=sqlite:///db.sqlite3
# ou
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# EMAIL
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SÉCURITÉ
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True

# AUTRES
LANGUAGE_CODE=fr-fr
TIME_ZONE=Africa/Algiers
```

### 5. **.env.prod** (Production spécifique)

Même structure que `.env.dist` mais avec vos vraies valeurs

---

## 🚀 Utilisation

### Activation du venv:

```powershell
.\.venv\Scripts\activate
```

### Installation des dépendances:

```bash
pip install -r requirements.txt
```

### Vérifier la config:

```bash
python manage.py check
```

### Lancer le serveur de développement:

```bash
python manage.py runserver
```

---

## 🔒 Sécurité

### Développement (.env):

- `DEBUG=True`
- `SECURE_SSL_REDIRECT=False`
- Cookies non sécurisés

### Production (.env.prod):

- `DEBUG=False`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `SECURE_HSTS_SECONDS=31536000`
- URLs d'admin en UUID

---

## 📋 Vérification

✅ `python manage.py check` → "System check identified no issues"  
✅ Serveur démarre correctement avec `.env`  
✅ django-environ installé et fonctionnel  
✅ Type casting automatique fonctionne  
✅ Support PostgreSQL/MySQL prêt

---

## 🔄 Prochaines Étapes

1. **Production**: Remplir `.env.prod` avec vraies valeurs
2. **Database**: `python manage.py migrate`
3. **Statiques**: `python manage.py collectstatic --no-input`
4. **Deploy**: Utiliser `gunicorn -c gunicorn_config.py config.wsgi:application`

---

## 📞 Références

- **django-environ docs**: https://django-environ.readthedocs.io/
- **Django settings**: https://docs.djangoproject.com/en/5.2/ref/settings/
- **Deployment**: Voir `SETUP_PRODUCTION.md`
