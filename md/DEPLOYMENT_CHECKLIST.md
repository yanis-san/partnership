# ✅ Checklist de Déploiement - Système de Paiements v2.0

## 📋 Avant de Déployer

### Étape 1: Vérifier les Fichiers Modifiés ✏️
```bash
# Vérifier les 3 fichiers Python/templates modifiés existent
ls -la partnerships/forms.py
ls -la partnerships/views.py
ls -la partnerships/templates/partnerships/partials/payment-success.html

# Tous les 3 doivent exister: OK
# ✅ Continuer
```

### Étape 2: Vérifier la Syntaxe Python
```bash
cd /chemin/vers/irl_ad
python -m py_compile partnerships/forms.py
python -m py_compile partnerships/views.py

# Doit retourner rien (pas d'erreur)
# ✅ Continuer
```

### Étape 3: Vérifier la Configuration Django
```bash
python manage.py check

# Doit afficher:
# System check identified no issues (0 silenced).
# ✅ Continuer
```

---

## 📁 Préparation de l'Environnement

### Étape 4: Créer les Dossiers de Stockage
```bash
# Créer les répertoires media
mkdir -p media/receipts/
mkdir -p logs/

# Configurer les permissions
chmod -R 755 media/
chmod -R 755 logs/

# Vérifier
ls -la media/receipts/
# Doit afficher: drwxr-xr-x
# ✅ Continuer
```

### Étape 5: Vérifier settings.py
```python
# Vérifier que settings.py contient:

# 1. MEDIA_ROOT et MEDIA_URL
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 2. DEBUG = True (ou urlpatterns configurées pour static())

# 3. Dans urls.py principal:
from django.conf.urls.static import static
urlpatterns = [...]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Test:
```bash
python manage.py shell
>>> from django.conf import settings
>>> settings.MEDIA_ROOT
'/full/path/to/media'  # ✅ Doit être un chemin absolu

>>> settings.MEDIA_URL
'/media/'  # ✅ Doit être /media/

>>> import os
>>> os.path.exists(settings.MEDIA_ROOT)
True  # ✅ Doit exister
```

---

## 🗄️ Base de Données

### Étape 6: Vérifier les Migrations
```bash
# Lister les migrations appliquées
python manage.py showmigrations partnerships

# Doit afficher "0001_initial" et "0002_paymentreceipt" comme [X]
# Si ce n'est pas le cas:
python manage.py migrate partnerships

# Vérifier que les modèles existent
python manage.py shell
>>> from partnerships.models import PaymentReceipt, Payment
>>> PaymentReceipt._meta.get_field('receipt_image')
<ImageField>  # ✅ Doit exister
```

### Étape 7: Test Rapide du Modèle
```bash
python manage.py shell
>>> from partnerships.models import Partner, Payment, PaymentReceipt
>>> from partnerships.forms import QuickPaymentForm

# Vérifier que QuickPaymentForm a les validateurs
>>> f = QuickPaymentForm()
>>> f.fields['receipt_image'].validators
[<FileExtensionValidator>, <function validate_image_size>]
# ✅ Doit avoir les 2 validateurs
```

---

## 🔒 Sécurité

### Étape 8: Vérifier les Permissions
```bash
# Vérifier que seuls les superusers peuvent uploader
# (Ce contrôle est dans les vues avec UserPassesTestMixin)

python manage.py shell
>>> from partnerships.views import PaymentReceiptUploadView
>>> view = PaymentReceiptUploadView()
>>> view.test_func()  # Retournera False si pas superuser
```

### Étape 9: Vérifier CSRF Protection
```html
<!-- payment-receipt-form.html doit avoir: -->
{% csrf_token %}
<!-- ou en HTMX: -->
hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'

# Vérifier dans le template
grep -n "csrf" partnerships/templates/partnerships/partials/payment-receipt-form.html
```

---

## 🧪 Tests Manuels

### Étape 10: Test Basique

**Setup:**
1. Créer un superuser (si n'existe pas)
2. Créer au moins 1 partenaire
3. Créer au moins 1 étudiant pour ce partenaire

```bash
# En shell:
python manage.py shell

from django.contrib.auth.models import User
from partnerships.models import Partner
from students.models import Student

# Créer superuser
user = User.objects.create_superuser('admin', 'admin@test.com', 'admin')

# Créer partenaire
partner = Partner.objects.create(
    name='Test Librairie',
    partner_type='LIB',
    email='lib@test.com',
    commission_per_student=1000,
    user=user
)

# Créer étudiant
student = Student.objects.create(
    full_name='Test Étudiant',
    email='student@test.com',
    library=partner,
    program_id=<id_d'un_programme>,  # À remplacer
    is_confirmed=False,
    status='active'
)
```

**Test du Dashboard:**
1. Démarrer le serveur: `python manage.py runserver`
2. Aller à `http://localhost:8000/partnerships/confirmations/`
3. Se connecter en tant qu'admin
4. Vérifier la section du partenaire
5. Vérifier que les boutons "💳 Paiement" et "📋 Historique" existent

**Test de Modal:**
1. Cliquer sur "💳 Paiement"
2. Vérifier que le modal s'ouvre (F12 → Console, pas d'erreur JavaScript)
3. Remplir le formulaire avec une petite image
4. Cliquer "Valider le paiement"

**Test de Upload:**
1. Formulaire doit se soumettre
2. Vérifier le reçu s'affiche dans le success message
3. Vérifier que les montants se mettent à jour (sans refresh!)

**Test de l'Historique:**
1. Cliquer sur "📋 Historique"
2. Vérifier que le reçu uploadé apparaît

### Étape 11: Tests des Erreurs

**Erreur: Image trop gros**
1. Créer une image > 5MB (ou utiliser ImageMagick)
2. Essayer d'uploader
3. Vérifier le message: "L'image est trop grande. Max 5MB"

**Erreur: Montant négatif**
1. Saisir -1000 dans le montant
2. Cliquer "Valider"
3. Vérifier le message d'erreur

**Erreur: Pas d'image**
1. Saisir un montant
2. Ne pas sélectionner d'image
3. Cliquer "Valider"
4. Vérifier le message: "This field is required"

---

## 📊 Vérifications Finales

### Checklist d'Avant Production

```
SYNTAXE & CONFIG
☐ Pas d'erreur Python (py_compile réussi)
☐ manage.py check passe
☐ MEDIA_ROOT/MEDIA_URL configurés
☐ Dossiers media/ existent avec permissions 755
☐ Migrations appliquées

MODÈLES & VIEWS
☐ Modèles Partner/Payment/PaymentReceipt existent
☐ PaymentReceipt.receipt_image (ImageField) existe
☐ PaymentReceiptUploadView passe les 7 variables au contexte:
  - partner
  - payment
  - receipt
  - partner_pending_count ← Nouveau
  - partner_confirmed_count
  - partner_paid_amount
  - partner_confirmed_amount
  - partner_solde

FORMULAIRES
☐ QuickPaymentForm a les 2 validateurs:
  - FileExtensionValidator(['jpg', 'jpeg', 'png'])
  - validate_image_size (5MB)

TEMPLATES
☐ payment-success.html utilise:
  - {{ receipt.amount_paid }} (pas {{ amount_paid }})
  - {{ partner_pending_count }} (pas {{ partner.students.pending }})
  - {{ partner_confirmed_count }} (pas {{ partner.students.confirmed }})
☐ Out-of-band div avec ID correct: id="partner-{{ partner.id }}-totals"

JAVASCRIPT
☐ HTMX est chargé dans le template
☐ Event listener htmx:afterSwap existe
☐ Modal toggle fonctionne

SÉCURITÉ
☐ Accès superuser only sur les vues de paiement
☐ CSRF protection sur le formulaire
☐ Validation côté serveur (extension, taille)

TESTS
☐ Dashboard s'affiche
☐ Modal s'ouvre (F12: pas d'erreur)
☐ Upload image réussit
☐ Montants se mettent à jour automatiquement
☐ Historique affiche les reçus
```

---

## 🚀 Déploiement

### Étape 12: Démarrer le Serveur

```bash
# 1. Arrêter ancien serveur (s'il tourne)
pkill -f "python manage.py runserver"

# 2. Redémarrer
cd /chemin/vers/irl_ad
python manage.py runserver 0.0.0.0:8000

# 3. Vérifier qu'il démarre
# Doit afficher: "Starting development server at http://0.0.0.0:8000/"
```

### Étape 13: Tester en Production

```bash
# 1. Accéder au dashboard
http://your-server:8000/partnerships/confirmations/

# 2. Tester le flow complet:
#    - Ouvrir modal
#    - Uploader image
#    - Valider paiement
#    - Vérifier mise à jour

# 3. Monitoring
tail -f logs/django.log  # Observer les erreurs
```

### Étape 14: Backup (Important!)

```bash
# Sauvegarder la base de données
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# Sauvegarder les reçus uploadés
tar -czf media_receipts.backup.$(date +%Y%m%d).tar.gz media/receipts/
```

---

## 📝 Documentation à Lire

Après déploiement, vos utilisateurs doivent lire:

1. **QUICK_FIX_SUMMARY.md** - Résumé des changements (2 min)
2. **PAYMENT_SYSTEM_TESTING.md** - Guide de test (15 min)
3. **PAYMENT_TROUBLESHOOTING.md** - Dépannage (sur demande)
4. **CHANGELOG_PAYMENTS_v2.md** - Détails complets (30 min)

---

## ✅ Sign-Off

Quand vous avez coché tous les points above:

```
Date: ___________
Déployé par: ___________
Environnement: ☐ Dev ☐ Staging ☐ Production
Status: ✅ PRÊT À L'EMPLOI
```

---

## 🆘 Si Quelque Chose Va Mal

### Rollback Rapide
```bash
# 1. Arrêter le serveur
pkill -f "python manage.py runserver"

# 2. Restaurer la backup
cp db.sqlite3.backup.YYMMDD db.sqlite3
tar -xzf media_receipts.backup.YYMMDD.tar.gz

# 3. Redémarrer
python manage.py runserver
```

### Demander de l'Aide
Rassembler:
- Exact error message
- Django logs (tail -f logs/django.log)
- Browser console (F12)
- Network tab (F12 → Network)
- Version de Python & Django: `python --version`, `python -m django --version`

---

**Bon déploiement! 🎉**

*Vous avez des questions? Voir PAYMENT_TROUBLESHOOTING.md*
