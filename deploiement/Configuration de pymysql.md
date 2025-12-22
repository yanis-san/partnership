
il faut installer pymysql 

ensuite notre fichier settings.py doit contenir ceci :

```python
import pymysql

```

Il faut rajouter ensuite la ligne suivante : 

```python
pymysql.install_as_MySQLdb()
```

Et remplacer la config de la bdd sqlite par ça (ou commenter) : 

```python
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
```