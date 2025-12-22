
Dans le répértoire du projet là où il y a le dossier config, on créé un fichier passenger_wsgi.py et on met à l'interieur ceci : 

```python
import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'config/wsgi.py')
application = wsgi.application

```