

En production, nous devons nous assurer d'avoir une configuration similaire : 

Tout d'abord, ilfaut s'assurer de mettre le fichier static dans le public_html, ensuite :

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# Définit l'URL de base pour les fichiers statiques.
# '/static/' signifie que les fichiers statiques seront servis à partir de l'URL /static/.

STATIC_ROOT = '/home/username/public_html/static'
# Définit le répertoire où Django collectera tous les fichiers statiques lors de l'exécution de la commande collectstatic.
# '/home/username/public_html/static' est le chemin absolu sur le serveur cPanel où les fichiers statiques seront stockés.

STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "public",
    BASE_DIR / "frontend" / "dist",
]
# Définit une liste de répertoires supplémentaires où Django recherchera des fichiers statiques.
# BASE_DIR / "frontend" / "public" indique le répertoire "public" dans le dossier "frontend" du projet, où les fichiers statiques de développement peuvent être stockés.
# BASE_DIR / "frontend" / "dist" indique le répertoire "dist" dans le dossier "frontend" du projet, où les fichiers statiques compilés par Vite sont stockés.

# Media files
MEDIA_URL = '/media/'
# Définit l'URL de base pour les fichiers média (fichiers uploadés par les utilisateurs).
# '/media/' signifie que les fichiers média seront servis à partir de l'URL /media/.

MEDIA_ROOT = '/home/username/public_html/media'
# Définit le répertoire où Django stockera les fichiers média uploadés par les utilisateurs.
# '/home/username/public_html/media' est le chemin absolu sur le serveur cPanel où les fichiers média seront stockés.
```

Afin d'utiliser nos propres fichiers js et css, il faut suivre quelques étapes :

Commençons par les fichiers CSS : 

Dans ***frontend/src/styles/app.css*** nous pouvons importer nos fichiers css personnalisés : 


```css
/* Importation des fichiers CSS personnalisés */
@import '../../../<app_name>/static/css/style.css'; 
```

Pour **js** c'est sensiblement la même chose à la fin du fichier ***frontend/src/index.js***, nous pouvons importer nos fichiers js personnalisés : 

```javascript
import "../../<app_name>/static/js/script.js";
```

***<app_name> correspond au dossier principal de l'application dans le même répertoire que config***

Il est nécéssaire de comprendre aussi que le fichier ***index.js**** est le point d'entrée des fichiers css indirectement avec le fichier app.css. Il faut donc s'assurer d'avoir la ligne suivante dans index.js : 

```javascript
// Entry point for CSS styles
import "./styles/app.css";
```


## En production
### Compiler les fichiers static 

On peut compiler nos fichiers static à cette étape là : 

```shell
npm run build
```


### Collecter les fichiers static

Dans le serveur de production, nous devons exécuter la ligne suivante pour collecter les fichiers static : 

```shell
python manage.py collectstatic
```

