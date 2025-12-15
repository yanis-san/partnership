# 💳 Système de Gestion des Paiements avec Reçus

## Vue d'ensemble

Système professionnel et transparent pour gérer les paiements aux partenaires avec:
- ✅ Upload facile des photos de reçus
- 📊 Suivi des montants acquis vs payés (Solde = Acquis - Payé)
- 🔄 Mise à jour en temps réel via HTMX
- 📋 Historique complet des paiements par partenaire
- 🎯 Transparence totale: pas d'accumulation d'erreurs entre cycles

---

## Architecture du Système

### 1. Modèles Django

#### `Payment` (modèle existant amélioré)
```python
- amount: Montant du paiement en DA
- status: pending | partial | completed | cancelled
- reference: Référence du paiement
- notes: Notes additionnelles
- completed_at: Date de complétion
- remaining_amount: Calculé automatiquement
```

#### `PaymentReceipt` (nouveau modèle)
```python
- payment: OneToOneField vers Payment (le reçu est lié à un paiement unique)
- receipt_image: ImageField pour stocker la photo du reçu
  - Stockage: media/receipts/YYYY/MM/DD/
  - Support: Tous les formats image (JPEG, PNG, etc.)
  - Mobile-friendly: Accès direct à la caméra

- amount_paid: Montant saisi lors de l'upload
- notes: Notes optionnelles (mode de paiement, date, etc.)
- created_at: Date d'upload
- updated_at: Date de modification
```

---

## 2. Formulaires

### `QuickPaymentForm`
Formulaire simplifié pour saisie rapide:
```python
Fields:
  - amount_paid (Décimal, obligatoire): Montant en DA
  - receipt_image (ImageField, obligatoire): Photo du reçu
  - notes (CharField, optionnel): Notes texte
```

**Caractéristiques:**
- Champ montant avec validation décimale
- Upload d'image avec accès caméra sur mobile (capture='environment')
- Largement stylisé pour une expérience mobile optimale

---

## 3. Vues HTMX

### `PaymentReceiptFormView` (GET)
**URL:** `/partnerships/payment-form/<partner_id>/`
- Affiche le formulaire d'upload du reçu
- Template: `partials/payment-receipt-form.html`
- Requête: HTMX GET depuis le modal
- Réponse: HTML du formulaire

### `PaymentReceiptUploadView` (POST)
**URL:** `/partnerships/payment-upload/<partner_id>/`
- Traite l'upload du reçu
- Crée un Payment et un PaymentReceipt
- Recalcule les montants du partenaire

**Logique:**
1. Valide le formulaire (montant + image)
2. Crée un Payment avec status=COMPLETED
3. Crée un PaymentReceipt associé
4. Recalcule: paid_amount, solde = confirmed_amount - paid_amount
5. Retourne template de succès avec mise à jour HTMX out-of-band

**Réponse:**
- Template principal: `partials/payment-success.html` (remplace le formulaire)
- Out-of-band swap: Met à jour les totaux du partenaire dans le dashboard

### `PaymentReceiptListView` (GET)
**URL:** `/partnerships/payment-history/<partner_id>/`
- Affiche l'historique complet des reçus
- Template: `partner-payment-history.html`
- Récupère: Tous les reçus du partenaire (triés par date décroissante)
- Affiche le dernier reçu en évidence

---

## 4. Templates

### `partials/payment-receipt-form.html`
**Contenu:**
- Header avec titre et description
- Affichage des erreurs s'il y en a
- Formulaire HTMX avec:
  - Champ montant avec unité DA
  - Upload d'image avec zone de drop
  - Champ notes optionnel
  - Boutons: Valider / Annuler
- CSS custom pour styling mobile-first

**HTMX:**
```html
<form hx-post="{% url 'payment-receipt-upload' partner.id %}"
      hx-target=".modal-content"
      hx-swap="innerHTML"
      enctype="multipart/form-data">
```

### `partials/payment-success.html`
**Contenu:**
- Message de succès avec montant affiché
- Aperçu du reçu uploadé
- Infos mises à jour (Acquis, Payé, Solde)
- Boutons d'actions:
  - Voir l'historique complet
  - Ajouter un autre paiement
  - Retour au dashboard
- **Out-of-band swap:** Met à jour automatiquement les totaux du partenaire dans le dashboard

**HTMX Oob Swap:**
```html
<div id="partner-{{ partner.id }}-totals"
     hx-swap-oob="true"
     class="partner-header">
  <!-- Totaux mis à jour -->
</div>
```

### `partner-payment-history.html`
**Contenu (page complète):**
- Header avec info partenaire
- Cartes récapitulatives (Acquis, Payé, Solde, Nb reçus)
- Liste des reçus en cartes:
  - En-tête avec numéro et date
  - Image du reçu
  - Détails: Montant, Date, Statut
  - Notes optionnelles
- Le dernier reçu affiché en premier

---

## 5. Flow HTMX Complet

### Étape 1: Afficher le formulaire
```
Utilisateur click "💳 Paiement"
  ↓
hx-get="{% url 'payment-receipt-form' %}"
  ↓
PaymentReceiptFormView.get()
  ↓
Retourne: partials/payment-receipt-form.html
  ↓
hx-target=".modal-content"
  ↓
Le formulaire s'affiche dans le modal
```

### Étape 2: Upload du reçu
```
Utilisateur saisit montant + image + click "Valider"
  ↓
hx-post="{% url 'payment-receipt-upload' %}"
enctype="multipart/form-data"
  ↓
PaymentReceiptUploadView.post()
  ↓
✅ Valide et crée Payment + PaymentReceipt
  ↓
Retourne: partials/payment-success.html
  ↓
hx-target=".modal-content"
hx-swap="innerHTML"
  ↓
Le succès s'affiche dans le modal
+ Out-of-band: Totaux du partenaire mis à jour dans le dashboard 🔄
```

### Étape 3: Voir l'historique
```
Depuis success.html, click "Voir l'historique complet"
  ↓
hx-get="{% url 'payment-history' %}"
  ↓
PaymentReceiptListView.get_context_data()
  ↓
Récupère tous les reçus du partenaire
  ↓
Retourne: partner-payment-history.html (version mobile du modal)
  ↓
hx-target=".modal-content"
hx-swap="innerHTML"
  ↓
L'historique s'affiche dans le modal
```

---

## 6. Intégration dans le Dashboard

### Boutons dans `admin-student-confirmation.html`

Dans le `partner-header`:
```html
<div class="stat-block payment-actions">
    <button class="btn-payment"
            hx-get="{% url 'payment-receipt-form' partner.id %}"
            hx-target="#payment-modal"
            hx-swap="innerHTML">
        💳 Paiement
    </button>
    <button class="btn-history"
            hx-get="{% url 'payment-history' partner.id %}"
            hx-target="#payment-modal"
            hx-swap="innerHTML">
        📋 Historique
    </button>
</div>
```

### Modal Container
```html
<div id="payment-modal" class="payment-modal">
    <div class="modal-backdrop"></div>
    <div class="modal-content">
        <!-- Contenu chargé dynamiquement via HTMX -->
    </div>
</div>
```

**JavaScript pour ouvrir/fermer le modal:**
```javascript
document.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target.id === 'payment-modal') {
        document.getElementById('payment-modal').style.display = 'flex';
    }
});
```

---

## 7. Calcul Transparent des Montants

### Formules

```
Montant Acquis = commission_per_student × nombre_students_confirmés

Montant Payé = SUM(Payment.amount WHERE status='completed')

Solde Restant = Montant Acquis - Montant Payé
```

### Exemple
```
Partner: Librairie ABC
Commission/étudiant: 1000 DA
Étudiants confirmés: 50
→ Montant Acquis = 50,000 DA

Paiements reçus:
  - 1er reçu: 20,000 DA (20/11/2024)
  - 2e reçu: 15,000 DA (25/11/2024)
→ Montant Payé = 35,000 DA

Solde Restant = 50,000 - 35,000 = 15,000 DA
```

---

## 8. URLs Django

```python
# Formulaire pour ajouter un paiement
path('payment-form/<uuid:partner_id>/',
     PaymentReceiptFormView.as_view(),
     name='payment-receipt-form')

# Upload du reçu
path('payment-upload/<uuid:partner_id>/',
     PaymentReceiptUploadView.as_view(),
     name='payment-receipt-upload')

# Historique des paiements
path('payment-history/<uuid:partner_id>/',
     PaymentReceiptListView.as_view(),
     name='payment-history')
```

---

## 9. Stockage des Fichiers

### Structure des répertoires
```
media/
└── receipts/
    └── 2024/
        ├── 11/
        │   ├── 20/
        │   │   ├── receipt_xxx.jpg
        │   │   └── receipt_yyy.png
        │   └── 25/
        │       └── receipt_zzz.jpg
        └── 12/
            └── 01/
                └── receipt_aaa.jpg
```

**Pattern:** `receipts/%Y/%m/%d/` (Auto-organisé par date)

### Sécurité
- Validation d'image côté serveur
- Pas d'exécution possible de code
- Accès restreint aux superusers

---

## 10. Guide d'Utilisation Admin

### Ajouter un Paiement (Flux Complet)

1. **Accéder au dashboard:**
   ```
   Connecté en tant que superuser
   → Aller à /partnerships/confirmations/
   ```

2. **Localiser le partenaire:**
   ```
   Scroll jusqu'à trouver le partenaire
   Voir ses totaux (Acquis, Payé, Solde)
   ```

3. **Cliquer sur "💳 Paiement":**
   ```
   Modal s'ouvre avec le formulaire
   ```

4. **Remplir le formulaire:**
   ```
   Saisir montant (ex: 20000 DA)
   Prendre/télécharger photo du reçu
   Optionnel: Ajouter notes (ex: "Virement SGAB le 25/11/2024")
   Click "Valider le paiement"
   ```

5. **Confirmation:**
   ```
   ✅ Message de succès avec montant
   Aperçu du reçu uploadé
   Totaux mis à jour en temps réel dans le dashboard (out-of-band)
   ```

### Consulter l'Historique

**Option 1: Depuis le succès**
```
Après ajout d'un paiement
→ Click "Voir l'historique complet"
→ Page avec tous les reçus
```

**Option 2: Directement**
```
Click "📋 Historique" depuis le dashboard
→ Voir tous les reçus du partenaire
→ Le plus récent affiché en premier
```

### Télécharger les Reçus

Les reçus sont accessibles directement:
```
URL: /media/receipts/2024/11/20/receipt_xxx.jpg
Depuis l'historique: Cliquer sur l'image
```

---

## 11. Avantages du Système

✅ **Transparence Complète**
- Distinction claire: Montant Acquis vs Montant Payé
- Solde auto-calculé sans erreur
- Pas de confusion entre cycles

✅ **Facilité d'Utilisation**
- Formulaire minimaliste et mobile-friendly
- Accès direct à la caméra sur mobile
- Un clic pour payer, deux pour vérifier

✅ **Traçabilité**
- Chaque paiement est lié à un reçu physique
- Photo de preuve stockée en sécurité
- Historique complet par partenaire

✅ **Mise à Jour Instantanée**
- HTMX: Aucun rafraîchissement de page
- Out-of-band: Les totaux se mettent à jour instantanément
- Expérience utilisateur fluide et professionnelle

✅ **Sécurité**
- Accès réservé aux superusers
- Validation serveur stricte
- Pas de modification possible des montants après saisie

---

## 12. Installation et Migration

### Appliquer la migration
```bash
python manage.py migrate partnerships
```

### Vérifier l'installation
```bash
python manage.py shell
>>> from partnerships.models import PaymentReceipt
>>> PaymentReceipt.objects.all()
# Devrait retourner une queryset vide (ok)
```

---

## 13. Dépannage

### Problème: L'image ne s'upload pas
**Solution:**
- Vérifier que `MEDIA_ROOT` et `MEDIA_URL` sont configurés dans settings.py
- Vérifier les permissions du répertoire `media/`

### Problème: Le modal ne s'affiche pas
**Solution:**
- Vérifier que HTMX est chargé: `<script src="https://unpkg.com/htmx.org@1.9.10"></script>`
- Vérifier la console JS pour les erreurs

### Problème: Les totaux ne se mettent pas à jour
**Solution:**
- Vérifier que l'out-of-band swap a le bon ID: `id="partner-{{ partner.id }}-totals"`
- Vérifier que `hx-swap-oob="true"` est présent
- Vérifier la console HTMX pour les requêtes

---

## 14. Améliorations Futures

- 📱 Compression d'images automatique
- 🔍 OCR pour extraire le montant depuis la photo
- 📧 Email automatique au partenaire lors d'un paiement
- 📊 Statistiques et graphiques de paiement
- 🏷️ Tags et catégorisation des paiements
- 💾 Export PDF de l'historique par partenaire

---

## 📝 Résumé Technique

| Composant | Fichier | Type |
|-----------|---------|------|
| Modèle | `partnerships/models.py` | Python (PaymentReceipt) |
| Formulaire | `partnerships/forms.py` | Python (QuickPaymentForm) |
| Vues | `partnerships/views.py` | Python (3 vues) |
| URLs | `partnerships/urls.py` | Python (3 routes) |
| Formulaire HTML | `partials/payment-receipt-form.html` | Template |
| Succès | `partials/payment-success.html` | Template |
| Historique | `partner-payment-history.html` | Template |
| Migration | `migrations/0002_paymentreceipt.py` | Django |
| Integration | `admin-student-confirmation.html` | Template |

**Total: 9 fichiers modifiés/créés, ~1500 lignes de code**
