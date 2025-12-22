

Il faut s'assurer de définir des liens secrets pour les interfaces d'administration django ou/et wagtail avec uuid. Les adresses seronts dans le fichier .env : 

Dans l'interpreteur python : 

```python
import uuid
uuid.uuid4() # On copie et on colle le code généré dans le .env
```

Par la suite dans le fichier url, il faut spécifier nos variables qui contiennent le code uuid (voir la configuration dans [[Gérer les données sensibles avec django environ]])
```python
    path(f'django-admin/{settings.DJANGO_ADMIN_URL_UUID}/', admin.site.urls),
    path(f'admin/{settings.WAGTAIL_ADMIN_URL_UUID}/', 
```
Nous pouvons rajouter ces lignes de codes afin que l'application soit sécurisé : 

```python
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    
else:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

