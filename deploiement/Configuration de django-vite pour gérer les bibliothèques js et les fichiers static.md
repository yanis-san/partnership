## Installer git puis cookiecutter globalement sur la machine 

```
pip install cookiecutter
```

## Création du répertoire frontend dans le BASE_DIR

On se positionne dans le BASE_DIR du projet et on exécute la commande suivante :
```shell
cookiecutter gh:placepython/django-vite
```

Un dossier nommé "frontend" devrait apparaitre


## On installe django-vite

```shell
pipenv install django-vite
```

## Configuration dans la fichier settings

On ajoute dans INSTALLED_APPS : 

``` py
"django_vite",
```

Et egalement on doit rajouter les lignes suivantes : 

```python
MANIFEST_PATH = BASE_DIR / 'frontend' / 'dist' / 'manifest.json'
# Construit le chemin absolu vers le fichier manifest.json généré par Vite.
# BASE_DIR est supposé être défini dans les paramètres Django et pointe vers le répertoire de base du projet.
# 'frontend/dist/manifest.json' est le chemin relatif vers le fichier manifest.json, qui contient les informations sur les assets générés par Vite.

# Django-Vite configuration
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        # Définit le mode de développement en fonction de la variable DEBUG de Django.
        # Si DEBUG est True, le mode de développement est activé, ce qui signifie que Django-Vite utilisera le serveur de développement de Vite.
        # Si DEBUG est False, le mode de développement est désactivé, ce qui signifie que Django-Vite utilisera les assets générés par Vite.

        "manifest_path": MANIFEST_PATH,
        # Spécifie le chemin vers le fichier manifest.json, qui contient les informations sur les assets générés par Vite.
        # Ce chemin est utilisé par Django-Vite pour déterminer quels assets charger.
    },
}
```

## Ajout de la configuration dans les templates

On charge d'abord static et django_vite: 
```html
{% load static django_vite %}
```

Dans le template base.html dans le head, on ajoute les lignes suivantes (il faut)

```html
{% vite_hmr_client %}

{% vite_asset 'src/index.js' %}
```

## Exécution de npm install et npm run build

on doit se placer dans le répertoire frontend :

```shell
cd frontend
```

On doit exécuter les deux commandes suivantes : 

```shell
npm install
```


## Démarrage du serveur de développement

Pour démarrer le serveur on exécute la commande suivante en se plaçant dans le répertoire **frontend** : 

```shell
npm run start
```


