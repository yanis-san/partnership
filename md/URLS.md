# Endpoints et URLs

## URLs Publiques (sans authentification)

### Inscription Élèves
```
GET  /register/
POST /register/
```
- Formulaire d'inscription des élèves
- Validation du code partenaire
- Redirection vers page de confirmation

**Exemple:**
```
http://localhost:8000/register/
```

### Page de Confirmation
```
GET /registration-success/
```
- Affiche les détails de l'inscription
- Montre la librairie associée

**Exemple:**
```
http://localhost:8000/registration-success/
```

### Dashboard Librairie
```
GET /library/<code>/
```
- Vue publique pour les librairies
- Pas d'authentification requise
- Affiche les statistiques de la librairie

**Variables:**
- `<code>`: Code partenaire (ex. LIB4F6)

**Exemples:**
```
http://localhost:8000/library/LIB4F6/
http://localhost:8000/library/LIB2AF/
http://localhost:8000/library/LIBD3B/
```

## URLs Authentifiées (admin)

### Admin Principal
```
GET /admin/
```
- Interface d'administration Django
- Nécessite login

**Accès:**
```
http://localhost:8000/admin/
```

### Gestion des Librairies
```
GET  /admin/partnerships/library/
GET  /admin/partnerships/library/<id>/
POST /admin/partnerships/library/add/
POST /admin/partnerships/library/<id>/change/
```

### Gestion des Codes
```
GET  /admin/partnerships/partnershipcode/
GET  /admin/partnerships/partnershipcode/<id>/
POST /admin/partnerships/partnershipcode/add/
POST /admin/partnerships/partnershipcode/<id>/change/
```

### Gestion des Paiements
```
GET  /admin/partnerships/payment/
GET  /admin/partnerships/payment/<id>/
POST /admin/partnerships/payment/add/
POST /admin/partnerships/payment/<id>/change/
```

**Avec actions:**
- Marquer comme complété
- Marquer comme en attente

### Gestion des Élèves
```
GET  /admin/students/student/
GET  /admin/students/student/<id>/
POST /admin/students/student/add/
POST /admin/students/student/<id>/change/
```

### Dashboard Admin
```
GET /admin/dashboard/
```
- Vue d'ensemble des statistiques
- Listes filtrées
- Paiements récents
- Élèves récents

**Authentification requise**

**Exemple:**
```
http://localhost:8000/admin/dashboard/
```

## Paramètres Communs

### Filtrage (dans l'admin)
```
?status=active
?created_at__gte=2024-01-01
?library__name__icontains=Centre
```

### Recherche (dans l'admin)
Utiliser la barre de recherche:
- **Librairies**: Nom, Email, Personne de contact
- **Codes**: Code, Nom de librairie
- **Paiements**: Nom librairie, Référence
- **Élèves**: Nom, Email, Code utilisé

### Tri
Cliquer sur les en-têtes de colonne dans l'admin

## Structure Hiérarchique

```
/
├── register/                              [PUBLIC]
│   ├── GET: Affiche formulaire
│   └── POST: Traite l'inscription
├── registration-success/                  [PUBLIC]
│   └── GET: Page de confirmation
├── library/<code>/                        [PUBLIC]
│   └── GET: Dashboard librairie
├── admin/                                 [AUTHENTIFIÉ]
│   ├── dashboard/                         [Vue personnalisée]
│   ├── partnerships/
│   │   ├── library/                      [CRUD]
│   │   ├── partnershipcode/              [CRUD]
│   │   └── payment/                      [CRUD + Actions]
│   ├── students/
│   │   └── student/                      [CRUD]
│   ├── auth/
│   │   ├── user/
│   │   └── group/
│   └── ...autres apps Django...
```

## Codes HTTP Attendus

### Succès
- `200 OK`: Requête réussie
- `201 Created`: Ressource créée
- `204 No Content`: Suppression réussie

### Erreurs Courantes
- `400 Bad Request`: Données invalides (inscription)
- `403 Forbidden`: Pas d'authentification (admin)
- `404 Not Found`: Ressource inexistante
- `500 Server Error`: Erreur serveur

## Exemples de Requêtes

### Inscrire un élève
```bash
POST /register/
Content-Type: application/x-www-form-urlencoded

first_name=Ahmed&last_name=Benameur&email=ahmed@example.com&phone=0671234567&level=1st_year&referral_code=LIB4F6
```

### Voir le dashboard d'une librairie
```bash
GET /library/LIB4F6/
```

### Connexion admin
```bash
GET /admin/
POST /admin/login/ (avec credentials)
```

## Statuts Disponibles

### Librairies
- `active`: Librairie active
- `inactive`: Librairie inactive
- `suspended`: Librairie suspendue

### Élèves
- `active`: Élève actif
- `inactive`: Élève inactif
- `suspended`: Élève suspendu

### Paiements
- `pending`: Paiement en attente
- `completed`: Paiement effectué
- `cancelled`: Paiement annulé

## Notes Importantes

- Tous les codes de partenariat sont en majuscules
- Les emails doivent être uniques (librairies et élèves)
- Les IDs sont des UUIDs (pas de prédiction possible)
- Les dates sont en UTC par défaut
- Les montants sont en Dinars Algériens (DA)

## Exemple de Flux Complet

1. **Administrateur crée une librairie**
   ```
   /admin/partnerships/library/add/
   → Créée avec code auto: LIB4F6
   ```

2. **Élève s'inscrit via le code**
   ```
   /register/
   POST: referral_code=LIB4F6
   → Redirection vers /registration-success/
   ```

3. **Librairie consulte ses stats**
   ```
   /library/LIB4F6/
   → Affiche: 1 élève, 1500 DA générés
   ```

4. **Admin crée un paiement**
   ```
   /admin/partnerships/payment/add/
   POST: library=LIB4F6, amount=1500
   ```

5. **Admin marque comme payé**
   ```
   /admin/partnerships/payment/
   Sélectionner paiement → "Marquer comme complété"
   ```

6. **Librairie voit le paiement confirmé**
   ```
   /library/LIB4F6/
   → Affiche: "Payé" comme statut
   ```
