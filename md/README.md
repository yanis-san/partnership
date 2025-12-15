# 📚 Système de Partenariat Librairies

Un système complet et robuste de suivi automatique des partenariats avec les librairies pour la promotion d'une école. Chaque librairie partenaire reçoit un code unique et reçoit une commission pour chaque élève qu'elle ramène.

## 🎯 Objectif

Motiver les librairies partenaires à faire la promotion de votre école en leur donnant une commission mesurable, transparente et vérifiable pour chaque élève inscrit via elles. C'est un système d'affiliation locale (comme les cromo sur internet, mais pour le monde physique).

## ✨ Fonctionnalités

### 🎟️ Attribution de codes
- Chaque librairie reçoit un code unique (ex. LIB001)
- Codes générés automatiquement lors de la création de la librairie
- Codes multiples possibles par librairie

### 🧍 Inscription élèves
- Formulaire d'inscription simple et intuitif
- Validation du code partenaire
- Enregistrement automatique du lien librairie ↔ élève
- Support des niveaux d'études

### 💰 Suivi des commissions
- Calcul automatique des gains par librairie
- Commission configurable par élève (par défaut: 1000 DA)
- Suivi en temps réel des montants générés

### 📊 Dashboard admin
- Vue d'ensemble de toutes les librairies
- Statistiques globales (élèves, revenus, paiements)
- Liste des paiements avec filtres
- Actions rapides pour gérer les paiements

### 🧾 Gestion des paiements
- Création et suivi des paiements
- Marquer les paiements comme complétés/en attente
- Statuts clairs: "Payé", "Partiel", "Non payé"
- Historique complet des paiements

### 👀 Dashboard librairie (public)
- Chaque librairie peut voir ses statistiques
- Nombre d'élèves parrainés
- Montant généré et payé
- Liste des élèves inscrits via son code

## 🏗️ Architecture

### Structure du projet

```
irl_ad/
├── config/                 # Configuration Django
│   ├── settings.py        # Paramètres globaux
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── partnerships/          # App pour les partenariats
│   ├── models.py          # Library, PartnershipCode, Payment
│   ├── views.py           # Vues admin
│   ├── admin.py           # Interface admin Django
│   ├── urls.py            # URLs partenariats
│   └── templates/         # Templates
├── students/              # App pour les élèves
│   ├── models.py          # Student
│   ├── views.py           # Vues inscription & dashboard
│   ├── forms.py           # Formulaire inscription
│   ├── admin.py           # Interface admin
│   ├── urls.py            # URLs élèves
│   └── templates/         # Templates
├── manage.py
├── Pipfile & Pipfile.lock
└── db.sqlite3             # Base de données
```

### Modèles de données

#### Library (Librairie partenaire)
- `id` (UUID)
- `name` (Nom)
- `email` (Email unique)
- `phone` (Téléphone)
- `contact_person` (Personne de contact)
- `address` (Adresse)
- `commission_per_student` (Commission par élève - défaut: 1000 DA)
- `status` (active, inactive, suspended)
- `created_at` / `updated_at`

#### Student (Élève)
- `id` (UUID)
- `first_name` / `last_name` (Prénom/Nom)
- `email` (Email unique)
- `phone` (Téléphone)
- `library` (ForeignKey vers Library)
- `referral_code` (Code utilisé)
- `level` (1ère, 2e, 3e année)
- `status` (active, inactive, suspended)
- `enrollment_date` (Date d'inscription)
- `created_at` / `updated_at`

#### PartnershipCode (Code de partenariat)
- `id` (UUID)
- `library` (ForeignKey)
- `code` (Code unique - ex. LIB001)
- `is_active` (Actif/Inactif)
- `created_at`

#### Payment (Paiement)
- `id` (UUID)
- `library` (ForeignKey)
- `amount` (Montant)
- `status` (pending, completed, cancelled)
- `reference` (Référence de paiement)
- `notes` (Notes)
- `created_at` / `completed_at`

## 🚀 Installation et démarrage

### 1. Prérequis
- Python 3.11+
- pipenv
- Git

### 2. Installation

```bash
# Cloner le projet
cd "C:\Users\yanis\Documents\Automatisation code\irl_ad"

# Installer les dépendances avec pipenv
pipenv install

# Activer l'environnement virtuel
pipenv shell

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Créer des données de test (optionnel)
python create_test_data.py

# Lancer le serveur de développement
python manage.py runserver
```

### 3. Accès initial

- **Admin Django**: http://localhost:8000/admin/
  - Gérer les librairies
  - Gérer les codes de partenariat
  - Gérer les paiements
  - Gérer les élèves

- **Inscription élèves**: http://localhost:8000/register/
  - Formulaire d'inscription public
  - Validation du code partenaire

- **Dashboard admin**: http://localhost:8000/admin/dashboard/
  - Vue d'ensemble des statistiques
  - Réquiert l'authentification

- **Dashboard librairie**: http://localhost:8000/library/[CODE]/
  - Remplacer [CODE] par le code réel (ex. LIB4F6)
  - Public, pas d'authentification

## 📋 Guide d'utilisation

### Pour l'administrateur

#### 1. Ajouter une librairie partenaire

1. Aller à `/admin/`
2. Cliquer sur "Librairies"
3. Cliquer sur "Ajouter une librairie"
4. Remplir les informations:
   - Nom
   - Email (unique)
   - Téléphone (optionnel)
   - Personne de contact
   - Adresse
   - Commission par élève (défaut: 1000 DA)
5. Sauvegarder
6. Un code partenaire est généré automatiquement

#### 2. Créer un code de partenariat

1. Aller à `/admin/`
2. Cliquer sur "Codes de partenariat"
3. Cliquer sur "Ajouter un code"
4. Choisir la librairie
5. Entrer le code (ex. LIB001)
6. Cocher "Actif"
7. Sauvegarder

#### 3. Gérer les paiements

1. Aller à `/admin/`
2. Cliquer sur "Paiements"
3. Pour ajouter un paiement:
   - Cliquer sur "Ajouter un paiement"
   - Choisir la librairie
   - Entrer le montant
   - Entrer la référence (optionnel)
   - Sauvegarder avec le statut "En attente"

4. Pour marquer comme payé:
   - Sélectionner un ou plusieurs paiements
   - Choisir l'action "Marquer comme complété"
   - Cliquer sur "Exécuter"

#### 4. Suivre les statistiques

1. Aller à `/admin/dashboard/`
2. Consulter:
   - Nombre de librairies actives
   - Nombre d'élèves inscrits
   - Montant total généré
   - Montant total payé
   - Solde restant à payer

### Pour les librairies partenaires

#### 1. Partager son code
- Code unique: ex. `LIB4F6`
- Communiquer ce code aux élèves intéressés

#### 2. Consulter son dashboard
- URL: `http://localhost:8000/library/LIB4F6/` (remplacer par son code)
- Voir:
  - Nombre d'élèves parrainés
  - Montant généré (élèves × commission)
  - Montant payé
  - Solde à recevoir
  - Statut de paiement (Payé / Partiel / Non payé)
  - Liste des élèves inscrits

### Pour les élèves

#### 1. S'inscrire
1. Aller à http://localhost:8000/register/
2. Remplir le formulaire:
   - Prénom
   - Nom
   - Email
   - Téléphone (optionnel)
   - Niveau
   - Code partenaire (obtenu de la librairie)
3. Cliquer sur "S'inscrire"
4. Voir le message de confirmation

## 💾 Données de test

Des données de test sont créées automatiquement avec `create_test_data.py`:

### Librairies créées
- Librairie du Centre (Code: LIB4F6)
- Librairie Educative (Code: LIB2AF)
- Librairie Scolaire Plus (Code: LIBD3B)

### Élèves créés
- Mohamed Bouchema
- Aicha Rezgui
- Omar Karim
- Yasmine Tlemcani
- Karim Bencheikh

## 🔐 Sécurité

### Mesures implémentées
- CSRF protection activée
- Validation des formulaires
- Validation des codes partenaires
- UUIDs pour les IDs (non prévisibles)
- Authentification requise pour le dashboard admin

### À faire pour la production
```python
# config/settings.py
DEBUG = False
ALLOWED_HOSTS = ['votredomaine.com']
SECRET_KEY = 'générer une nouvelle clé'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 Calcul des commissions

### Formule
```
Commission totale = Nombre d'élèves inscrits × Commission par élève
```

### Exemple
- Librairie A a parrainé 10 élèves
- Commission par élève: 1500 DA
- Commission totale: 10 × 1500 = 15 000 DA
- Si 5 000 DA payés: Solde = 10 000 DA

## 🛠️ Technologies utilisées

- **Framework**: Django 5.2
- **Base de données**: SQLite (développement)
- **Template engine**: Django Templates
- **Frontend**: HTML5 + CSS3 (simple et responsive)
- **Python**: 3.11+

## 📝 Notes importantes

### Partitionnement des données
- Chaque librairie voit uniquement ses propres données
- Les élèves sont liés aux librairies par le code utilisé
- Les paiements sont liés aux librairies

### Calculs automatiques
- Les montants sont recalculés en temps réel à partir de:
  - Nombre d'élèves actifs
  - Commission configurée
  - Paiements effectués

### Codes de partenariat
- Peuvent être multiples par librairie
- Peuvent être désactivés sans supprimer les données
- Chaque élève mémorise le code utilisé lors de son inscription

## 🐛 Dépannage

### Erreur: "Code partenaire invalide"
- Vérifier que le code existe dans la base de données
- Vérifier que le code est actif
- Vérifier que la librairie est active

### Erreur: "Email déjà utilisé"
- L'email doit être unique pour les élèves
- L'email doit être unique pour les librairies

### Les données ne s'affichent pas
- Vérifier que les migrations sont appliquées: `python manage.py migrate`
- Vérifier que les données de test sont créées: `python create_test_data.py`

## 🚀 Déploiement

Pour déployer en production:

1. Configurer la base de données (PostgreSQL recommandé)
2. Configurer les variables d'environnement
3. Collecter les fichiers statiques: `python manage.py collectstatic`
4. Utiliser un serveur WSGI (Gunicorn)
5. Configurer un reverse proxy (Nginx)
6. Activer HTTPS et les cookies sécurisés

## 📞 Support

Pour toute question ou bug:
1. Vérifier la documentation
2. Consulter les logs Django
3. Vérifier la base de données dans l'admin

## 📄 Licence

Ce projet est propriétaire et destiné à un usage interne.

## ✅ Checklist de mise en production

- [ ] `DEBUG = False` dans settings.py
- [ ] `SECRET_KEY` changée
- [ ] `ALLOWED_HOSTS` configuré
- [ ] HTTPS activé
- [ ] Base de données configurée (PostgreSQL)
- [ ] Fichiers statiques collectés
- [ ] Logs configurés
- [ ] Sauvegardes quotidiennes activées
- [ ] Moniteurs de performance en place
- [ ] Plan de récupération en cas de sinistre
