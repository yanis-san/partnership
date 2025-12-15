# URLs Simplifiees du Systeme

## Pages Principales

### Accueil
```
http://localhost:8000/
```
- Vue d'ensemble du systeme
- Liens vers inscription et dashboards
- Instructions

### Inscription des Eleves
```
http://localhost:8000/register/
```
- Formulaire d'inscription
- Validation du code partenaire
- Redirection vers confirmation

### Confirmation d'Inscription
```
http://localhost:8000/register/success/
```
- Affichage des donnees de l'eleve
- Confirmation de l'inscription

### Dashboard Librairie (Public - Pas de Login)
```
http://localhost:8000/dashboard/library/LIB4F6/
http://localhost:8000/dashboard/library/LIB2AF/
http://localhost:8000/dashboard/library/LIBD3B/
```
- Vue publique de la librairie
- Ses statistiques
- Ses eleves
- Statut de paiement
- Pas d'authentification requise

### Dashboard Admin (Authentification Requise)
```
http://localhost:8000/dashboard/admin/
```
- Statistiques globales
- Tableaux des librairies
- Paiements recents
- Eleves recents
- Acces a l'admin Django complet

### Admin Django Complet
```
http://localhost:8000/admin/
```
- Interface complete pour tout gerer
- Creer/modifier/supprimer librairies
- Creer/modifier/supprimer codes
- Creer/modifier paiements
- Lister tous les eleves

---

## Codes de Test

```
LIB4F6 - Librairie du Centre (Commission: 1500 DA)
LIB2AF - Librairie Educative (Commission: 1200 DA)
LIBD3B - Librairie Scolaire Plus (Commission: 1000 DA)
```

## Credentials

```
Username: admin
Password: admin123
```

---

## Exemples d'Utilisation

### 1. Aller a l'Accueil
Cliquez sur "Affiliation Librairies" dans le menu

### 2. S'inscrire Comme Eleve
- Cliquez sur "Inscription"
- Remplissez le formulaire
- Utilisez le code: LIB4F6
- Soumettez
- Vous voyez la confirmation

### 3. Voir le Dashboard d'une Librairie
- Cliquez sur le lien dans l'accueil
- Ou allez a: http://localhost:8000/dashboard/library/LIB4F6/
- Vous voyez:
  - Nombre d'eleves
  - Montant genere
  - Montant paye
  - Solde a recevoir

### 4. Gerer l'Admin
- Cliquez sur "Admin" dans le menu
- Authentifiez-vous (admin / admin123)
- Cliquez sur "Librairies" pour les gerer
- Cliquez sur "Eleves" pour les voir
- Cliquez sur "Paiements" pour creer des paiements

### 5. Voir le Dashboard Admin
- Allez a: http://localhost:8000/dashboard/admin/
- Vous voyez:
  - Vue d'ensemble globale
  - Toutes les librairies et leurs stats
  - Paiements recents
  - Eleves recents

---

## Navigation Simplifiee

```
ACCUEIL (/)
  ├── Inscription Eleves (/register/)
  │    └── Confirmation (/register/success/)
  │
  ├── Dashboard Librairie (/dashboard/library/[CODE]/)
  │
  ├── Admin Django (/admin/)
  │    ├── Librairies
  │    ├── Codes
  │    ├── Paiements
  │    └── Eleves
  │
  └── Dashboard Admin (/dashboard/admin/)
       ├── Statistiques
       ├── Librairies
       ├── Paiements
       └── Eleves
```

---

## Menu Visible sur Chaque Page

```
+----------------------------------------------+
| Affiliation Librairies                       |
| Systeme de suivi pour les partenaires        |
+----------------------------------------------+
| Accueil | Inscription | Admin                |
+----------------------------------------------+
```

---

## Taches Courantes

### Ajouter une Librairie
1. Aller a /admin/
2. Cliquer "Librairies"
3. Cliquer "Ajouter"
4. Remplir et sauvegarder
5. Code genere automatiquement

### Creer un Paiement
1. Aller a /admin/
2. Cliquer "Paiements"
3. Cliquer "Ajouter"
4. Choisir librairie et montant
5. Sauvegarder

### Marquer un Paiement comme Complete
1. Aller a /admin/partnerships/payment/
2. Selectionner les paiements
3. Choisir action "Marquer comme complete"
4. Cliquer "Executer"

### Consulter le Dashboard d'une Librairie
1. Aller a /dashboard/library/LIB4F6/
2. Remplacer LIB4F6 par le code reel
3. Voir stats, eleves, etc.

### Voir les Eleves d'une Librairie
1. Aller a /dashboard/library/[CODE]/
2. Voir la liste des eleves inscrits
3. Voir leurs details (email, niveau, date)

---

## Erreurs Courantes et Solutions

### "Code partenaire invalide"
- Verifier le code est correct
- Codes disponibles: LIB4F6, LIB2AF, LIBD3B

### "Email deja utilise"
- Utiliser un email different
- Chaque email doit etre unique

### "Acces refuse" en admin
- Se connecter d'abord: /admin/
- Login: admin / admin123

### Dashboard admin vide
- Verifier les donnees de test sont creees
- Lancer: `pipenv run python create_test_data.py`

---

## Notes Importantes

- Codes sont toujours en MAJUSCULES
- Emails doivent etre uniques
- Commissions en Dinars Algeriens (DA)
- Les montants se recalculent automatiquement
- Pas besoin de login pour consulter le dashboard librairie
- Login requis pour l'admin et le dashboard admin
