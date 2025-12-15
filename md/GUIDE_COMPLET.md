# Guide Complet du Système de Partenariat Librairies

## 📚 Table des Matières

1. [Aperçu rapide](#aperçu-rapide)
2. [Installation](#installation)
3. [Guide d'utilisation](#guide-dutilisation)
4. [Architecture](#architecture)
5. [API et URLs](#api-et-urls)
6. [Dépannage](#dépannage)
7. [Production](#production)

---

## 🎯 Aperçu Rapide

### Qu'est-ce que c'est?
Un système complet de gestion d'affiliations pour les librairies partenaires d'une école. Chaque librairie reçoit un code unique et gagne de l'argent pour chaque élève qu'elle ramène.

### Comment ça fonctionne?
```
Librairie → Code Unique → Élève s'inscrit → Commission générée → Paiement
  (LIB001)  (partage)    (avec le code)    (1000 DA/élève)     (à suivre)
```

### En 30 secondes
1. Admin crée une librairie → code auto-généré
2. Librairie partage son code
3. Élève s'inscrit avec le code
4. Commission calculée automatiquement
5. Admin paie la librairie
6. Tout est transparent et traçable

---

## ⚡ Installation

### Prérequis
- Windows/Mac/Linux
- Python 3.11+
- pipenv (gestionnaire de paquets)

### Étapes

```bash
# 1. Naviguer vers le projet
cd "C:\Users\yanis\Documents\Automatisation code\irl_ad"

# 2. Installer les dépendances
pipenv install

# 3. Activer l'environnement
pipenv shell

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un admin
python manage.py createsuperuser

# 6. Créer des données de test (optionnel)
python create_test_data.py

# 7. Lancer le serveur
python manage.py runserver
```

### Résultat
```
Server is running at http://localhost:8000
Admin access at http://localhost:8000/admin
```

---

## 📖 Guide d'Utilisation

### Cas 1: Ajouter une librairie partenaire

**Qui?** L'administrateur de l'école
**Où?** `/admin/` → Librairies → Ajouter

**Étapes:**
1. Aller à http://localhost:8000/admin/
2. Cliquer sur "Librairies"
3. Cliquer sur "Ajouter une librairie"
4. Remplir les champs:
   - **Nom**: "Librairie XYZ"
   - **Email**: "xyz@librairie.dz" (unique)
   - **Téléphone**: "+213 21 XXXXXXX"
   - **Personne de contact**: "Ahmed Ben"
   - **Adresse**: "Rue du Marché, Alger"
   - **Commission/élève**: 1500 (ou autre montant)
5. Cliquer "Sauvegarder"
6. **Code généré automatiquement** (ex: LIB4F6)

**Résultat:** La librairie peut maintenant partager son code avec les élèves

---

### Cas 2: S'inscrire en tant qu'élève

**Qui?** Un nouvel élève
**Où?** `/register/` (public, pas de login)

**Flux:**
1. Obtenir un code de sa librairie (ex: LIB4F6)
2. Aller à http://localhost:8000/register/
3. Remplir le formulaire:
   - Prénom, Nom
   - Email (unique)
   - Téléphone (optionnel)
   - Niveau (1ère, 2e, 3e année)
   - **Code partenaire** (obligatoire!)
4. Cliquer "S'inscrire"
5. Voir la page de confirmation

**Résultat:**
- Élève enregistré dans la base
- Commission de 1000 DA (ou configurée) ajoutée au compte de la librairie
- Élève voit ses détails

---

### Cas 3: Consulter ses stats (librairie)

**Qui?** Une librairie partenaire
**Où?** `/library/LIB4F6/` (remplacer par son code)

**Accès:** Public, pas de password
**URL:** http://localhost:8000/library/LIB4F6/

**Informations affichées:**
```
Élèves parrainés: 5
Montant généré: 5000 DA (5 × 1000)
Montant payé: 2000 DA
Solde à recevoir: 3000 DA
Statut: Partiel
```

**Actions possibles:** Voir la liste des élèves

---

### Cas 4: Gérer un paiement

**Qui?** L'administrateur
**Où?** `/admin/` → Paiements

**Créer un paiement:**
1. Aller à `/admin/partnerships/payment/`
2. Cliquer "Ajouter un paiement"
3. Choisir la librairie
4. Entrer le montant (ex: 1500 DA)
5. Entrer une référence (ex: "Virement bancaire #123")
6. Cliquer "Sauvegarder"
7. **Statut = "En attente"**

**Marquer comme payé:**
1. Aller à la liste des paiements
2. Sélectionner le(s) paiement(s)
3. Choisir l'action "Marquer comme complété"
4. Cliquer "Exécuter"
5. **Statut = "Complété"**

**Résultat:**
- La librairie le voit comme "Payé" sur son dashboard
- Historique gardé pour l'audit

---

### Cas 5: Voir le dashboard admin

**Qui?** L'administrateur
**Où?** `/admin/dashboard/`

**Authentification requise** (login admin)

**Affichage:**
- Nombre total de librairies
- Nombre total d'élèves
- Montant total généré
- Montant total payé
- Montant restant à payer
- Tableau des librairies avec leurs stats
- Paiements récents
- Élèves récents

**Actions rapides:**
- Bouton pour gérer les librairies
- Bouton pour gérer les paiements
- Bouton pour voir tous les élèves

---

## 🏗️ Architecture

### Organigramme Entités

```
LIBRAIRIE (Library)
├── Commission par élève: 1500 DA
├── Codes partenariat multiples
│   ├── LIB4F6 (actif)
│   ├── LIB-PROMO-001 (actif)
│   └── LIB-OLD-CODE (inactif)
├── Élèves associés
│   ├── Mohamed (via LIB4F6)
│   ├── Fatima (via LIB4F6)
│   └── Ali (via LIB-PROMO-001)
└── Paiements
    ├── Paiement #1: 1500 DA (complété)
    ├── Paiement #2: 3000 DA (en attente)
    └── Paiement #3: 1500 DA (complété)
```

### Flow de Commission

```
1. Admin crée Librairie
   ↓ (Commission/élève = 1500)

2. Code généré (LIB4F6)
   ↓ (Librairie le partage)

3. Élève s'inscrit avec LIB4F6
   ↓ (Commission = +1500)

4. Commission totale = 1500
   ↓ (Admin doit payer)

5. Admin crée paiement (1500 DA)
   ↓ (Marque comme complété)

6. Librairie voit: PAYÉ ✅
```

### Modèles de Données

**Library (Librairie)**
```
id: UUID unique
name: Texte
email: Email unique
phone: Téléphone
contact_person: Nom personne
address: Adresse
commission_per_student: Montant
status: active|inactive|suspended
created_at: Date/heure
updated_at: Date/heure
```

**Student (Élève)**
```
id: UUID unique
first_name: Prénom
last_name: Nom
email: Email unique
phone: Téléphone
library: Référence vers Library
referral_code: Code utilisé
level: 1st_year|2nd_year|3rd_year|other
status: active|inactive|suspended
enrollment_date: Date/heure
created_at / updated_at
```

**PartnershipCode (Code)**
```
id: UUID unique
library: Référence vers Library
code: Texte unique (ex: LIB4F6)
is_active: Booléen
created_at: Date/heure
```

**Payment (Paiement)**
```
id: UUID unique
library: Référence vers Library
amount: Montant
status: pending|completed|cancelled
reference: Texte (ex: "Virement #123")
notes: Notes supplémentaires
created_at: Date/heure
completed_at: Date/heure (si complété)
```

---

## 🔗 API et URLs

### URLs Publiques

| URL | Méthode | Description |
|-----|---------|-------------|
| `/register/` | GET/POST | Formulaire d'inscription élève |
| `/registration-success/` | GET | Confirmation d'inscription |
| `/library/LIB4F6/` | GET | Dashboard librairie public |

### URLs Admin (authentification requise)

| URL | Description |
|-----|------------|
| `/admin/` | Interface admin Django |
| `/admin/partnerships/library/` | Gérer librairies |
| `/admin/partnerships/partnershipcode/` | Gérer codes |
| `/admin/partnerships/payment/` | Gérer paiements |
| `/admin/students/student/` | Gérer élèves |
| `/admin/dashboard/` | Dashboard personnalisé |

### Exemples de Requêtes

**Inscrire un élève:**
```bash
POST /register/
Données:
  first_name=Ahmed
  last_name=Benali
  email=ahmed@example.com
  phone=0671234567
  level=1st_year
  referral_code=LIB4F6
```

**Voir le dashboard d'une librairie:**
```bash
GET /library/LIB4F6/
# Affiche les stats de la librairie avec le code LIB4F6
```

---

## 🐛 Dépannage

### Erreur: "Code partenaire invalide"

**Cause:** Le code n'existe pas ou n'est pas actif

**Solutions:**
1. Vérifier que le code existe: `/admin/partnerships/partnershipcode/`
2. Vérifier que `is_active = Oui`
3. Vérifier que la librairie est active (status = "active")

### Erreur: "Email déjà utilisé"

**Cause:** L'email est déjà enregistré

**Solutions:**
1. Utiliser un email différent
2. Ou réutiliser un compte existant

### Dashboard admin ne s'affiche pas

**Cause:** Pas d'authentification

**Solutions:**
1. Aller à `/admin/` et se connecter d'abord
2. Puis accéder à `/admin/dashboard/`

### Les données de test ne sont pas créées

**Cause:** Le script n'a pas été lancé

**Solutions:**
```bash
pipenv run python create_test_data.py
```

### Oublié le password admin?

```bash
python manage.py changepassword admin
# Entrez le nouveau password
```

---

## 🚀 Production

### Avant de déployer

**Sécurité:**
```python
# config/settings.py
DEBUG = False
SECRET_KEY = "nouvelle-clé-générée"
ALLOWED_HOSTS = ["votredomaine.com"]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Base de données:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nom_db',
        'USER': 'utilisateur',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Serveur:**
```bash
# Installer gunicorn
pip install gunicorn

# Lancer
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

**Web server (Nginx):**
```nginx
server {
    listen 80;
    server_name votredomaine.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### Sauvegarde de la base de données

```bash
# Exporter les données
python manage.py dumpdata > backup.json

# Importer les données
python manage.py loaddata backup.json
```

---

## 📊 Rapports Utiles

### Générer un rapport de paiements

```bash
pipenv run python manage_script.py stats
```

### Lister tous les élèves

```bash
pipenv run python manage_script.py students
```

---

## 📞 Besoin d'aide?

1. **Erreurs Django**: Vérifier la console
2. **Base de données**: Voir `/admin/`
3. **Erreurs de formulaire**: Vérifier les messages d'erreur
4. **Performance**: Consulter `/admin/dashboard/`

---

## ✅ Checklist d'utilisation

- [ ] Installation complète et serveur lancé
- [ ] Admin créé et accessible
- [ ] Données de test créées
- [ ] Librairies créées et codes générés
- [ ] Formulaire d'inscription testé
- [ ] Dashboard librairie testé
- [ ] Dashboard admin testé
- [ ] Paiements créés et marqués
- [ ] Documentation lue en entier

---

## 📝 Notes Finales

- **Codes**: En MAJUSCULES (LIB4F6, pas lib4f6)
- **Montants**: En Dinars Algériens (DA)
- **Emails**: Uniques (pas de doublons)
- **Commissions**: Recalculées à chaque inscription
- **Paiements**: À gérer manuellement par l'admin
- **Statuts**: Voir la liste dans chaque modèle

---

**Projet créé et prêt à être utilisé! 🎉**

Pour plus d'informations:
- Voir **README.md** pour la documentation technique
- Voir **QUICKSTART.md** pour un démarrage rapide
- Voir **URLS.md** pour la liste complète des endpoints
