
On commence par installer django-environ avec
```shell
pipenv install django-environ
```

### Import de django-environ

```python
import environ
```

### On initialise les variables d'environnement dans le fichier settings.py

```python
env = environ.Env()  # Crée une instance de la classe environ.Env, qui permet de gérer les variables d'environnement.
env_file = str(BASE_DIR / ".env")  # Construit le chemin absolu vers le fichier .env en utilisant BASE_DIR et l'opérateur / pour joindre les chemins.
                                # BASE_DIR est supposé être défini dans les paramètres Django et pointe vers le répertoire de base du projet.
                                # str() convertit le chemin en une chaîne de caractères, car read_env attend une chaîne.
env.read_env(env_file)  # Lit le fichier .env situé au chemin env_file et charge les variables d'environnement qu'il contient.
                        # Ces variables sont ensuite accessibles via l'objet env.
```

### Création du fichier .env

On se positionne là où on a mentionné le chemin de env_file pour le fichier .env et on créé le fichier la bas

```shell
touch .env
```

### Définition des variables dans le fichier .env

On définit les variables qui contiennent des données sensibles dans le fichier .env en faisant attention à ne pas mettre d'espace entre les = comme dans la convention PEP8

Voici un exemple de fichier .env : 

```
# Django settings
SECRET_KEY=django-insecure-%vkwnqn-8o#yfr3m#h*8q+i$lzp56hzn@i=m&3-5
DEBUG=False
ALLOWED_HOSTS=test.com,www.test.com,localhost,127.0.0.1
DJANGO_ADMIN_URL_UUID=bfcc2753-2d86-4a44-89dd-546199ff5522
WAGTAIL_ADMIN_URL_UUID=71b090bf-3873-479e-abd7-817e19e28e7b

# Database settings
DB_NAME=user_database_name
DB_USER=user_database_name
DB_PASSWORD=123
DB_HOST=localhost
DB_PORT=3306


# reCAPTCHA settings
RECAPTCHA_PUBLIC_KEY=6Ldb7YQTv0i6l3MP9BpwQd
RECAPTCHA_PRIVATE_KEY=6Ldb7bEqA3Ww6co3dB9iYlhOykwRCC
RECAPTCHA_REQUIRED_SCORE=0.5

# Wagtail settings
WAGTAILADMIN_BASE_URL=https://test.com
```

Dans le fichier settings.py, on récupère les valeurs de cette manière :

```python
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG',default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
DJANGO_ADMIN_URL_UUID = env('DJANGO_ADMIN_URL_UUID')
WAGTAIL_ADMIN_URL_UUID = env('WAGTAIL_ADMIN_URL_UUID')


DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': env('DB_NAME'),
         'USER': env('DB_USER'),
         'PASSWORD': env('DB_PASSWORD'),
         'HOST': env('DB_HOST'),
         'PORT': env('DB_PORT'),
         'OPTIONS': {
             'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
         },
     }
 }
 

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = env.float('RECAPTCHA_REQUIRED_SCORE', default=0.5)

```