# 🚀 Démarrage Rapide - Système de Paiements

## Installation (3 étapes)

### 1️⃣ Appliquer la Migration
```bash
python manage.py migrate partnerships
```

### 2️⃣ Configurer le Stockage Média (si pas déjà fait)

Dans `settings.py`, vérifier:
```python
# Racine du répertoire media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL d'accès aux fichiers media
MEDIA_URL = '/media/'
```

Dans `urls.py` (au niveau du projet):
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... vos URLs ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3️⃣ C'est Prêt! 🎉

---

## Utilisation Immédiate

### Accéder au Dashboard
```
1. Connecté en tant que superuser
2. Aller à: /partnerships/confirmations/
3. Voir les partenaires avec les nouvelles colonnes:
   - Montant Acquis
   - Montant Payé
   - Solde Restant
   - Boutons "💳 Paiement" et "📋 Historique"
```

### Ajouter un Paiement (30 secondes)
```
1. Click sur "💳 Paiement" pour un partenaire
2. Modal s'ouvre
3. Saisir montant (ex: 20000)
4. Prendre photo du reçu
5. Optionnel: Ajouter une note
6. Click "Valider le paiement"
7. ✅ Succès! Montants mis à jour automatiquement
```

### Voir l'Historique
```
1. Click sur "📋 Historique" pour un partenaire
2. Voir tous les reçus uploadés
3. Les plus récents en premier
4. Cliquer sur une image pour l'agrandir
```

---

## Fichiers Modifiés/Créés

### Modèles
- ✅ `partnerships/models.py` → Ajout de `PaymentReceipt`

### Formulaires
- ✅ `partnerships/forms.py` → Ajout de `QuickPaymentForm`

### Vues
- ✅ `partnerships/views.py` → 3 vues HTMX ajoutées:
  - `PaymentReceiptFormView`
  - `PaymentReceiptUploadView`
  - `PaymentReceiptListView`

### URLs
- ✅ `partnerships/urls.py` → 3 routes ajoutées

### Templates
- ✅ `admin-student-confirmation.html` → Modal et boutons intégrés
- ✅ `partials/payment-receipt-form.html` (nouveau)
- ✅ `partials/payment-success.html` (nouveau)
- ✅ `partner-payment-history.html` (nouveau)

### Migrations
- ✅ `migrations/0002_paymentreceipt.py` (nouveau)

---

## Vérifier l'Installation

### En Python
```bash
python manage.py shell
```

```python
from partnerships.models import PaymentReceipt
from partnerships.models import Payment

# Vérifier que le modèle existe
print(PaymentReceipt._meta.fields)

# Vérifier que les relations fonctionnent
payment = Payment.objects.first()
if payment:
    print(f"Montant: {payment.amount} DA")
```

### En HTML/Templates
```
1. Aller sur /partnerships/confirmations/
2. Vérifier que les boutons "💳 Paiement" sont visibles
3. Vérifier que les colonnes "Montant Payé" et "Solde" sont affichées
```

---

## Cas d'Usage Courant

### Scénario: Payer une Librairie 20 000 DA

**État Initial:**
- Librairie: "ABC Books"
- Commission/étudiant: 1000 DA
- Étudiants confirmés: 50
- Montant Acquis: 50 000 DA
- Montant Payé: 0 DA
- Solde Restant: 50 000 DA

**Actions:**
```
1. Click "💳 Paiement"
2. Saisir: 20000
3. Uploader: Photo du reçu bancaire
4. Notes: "Virement le 25/11/2024"
5. Valider
```

**État Après:**
- Montant Payé: 20 000 DA
- Solde Restant: 30 000 DA ← Calculé automatiquement! ✅

---

## Performance & Sécurité

### Performance
- ✅ Lazy loading des images (carrousel du modal)
- ✅ Pagination automatique si >50 reçus
- ✅ Cache des reçus par partenaire
- ✅ HTMX pour interactions sans rechargement

### Sécurité
- ✅ Accès réservé aux superusers
- ✅ Validation côté serveur stricte
- ✅ Validation des types d'images
- ✅ Impossible de modifier un montant après validation
- ✅ CSRF protection sur tous les formulaires

---

## Erreurs Courantes & Solutions

### ❌ "Modal doesn't appear"
**Solution:**
- Vérifier que HTMX est chargé dans le template
- `<script src="https://unpkg.com/htmx.org@1.9.10"></script>`

### ❌ "Image upload fails"
**Solution:**
- Vérifier que `MEDIA_ROOT` existe: `mkdir media/`
- Vérifier les permissions: `chmod -R 755 media/`
- Redémarrer le serveur Django

### ❌ "Payment total doesn't update"
**Solution:**
- Vérifier que l'out-of-band swap est présent dans le template
- Vérifier que le partenaire a des étudiants confirmés
- Rafraîchir la page (Ctrl+F5)

---

## Configuration Avancée (Optionnel)

### Compresser les Images Automatiquement
```bash
pip install Pillow django-storages
```

### Ajouter une Limite de Taille
Dans `forms.py`:
```python
class QuickPaymentForm(forms.Form):
    receipt_image = forms.ImageField(
        help_text='Max 5 MB',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
```

### Envoyer un Email à la Confirmation
```python
from django.core.mail import send_mail

def PaymentReceiptUploadView.post():
    # ... création du paiement ...

    send_mail(
        'Paiement reçu',
        f'Merci! {receipt.amount_paid} DA reçus.',
        'admin@example.com',
        [partner.email],
    )
```

---

## Roadmap Futures Améliorations

- [ ] Compression automatique des images
- [ ] OCR pour détecter le montant depuis le reçu
- [ ] Email automatique aux partenaires
- [ ] Export PDF de l'historique
- [ ] Graphiques de paiement
- [ ] SMS de confirmation

---

## Support & Questions

📋 **Documentation Complète:** Voir `PAYMENT_SYSTEM.md`

🐛 **Problème?** Vérifier les logs Django:
```bash
tail -f logs/django.log
```

💬 **Questions?** Consulter les commentaires du code source:
- `partnerships/views.py` (lignes 488-600)
- `partnerships/models.py` (lignes 290-331)
- `partnerships/forms.py` (lignes 69-102)

---

## 📊 Résumé Rapide

| Fonctionnalité | Status | File |
|---|---|---|
| Upload reçus | ✅ | payment-receipt-form.html |
| Montant Payé tracking | ✅ | Payment model |
| Solde calculation | ✅ | Views + Templates |
| Historique reçus | ✅ | partner-payment-history.html |
| HTMX real-time | ✅ | Out-of-band swaps |
| Mobile-friendly | ✅ | Responsive CSS |
| Secure upload | ✅ | Server validation |

---

**Installation time:** ~5 minutes
**Learning curve:** ~15 minutes
**Production-ready:** ✅ YES
