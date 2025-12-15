# Démarrage rapide

## 1. Préparation (première fois uniquement)

```bash
# Activez pipenv
pipenv shell

# Installez les dépendances si nécessaire
pipenv install

# Appliquez les migrations
python manage.py migrate

# Créez un compte administrateur
python manage.py createsuperuser

# Créez des données de test
python create_test_data.py
```

## 2. Lancer le serveur

```bash
# Si vous êtes dans pipenv shell
python manage.py runserver

# Ou directement
pipenv run python manage.py runserver
```

Le serveur démarre sur: **http://localhost:8000**

## 3. Premiers pas

### Admin (gestion)
- URL: http://localhost:8000/admin/
- Login: votre compte administrateur créé à l'étape 1
- Gérez les librairies, codes, paiements et élèves

### Inscription (public)
- URL: http://localhost:8000/register/
- Testez avec un code: `LIB4F6`, `LIB2AF` ou `LIBD3B`

### Dashboard librairie (public)
- URL: http://localhost:8000/library/LIB4F6/
- Remplacez `LIB4F6` par un code réel

### Dashboard admin (authentifié)
- URL: http://localhost:8000/admin/dashboard/
- Nécessite une connexion

## 4. Tâches courantes

### Ajouter une librairie
1. Admin → Librairies → Ajouter
2. Remplissez les infos
3. Sauvegardez (code généré auto)

### Créer un code supplémentaire
1. Admin → Codes de partenariat → Ajouter
2. Choisissez une librairie
3. Entrez un code (ex. LIB-PROMO-001)
4. Cochez "Actif"

### Créer un paiement
1. Admin → Paiements → Ajouter
2. Choisissez une librairie
3. Entrez le montant
4. Sauvegardez comme "En attente"
5. Marquez comme "Complété" après paiement

### Voir les statistiques
1. Accédez au dashboard admin: /admin/dashboard/
2. Ou lancez: `pipenv run python manage_script.py stats`

### Voir les élèves
- Admin → Élèves (vue complète avec filtres)
- Ou lancez: `pipenv run python manage_script.py students`

## 5. Données de test créées

### Librairies
| Nom | Code | Commission |
|-----|------|-----------|
| Librairie du Centre | LIB4F6 | 1500 DA |
| Librairie Educative | LIB2AF | 1200 DA |
| Librairie Scolaire Plus | LIBD3B | 1000 DA |

### Élèves
- Mohamed Bouchema (LIB Scolaire Plus)
- Aicha Rezgui (LIB Educative)
- Omar Karim (LIB Centre)
- Yasmine Tlemcani (LIB Scolaire Plus)
- Karim Bencheikh (LIB Educative)

## 6. Credentials par défaut

Si vous utilisez create_test_data.py:
- Admin: `admin` / `admin123`

## 7. Fichiers importants

```
irl_ad/
├── manage.py                    # Commande Django
├── create_test_data.py          # Données de test
├── manage_script.py             # Utilitaires
├── README.md                    # Documentation complète
├── QUICKSTART.md               # Ce fichier
├── requirements.txt             # Dépendances (pip)
├── Pipfile & Pipfile.lock      # Dépendances (pipenv)
├── db.sqlite3                  # Base de données
├── config/
│   ├── settings.py             # Configuration Django
│   ├── urls.py                 # Routage
│   └── wsgi.py
├── partnerships/
│   ├── models.py               # Library, Payment, Code
│   ├── views.py                # Dashboards
│   ├── admin.py                # Interface admin
│   ├── urls.py
│   └── templates/
│       └── partnerships/
│           └── admin-dashboard.html
└── students/
    ├── models.py               # Student
    ├── views.py                # Inscription, dashboards
    ├── forms.py                # Formulaire
    ├── admin.py
    ├── urls.py
    └── templates/
        ├── base.html
        └── students/
            ├── register.html
            ├── registration-success.html
            └── library-dashboard.html
```

## 8. Besoin d'aide?

- Voir **README.md** pour la documentation complète
- Vérifier **config/settings.py** pour les paramètres
- Consulter les logs Django si erreur

## 9. Redémarrage du serveur

```bash
# Arrêtez avec Ctrl+C
# Puis relancez
python manage.py runserver

# Ou sur un port différent
python manage.py runserver 8001
```

## 10. Réinitialiser la base de données

**ATTENTION: Supprime toutes les données!**

```bash
# Supprimer la base
rm db.sqlite3

# Refaire les migrations
python manage.py migrate

# Recréer l'admin
python manage.py createsuperuser

# Recréer les données de test
python create_test_data.py
```

---

**Prêt? Lancez le serveur et testez!** 🚀
