# DEMARRER ICI

## 1. Lancer le Serveur

```bash
cd "C:\Users\yanis\Documents\Automatisation code\irl_ad"
pipenv shell
python manage.py runserver
```

Le serveur démarre sur: **http://localhost:8000**

## 2. Pages Principales

### ACCUEIL
```
http://localhost:8000/
```
Menu simple avec les 3 options principales

### INSCRIPTION DES ELEVES
```
http://localhost:8000/register/
```
Formulaire d'inscription avec codes de test:
- LIB4F6 (Librairie du Centre)
- LIB2AF (Librairie Educative)
- LIBD3B (Librairie Scolaire Plus)

### DASHBOARD LIBRAIRIE
```
http://localhost:8000/dashboard/library/LIB4F6/
```
Remplacez `LIB4F6` par n'importe quel autre code
- Voir les eleves inscrits
- Voir les gains generés
- Voir les paiements reçus
- Statut de paiement

### DASHBOARD ADMIN
```
http://localhost:8000/dashboard/admin/
```
**Authentification requise** (admin / admin123)
- Vue d'ensemble globale
- Toutes les librairies
- Paiements recents
- Eleves recents

### ADMIN DJANGO COMPLET
```
http://localhost:8000/admin/
```
Pour gerer tout en détail:
- Creer/modifier librairies
- Creer/modifier codes
- Creer/modifier paiements
- Lister tous les eleves

---

## 3. Menu de Navigation

En haut de chaque page:
```
[Affiliation Librairies]
System de suivi pour les partenaires

[ Accueil ] [ Inscription ] [ Admin ]
```

---

## 4. Donnees de Test

### Librairies
```
LIB4F6 - Librairie du Centre (1500 DA/eleve)
LIB2AF - Librairie Educative (1200 DA/eleve)
LIBD3B - Librairie Scolaire Plus (1000 DA/eleve)
```

### Credentials Admin
```
Username: admin
Password: admin123
```

---

## 5. Exemple Complet

### Etape 1: Allez a l'Accueil
```
http://localhost:8000/
```
Vous voyez le menu principal

### Etape 2: Inscrivez un Eleve
```
http://localhost:8000/register/
```
- Prenom: Ahmed
- Nom: Benali
- Email: ahmed@example.com
- Telephone: 0671234567
- Niveau: 1ère année
- Code: LIB4F6
- Cliquez "S'inscrire"

### Etape 3: Confirmez l'Inscription
Vous voyez la page de confirmation avec tous les details

### Etape 4: Consultez le Dashboard Librairie
```
http://localhost:8000/dashboard/library/LIB4F6/
```
Vous voyez:
- 1 eleve inscrit (Ahmed Benali)
- 1500 DA generes
- 0 DA payes
- 1500 DA a recevoir
- Statut: EN ATTENTE

### Etape 5: Allez a l'Admin
```
http://localhost:8000/admin/
```
- Username: admin
- Password: admin123

### Etape 6: Creer un Paiement
1. Cliquez "Paiements"
2. Cliquez "Ajouter un paiement"
3. Librairie: Librairie du Centre
4. Montant: 1500
5. Cliquez "Sauvegarder"
6. Choisissez l'action "Marquer comme complet"
7. Cliquez "Executer"

### Etape 7: Verifiez le Dashboard Librairie
```
http://localhost:8000/dashboard/library/LIB4F6/
```
Vous voyez maintenant:
- 1500 DA payes
- 0 DA a recevoir
- Statut: PAYE ✓

---

## 6. Structure des URLs

```
/                               = Accueil
/register/                      = Inscription eleve
/register/success/              = Confirmation inscription
/dashboard/library/[CODE]/      = Dashboard librairie
/dashboard/admin/               = Dashboard admin (login requis)
/admin/                         = Admin Django complet
```

---

## 7. Ce qui Marche

✅ Formulaire d'inscription avec validation
✅ Pages simples et fonctionnelles
✅ Navigation claire au menu
✅ Dashboard librairie publique
✅ Dashboard admin avec authentification
✅ Admin Django complet et personnalisé
✅ Calculs automatiques des commissions
✅ CSS simple inclus dans les templates
✅ Base de donnees avec donnees de test

---

## 8. Taches Courantes

### Ajouter une Librairie
1. /admin/ → Librairies → Ajouter
2. Remplir les infos
3. Sauvegarder → Code genere auto

### Creer un Code Supplementaire
1. /admin/ → Codes de partenariat → Ajouter
2. Choisir une librairie
3. Entrer le code (ex: LIB-PROMO-001)
4. Cocher "Actif"
5. Sauvegarder

### Voir les Eleves d'une Librairie
1. /dashboard/library/[CODE]/
2. Voir la liste des eleves en bas

### Marquer un Paiement comme Complete
1. /admin/partnerships/payment/
2. Selectionner le paiement
3. Choisir action "Marquer comme complete"
4. Cliquer "Executer"

---

## 9. Erreurs Frequentes

**"Code partenaire invalide"**
- Verifier le code: LIB4F6, LIB2AF ou LIBD3B

**"Email deja utilise"**
- Utiliser un email different

**"Acces refuse" en admin**
- Se connecter d'abord (/admin/)
- admin / admin123

---

## 10. Besoin d'Aide?

1. Verifier URLS_SIMPLES.md pour la liste complete des URLs
2. Verifier README.md pour la documentation technique
3. Verifier QUICKSTART.md pour les commandes utiles

---

## C'est Pret! 🚀

Le systeme est **completement fonctionnel** et **pret a etre utilise**!

Lancez le serveur et testez!
