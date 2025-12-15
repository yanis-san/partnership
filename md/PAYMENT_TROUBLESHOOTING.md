# 🔧 Guide de Dépannage - Système de Paiements

## 🎯 Arbre de Diagnostic Rapide

```
Problème observé?
├─ Modal ne s'ouvre pas → [SECTION A]
├─ Image ne s'upload pas → [SECTION B]
├─ Montants ne se mettent pas à jour → [SECTION C]
├─ Erreur de validation → [SECTION D]
├─ Erreur 403/Permission → [SECTION E]
├─ Erreur 404 → [SECTION F]
└─ Autre → [SECTION G - Logs]
```

---

## 🅰️ SECTION A: Modal ne s'ouvre pas

### Symptômes
- ❌ Clic sur "💳 Paiement" ne fait rien
- ❌ Rien ne s'affiche
- ❌ Console browser montre une erreur

### Étapes de diagnostic

**Étape A1: Vérifier que HTMX est chargé**
```javascript
// Ouvrir F12 → Console
// Taper:
console.log(htmx);
// Doit afficher: Object { __init: [...] }
// Si undefined = HTMX n'est pas chargé
```

**Diagnostic A1a: HTMX n'est pas chargé**
```html
<!-- Vérifier que ce script existe dans admin-student-confirmation.html -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

**Solutions A1a:**
- Vérifier que le template base inclut le script
- Vérifier que le CDN HTMX est accessible (tester directement l'URL)
- Alternativement: télécharger HTMX localement et utiliser un chemin local

---

**Étape A2: Vérifier l'événement HTMX**
```javascript
// Dans la console:
document.addEventListener('htmx:load', console.log);
document.addEventListener('htmx:xhr:loadstart', console.log);
document.addEventListener('htmx:beforeRequest', console.log);

// Puis cliquer sur le bouton de paiement et observer les logs
```

**Diagnostic A2a: Événement ne se déclenche pas**
```html
<!-- Vérifier que le bouton a les bons attributs -->
<button hx-get="{% url 'payment-receipt-form' partner.id %}"
        hx-target="#payment-modal"
        hx-swap="innerHTML">
    💳 Paiement
</button>
```

**Solutions A2a:**
- Vérifier que les attributs `hx-get`, `hx-target`, `hx-swap` existent
- Vérifier que l'URL est correcte (F12 → Network → XHR)
- Vérifier que le JS du modal est au bon endroit

---

**Étape A3: Vérifier le script du modal**
```javascript
// Celui-ci doit être dans admin-student-confirmation.html
document.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target.id === 'payment-modal') {
        document.getElementById('payment-modal').style.display = 'flex';
    }
});
```

**Diagnostic A3a: Script n'existe pas**
```bash
# Chercher dans le template
grep -n "htmx:afterSwap" admin-student-confirmation.html
# Doit retourner une ligne
```

**Solutions A3a:**
- Ajouter le script JS ci-dessus avant la fermeture du body
- S'assurer que le script est dans le même template

---

**Étape A4: Vérifier que le modal DOM existe**
```javascript
// Dans la console:
document.getElementById('payment-modal');
// Doit retourner: <div id="payment-modal">
// Si null = le modal n'existe pas dans le DOM
```

**Solutions A4a: Modal n'existe pas**
```html
<!-- Ajouter ce code dans admin-student-confirmation.html -->
<div id="payment-modal" class="payment-modal" style="display: none;">
    <div class="modal-backdrop" onclick="..."></div>
    <div class="modal-content">
        <button class="modal-close" onclick="...">×</button>
        <!-- Contenu chargé par HTMX ici -->
    </div>
</div>
```

---

### Résolution Complète A

**Checklist:**
- [ ] `<script src="https://unpkg.com/htmx.org@1.9.10"></script>` existe
- [ ] `<div id="payment-modal">` existe
- [ ] Event listener `htmx:afterSwap` existe
- [ ] Bouton a `hx-get`, `hx-target`, `hx-swap`

Si tous les points sont ✅ et le modal ne s'ouvre toujours pas:
→ Aller à [SECTION G: Logs & Debugging Avancé]

---

## 🅱️ SECTION B: Image ne s'upload pas

### Symptômes
- ❌ "Choose File" fonctionnne mais l'image ne s'upload pas
- ❌ Erreur "This field is required"
- ❌ Erreur de type de fichier

### Étapes de diagnostic

**Étape B1: Vérifier que le champ existe dans le formulaire**
```bash
# Vérifier que QuickPaymentForm a le champ receipt_image
python manage.py shell
>>> from partnerships.forms import QuickPaymentForm
>>> f = QuickPaymentForm()
>>> 'receipt_image' in f.fields
True  # Doit retourner True
```

---

**Étape B2: Tester la validation**
```python
# Dans le shell Django:
from partnerships.forms import QuickPaymentForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

# Créer une petite image test
img = Image.new('RGB', (100, 100), color='red')
img_file = BytesIO()
img.save(img_file, format='PNG')
img_file.seek(0)

# Créer un upload
img_upload = SimpleUploadedFile("test.png", img_file.getvalue(), content_type="image/png")

# Tester le formulaire
form = QuickPaymentForm(
    {'amount_paid': '5000'},
    {'receipt_image': img_upload}
)

if form.is_valid():
    print("✅ Formulaire valide")
else:
    print(f"❌ Erreurs: {form.errors}")
    # Affichera détails de ce qui n'est pas bon
```

**Diagnostic B2a: Extension rejetée**
```
Erreur: receipt_image - File extension jpg is not allowed.
```

**Solutions B2a:**
```python
# Vérifier la liste des extensions acceptées dans forms.py
FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
```

Les extensions autorisées sont: `jpg`, `jpeg`, `png`

**Diagnostic B2b: Taille dépassée**
```
Erreur: receipt_image - L'image est trop grande. Max 5MB, vous avez 8.5MB.
```

**Solutions B2b:**
- Compresser l'image (utiliser un outil de compression)
- Ou augmenter la limite dans `validate_image_size()` (à vos risques)

---

**Étape B3: Vérifier le dossier media/**
```bash
# Dossier media/ doit exister et être accessible
ls -la media/
# Doit afficher: drwxr-xr-x ... media/

# S'il n'existe pas:
mkdir -p media/receipts/
chmod 755 media/

# Vérifier les permissions Django
python manage.py shell
>>> from django.conf import settings
>>> settings.MEDIA_ROOT
# Doit afficher quelque chose comme '/chemin/vers/media'

>>> import os
>>> os.path.exists(settings.MEDIA_ROOT)
True  # Doit être True
```

---

**Étape B4: Vérifier settings.py**
```python
# Vérifier que settings.py a:

# Racine du répertoire media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL d'accès aux fichiers media
MEDIA_URL = '/media/'

# DEBUG doit être True (ou urlpatterns configurées)
DEBUG = True

# Dans urls.py principal:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... autres URLs ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Diagnostic B4a: Settings incorrects**
```python
# Test rapide:
python manage.py shell
>>> from django.conf import settings
>>> settings.MEDIA_URL
'/media/'  # Doit être /media/

>>> settings.MEDIA_ROOT
'/full/path/to/media'  # Doit être un chemin absolu
```

---

**Étape B5: Vérifier le modèle PaymentReceipt**
```bash
# Vérifier que le modèle a le champ receipt_image
python manage.py shell
>>> from partnerships.models import PaymentReceipt
>>> PaymentReceipt._meta.get_fields()
# Doit inclure: 'receipt_image' (ImageField)

# Vérifier que la migration a été appliquée
>>> PaymentReceipt.objects.model._meta.get_field('receipt_image')
<ImageField>
```

---

### Résolution Complète B

**Checklist:**
- [ ] Image format est JPG/PNG/JPEG
- [ ] Image taille < 5MB
- [ ] Dossier `media/receipts/` existe
- [ ] Permissions sur `media/` sont 755
- [ ] `MEDIA_ROOT` et `MEDIA_URL` configurés dans settings.py
- [ ] Urlpatterns incluent `static()` pour DEBUG

Si tous les points sont ✅ et l'image ne s'upload toujours pas:
→ Aller à [SECTION G: Logs & Debugging Avancé]

---

## 🅲️ SECTION C: Montants ne se mettent pas à jour

### Symptômes
- ❌ Après upload de paiement, "Montant Payé" ne change pas
- ❌ "Solde Restant" ne se calcule pas
- ❌ Page doit être rafraîchie pour voir les changements

### Étapes de diagnostic

**Étape C1: Vérifier le out-of-band swap dans la réponse**
```bash
# Ouvrir F12 → Network → XHR
# POST sur: /partnerships/payment-upload/<partner_id>/
# Regarder la Response tab

# Doit contenir:
<div id="partner-<uuid>-totals" hx-swap-oob="true">
    <!-- Les montants mis à jour -->
    <div class="stat-block">
        <label>Montant Payé</label>
        <value>10000 DA</value>
    </div>
    ...
</div>
```

**Diagnostic C1a: Pas de out-of-band dans la réponse**

**Solutions C1a:**
- Vérifier que le template `payment-success.html` contient le div:
```html
<div id="partner-{{ partner.id }}-totals"
     hx-swap-oob="true"
     class="partner-header">
```

- Vérifier que le `{{ partner.id }}` est correct (pas vide ou mal formaté)

---

**Étape C2: Vérifier que le div cible existe**
```javascript
// Dans la console:
document.getElementById('partner-<uuid>-totals');
// Remplacer <uuid> par l'ID réel du partenaire
// Doit retourner un élément (pas null)
```

**Diagnostic C2a: Div n'existe pas**
```html
<!-- Le template admin-student-confirmation.html doit avoir:-->
<div class="partner-header" id="partner-{{ data.partner.id }}-totals">
    <!-- Les stat-blocks avec les montants -->
</div>
```

---

**Étape C3: Vérifier les variables de contexte**
```python
# Dans PaymentReceiptUploadView (views.py ligne ~542)
# Vérifier que le contexte inclut:

return render(request, 'partnerships/partials/payment-success.html', {
    'partner': partner,
    'payment': payment,
    'receipt': receipt,
    'partner_pending_count': partner_pending_count,  # ← Vérifié ✅
    'partner_confirmed_count': partner_confirmed_count,  # ← Vérifié ✅
    'partner_paid_amount': partner_paid_amount,
    'partner_confirmed_amount': partner_confirmed_amount,
    'partner_solde': partner_solde,
})
```

**Diagnostic C3a: Variables manquantes**
```bash
python manage.py shell
>>> from partnerships.views import PaymentReceiptUploadView
# Vérifier la méthode post() et les variables passées
```

---

**Étape C4: Vérifier la logique de calcul du partner_paid_amount**
```python
# Dans la vue:
partner_paid_amount = partner.total_paid
# Cela doit retourner la somme des paiements COMPLETED

# Test:
python manage.py shell
>>> from partnerships.models import Partner
>>> p = Partner.objects.first()
>>> p.total_paid  # Doit retourner un nombre
500  # ou 0 ou autre...
```

**Diagnostic C4a: total_paid retourne 0 ou un nombre incorrecte**
```python
# Vérifier la propriété total_paid dans models.py (ligne 107-111)
@property
def total_paid(self):
    """Montant total déjà payé à cette librairie"""
    return self.payments.filter(status=Payment.COMPLETED).aggregate(
        total=models.Sum('amount')
    )['total'] or 0
```

---

**Étape C5: Vérifier que le paiement est marqué COMPLETED**
```python
# Test:
python manage.py shell
>>> from partnerships.models import Payment
>>> p = Payment.objects.last()
>>> p.status
'completed'  # Doit être 'completed'
>>> p.amount
5000  # Doit avoir le bon montant
```

---

### Résolution Complète C

**Checklist:**
- [ ] Out-of-band div existe dans `payment-success.html` avec l'ID correct
- [ ] Div cible existe dans `admin-student-confirmation.html`
- [ ] Variables `partner_pending_count`, `partner_confirmed_count` passées par la vue
- [ ] `partner.total_paid` retourne le bon montant
- [ ] Paiement est marqué avec `status=Payment.COMPLETED`
- [ ] HTMX version >= 1.9.10 (plus ancien ne supporte pas oob swaps correctement)

Si tous les points sont ✅ et les montants ne se mettent pas à jour:
→ Aller à [SECTION G: Logs & Debugging Avancé]

---

## 🅳️ SECTION D: Erreurs de Validation

### Symptômes
- ❌ Message d'erreur dans le formulaire
- ❌ Paiement rejeta avec raison inconnue

### Erreurs Courantes

**Erreur D1: "This field is required."**
```
Cause: Champ requis non rempli
Solutions:
- Vous avez rempli tous les champs?
- amount_paid: Doit être un nombre > 0
- receipt_image: Doit avoir un fichier
- notes: Peut être vide
```

**Erreur D2: "File extension ... is not allowed"**
```
Cause: Format d'image non supporté
Solutions:
- Extensions autorisées: jpg, jpeg, png (minuscules)
- Vérifier l'extension réelle du fichier
- Si c'est un .PNG en majuscule, renommer en .png
```

**Erreur D3: "L'image est trop grande. Max 5MB"**
```
Cause: Fichier image > 5MB
Solutions:
- Compresser l'image avant upload
- Utiliser un outil: TinyPNG, Squoosh, ou ImageOptim
- Réduire les dimensions (ex: 1920x1080 au lieu de 4000x3000)
```

**Erreur D4: "Ensure this value is greater than or equal to 0"**
```
Cause: Montant négatif ou invalide
Solutions:
- Montant doit être >= 0
- Utiliser un nombre positif (ex: 5000, pas -5000)
- Ne pas utiliser de lettres ou symboles
```

**Erreur D5: "Ensure this value is less than or equal to ..."**
```
Cause: Montant trop gros (overflow décimal)
Solutions:
- Montant max: 999999999999.99 DA
- Cela ne devrait jamais arrive en pratique
- Vérifier que vous ne copier pas un mauvais nombre
```

---

### Résolution D

**Checklist:**
- [ ] Tous les champs requis sont remplis
- [ ] amount_paid: nombre positif (ex: 5000)
- [ ] receipt_image: fichier jpg/jpeg/png < 5MB
- [ ] notes: peut être vide (optionnel)

---

## 🅴️ SECTION E: Erreur 403 ou Permission Denied

### Symptômes
- ❌ "403 Forbidden" ou "You don't have permission"
- ❌ "Forbidden (403)" dans le navigateur

### Causes Principales

**Erreur E1: CSRF Token manquant ou invalide**
```html
<!-- Le formulaire doit avoir le CSRF token -->
<form method="POST" hx-post="...">
    {% csrf_token %}  <!-- ← Vérifié -->
    ...
</form>

<!-- Ou en HTMX headers -->
<button hx-post="..."
        hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

**Solutions E1:**
- Vérifier que `{% csrf_token %}` est dans le formulaire
- Ou passer le token en header HTMX (voir ci-dessus)

---

**Erreur E2: User n'est pas superuser**
```python
# Toutes les vues de paiement requièrent:
class PaymentReceiptFormView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser  # ← Doit être True
```

**Solutions E2:**
```bash
# Vérifier que vous êtes connecté en tant que superuser:
python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='<votre_username>')
>>> u.is_superuser
True  # Doit être True

# Si False, créer un superuser:
python manage.py createsuperuser
```

---

**Erreur E3: Session expirée**
```
Cause: Cookie de session expiré
Solutions:
- Vous reconnecter
- Démarrer une nouvelle session
```

---

### Résolution E

**Checklist:**
- [ ] Vous êtes connecté en tant que superuser
- [ ] `{% csrf_token %}` est dans le formulaire ou headers
- [ ] Session n'est pas expirée

---

## 🅵️ SECTION F: Erreur 404 ou URL non trouvée

### Symptômes
- ❌ "404 Page not found"
- ❌ "The current path didn't match any of these"

### Causes Principales

**Erreur F1: URL pattern ne correspond pas**
```bash
# Vérifier que les URLs sont enregistrées dans partnerships/urls.py
grep -E "payment-form|payment-upload|payment-history" urls.py
```

**Solutions F1:**
```python
# partnerships/urls.py doit avoir:
path('payment-form/<uuid:partner_id>/', PaymentReceiptFormView.as_view(), name='payment-receipt-form'),
path('payment-upload/<uuid:partner_id>/', PaymentReceiptUploadView.as_view(), name='payment-receipt-upload'),
path('payment-history/<uuid:partner_id>/', PaymentReceiptListView.as_view(), name='payment-history'),
```

---

**Erreur F2: UUID invalide**
```
Cause: L'UUID du partenaire est mal formaté
Solutions:
- Vérifier que l'UUID est au bon format (ex: 123e4567-e89b-12d3-a456-426614174000)
- Ne pas modifier l'UUID dans l'URL
```

---

**Erreur F3: Mauvais app name**
```python
# Vérifier que app_name = 'partnerships' est défini dans urls.py
```

---

### Résolution F

**Checklist:**
- [ ] URLs patterns existent dans partnerships/urls.py
- [ ] app_name = 'partnerships' est défini
- [ ] UUID du partenaire est valide

---

## 🅶️ SECTION G: Logs & Debugging Avancé

### Étape G1: Activer les logs Django
```bash
# Dans settings.py:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
```

```bash
# Créer dossier logs
mkdir -p logs/

# Tail les logs en temps réel
tail -f logs/django.log
```

---

### Étape G2: Browser Developer Tools

**F12 → Console tab**
```javascript
// Vérifier les erreurs JavaScript
// Rechercher des erreurs rouges en rapport avec HTMX

// Test HTMX:
console.log(htmx);

// Test événement:
document.addEventListener('htmx:afterSwap', (e) => console.log('SWAP:', e));
```

**F12 → Network tab**
```
1. Filter: XHR
2. POST sur payment-upload
3. Regarder Response (ne doit pas être une erreur HTML)
4. Vérifier le statut (doit être 200)
```

---

### Étape G3: Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

```python
# Dans settings.py:
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]

MIDDLEWARE = [
    ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

```python
# Dans urls.py:
if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

Ensuite, un panneau aparaît sur la droite avec les infos requête.

---

### Étape G4: Test unitaire de la vue

```python
# test_payment_views.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from partnerships.models import Partner, Payment, PaymentReceipt
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class PaymentUploadTestCase(TestCase):
    def setUp(self):
        # Créer superuser
        self.user = User.objects.create_superuser('admin', 'admin@test.com', 'admin')

        # Créer partenaire
        self.partner = Partner.objects.create(
            name='Test Partner',
            email='partner@test.com',
            user=self.user
        )

        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_payment_upload_success(self):
        # Créer une image
        img = Image.new('RGB', (100, 100), color='red')
        img_file = BytesIO()
        img.save(img_file, format='PNG')
        img_file.seek(0)

        img_upload = SimpleUploadedFile("test.png", img_file.getvalue(), content_type="image/png")

        # POST
        response = self.client.post(
            f'/partnerships/payment-upload/{self.partner.id}/',
            {
                'amount_paid': '5000',
                'receipt_image': img_upload,
                'notes': 'Test'
            }
        )

        # Vérifier
        self.assertEqual(response.status_code, 200)  # Pas d'erreur
        self.assertTrue(PaymentReceipt.objects.exists())  # Reçu créé
        self.assertTrue(b'payment-success' in response.content)  # Template correct
```

```bash
# Lancer le test
python manage.py test payments.tests
```

---

### Étape G5: Shell Django interactif

```bash
python manage.py shell
```

```python
# Test la vue manuellement
from django.test import RequestFactory
from partnerships.views import PaymentReceiptUploadView
from partnerships.models import Partner
from django.contrib.auth.models import User

# Créer une requête POST simulée
factory = RequestFactory()
request = factory.post('/payments/upload/')

# Mettre l'utilisateur
user = User.objects.get(username='admin')
request.user = user

# Appeler la vue
view = PaymentReceiptUploadView.as_view()
response = view(request)

# Vérifier la réponse
print(response.status_code)  # Doit être 200
print(response.content[:500])  # Afficher le début du contenu
```

---

## 📞 Quand Demander de l'Aide

Si vous avez suivi toutes les sections et que le problème persiste:

**Rassembler ces infos:**
1. Section/problème spécifique (A-G)
2. Messages d'erreur exacts
3. Logs Django (tail -f logs/django.log)
4. Browser console errors (F12)
5. Network response (F12 → Network)
6. Version Django: `python manage.py --version`
7. Version HTMX utilisée

Puis poser la question avec ces infos.

---

## ✅ Résumé

| Section | Problème | Solution Rapide |
|---------|----------|---|
| A | Modal ne s'ouvre | Vérifier HTMX, JS, DOM |
| B | Image ne s'upload | Format/taille/permissions |
| C | Montants ne se mettent à jour | Out-of-band swap, variables |
| D | Erreur validation | Format image, montant |
| E | Error 403 | Superuser, CSRF token |
| F | Error 404 | URLs patterns |
| G | Autre | Logs & debug toolbar |

---

**Bon debugging! 🔧**
