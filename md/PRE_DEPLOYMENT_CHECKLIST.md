# ✅ Checklist Pré-Déploiement - Système de Paiements

## 1. Configuration Django

- [ ] Vérifier que `MEDIA_ROOT` est configuré
  ```python
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```

- [ ] Vérifier que `MEDIA_URL` est configuré
  ```python
  MEDIA_URL = '/media/'
  ```

- [ ] Vérifier que le répertoire existe
  ```bash
  mkdir -p media/receipts
  chmod 755 media
  ```

- [ ] Si production avec whitenoise, ajouter:
  ```python
  STORAGES = {
      'staticfiles': {
          'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
      },
  }
  ```

---

## 2. Migrations Django

- [ ] Créer la migration
  ```bash
  python manage.py makemigrations partnerships
  ```

- [ ] Vérifier le contenu de la migration
  ```bash
  cat partnerships/migrations/0002_paymentreceipt.py
  ```

- [ ] Appliquer la migration
  ```bash
  python manage.py migrate partnerships
  ```

- [ ] Vérifier que le modèle existe
  ```bash
  python manage.py shell
  >>> from partnerships.models import PaymentReceipt
  >>> PaymentReceipt.objects.all()
  <QuerySet []>  # ✅
  ```

---

## 3. Dépendances Python

- [ ] Pillow est installé (pour images)
  ```bash
  pip list | grep -i pillow
  # Pillow >= 8.0.0 required
  ```

- [ ] Django est à jour (> 3.2)
  ```bash
  pip list | grep -i django
  # Django >= 3.2
  ```

- [ ] Pas de conflits de dépendances
  ```bash
  pip check
  # No broken requirements found.
  ```

---

## 4. Fichiers et Templates

- [ ] Vérifier que tous les fichiers existent
  ```bash
  ✅ partnerships/models.py (PaymentReceipt ajouté)
  ✅ partnerships/forms.py (QuickPaymentForm ajouté)
  ✅ partnerships/views.py (3 vues ajoutées)
  ✅ partnerships/urls.py (3 routes ajoutées)
  ✅ partnerships/migrations/0002_paymentreceipt.py
  ✅ partials/payment-receipt-form.html
  ✅ partials/payment-success.html
  ✅ partner-payment-history.html
  ✅ admin-student-confirmation.html (modal ajouté)
  ```

- [ ] Vérifier que HTMX est chargé dans base.html
  ```html
  <script src="https://unpkg.com/htmx.org@1.9.10"></script>
  ```

- [ ] Vérifier la syntaxe des templates
  ```bash
  python manage.py check
  # System check identified no issues (0 silenced).
  ```

---

## 5. Sécurité

- [ ] CSRF protection activée
  ```python
  MIDDLEWARE = [
      ...
      'django.middleware.csrf.CsrfViewMiddleware',
      ...
  ]
  ```

- [ ] Vérifier que les vues vérifient is_superuser
  ```python
  def test_func(self):
      return self.request.user.is_superuser  # ✅
  ```

- [ ] HTTPS activé en production
  ```python
  if not DEBUG:
      SECURE_SSL_REDIRECT = True
      SESSION_COOKIE_SECURE = True
      CSRF_COOKIE_SECURE = True
  ```

- [ ] Limite de taille de fichier définie (optionnel)
  ```python
  DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
  FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
  ```

---

## 6. Tests de Fonctionnalité

### A. Test du formulaire
- [ ] Accéder à `/partnerships/confirmations/`
- [ ] Click "💳 Paiement" sur un partenaire
- [ ] Modal s'affiche avec le formulaire
- [ ] Saisir montant: 10000
- [ ] Uploader une image
- [ ] Click "Valider"
- [ ] Message de succès s'affiche ✅

### B. Test de la mise à jour HTMX
- [ ] Vérifier que le dashboard se met à jour (arrière-plan)
- [ ] "Montant Payé" augmente automatiquement
- [ ] "Solde" diminue automatiquement
- [ ] Pas de rafraîchissement de page

### C. Test de l'historique
- [ ] Depuis le succès, click "Historique"
- [ ] Tous les reçus s'affichent
- [ ] Les plus récents en premier
- [ ] Images visibles

### D. Test du mobile
- [ ] Accéder depuis un téléphone
- [ ] Click "💳 Paiement"
- [ ] Modal responsive
- [ ] Caméra accessible pour upload image
- [ ] Boutons accessibles

---

## 7. Base de Données

- [ ] Sauvegarde avant migration
  ```bash
  cp db.sqlite3 db.sqlite3.backup
  ```

- [ ] Vérifier l'intégrité après migration
  ```bash
  python manage.py sqlmigrate partnerships 0002
  # Vérifier les CREATE TABLE commands
  ```

- [ ] Vérifier que les relations fonctionnent
  ```python
  from partnerships.models import Partner, Payment, PaymentReceipt

  partner = Partner.objects.first()
  payment = partner.payments.first()
  receipt = payment.receipt  # ✅ OneToOne access
  ```

---

## 8. Logs et Monitoring

- [ ] Vérifier que les logs sont activés
  ```python
  LOGGING = {
      'version': 1,
      'handlers': {
          'file': {
              'level': 'INFO',
              'class': 'logging.FileHandler',
              'filename': 'logs/django.log',
          },
      },
  }
  ```

- [ ] Créer le répertoire logs
  ```bash
  mkdir -p logs
  chmod 755 logs
  ```

---

## 9. Performance

- [ ] Vérifier que les images ne sont pas trop lourdes
  ```bash
  # Maximum recommandé: 2-3 MB par reçu
  # Moyen: 500 KB - 1 MB
  ```

- [ ] Optimiser les requêtes BD (lazy loading)
  ```python
  # ✅ SELECT_RELATED en place
  receipts = PaymentReceipt.objects.filter(
      payment__library=partner
  ).select_related('payment')
  ```

- [ ] Vérifier que les templates n'ont pas de N+1 queries
  ```python
  # DEBUG: Set DEBUG=True, voir les requêtes
  python manage.py shell
  >>> from django.db import connection, reset_queries
  >>> reset_queries()
  >>> # ... votre code ...
  >>> len(connection.queries)  # Ne doit pas être énorme
  ```

---

## 10. Documentation

- [ ] README.md mis à jour
- [ ] PAYMENT_SYSTEM.md créé ✅
- [ ] QUICK_START_PAYMENTS.md créé ✅
- [ ] PAYMENT_FLOW_DIAGRAM.md créé ✅
- [ ] Commentaires ajoutés au code

---

## 11. Déploiement

### Sur serveur de développement
```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Apply migrations
python manage.py migrate

# 5. Restart server
sudo systemctl restart django  # ou votre service
```

### Sur serveur de production
```bash
# 1. Vérifier que settings.py est en mode production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# 2. Vérifier HTTPS
SECURE_SSL_REDIRECT = True

# 3. Vérifier STATIC_ROOT pour whitenoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 4. Sauvegarde DB avant migration
pg_dump dbname > backup_before_migration.sql

# 5. Apply migrations
python manage.py migrate partnerships

# 6. Vérifier les permissions media
chmod -R 755 media/
chown -R www-data:www-data media/  # ou votre utilisateur

# 7. Restart workers
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 12. Post-Déploiement

- [ ] Vérifier que le site est accessible
  ```bash
  curl https://yourdomain.com/partnerships/confirmations/
  ```

- [ ] Vérifier que les médias sont accessibles
  ```bash
  curl https://yourdomain.com/media/receipts/...
  ```

- [ ] Faire un test complet avec un superuser
  - [ ] Ajouter un paiement
  - [ ] Uploader un reçu
  - [ ] Vérifier les totaux
  - [ ] Vérifier l'historique

- [ ] Monitorer les logs
  ```bash
  tail -f logs/django.log
  tail -f /var/log/nginx/error.log
  ```

- [ ] Vérifier qu'aucune erreur 500 n'apparaît

---

## 13. Rollback (si problème)

```bash
# 1. Revert migration
python manage.py migrate partnerships 0001

# 2. Revert code
git checkout HEAD~1

# 3. Restart server
sudo systemctl restart django

# 4. Contact dev for support
```

---

## 14. Améliorations Post-Lancement (Nice-to-Have)

- [ ] Ajouter compression d'images automatique (Pillow)
- [ ] Ajouter OCR pour extraire montants (pytesseract)
- [ ] Ajouter email de confirmation (django-mail)
- [ ] Ajouter export PDF (reportlab)
- [ ] Ajouter statistiques/graphiques (matplotlib)

---

## Signature

**Déploiement Date:** ________________
**Déployé par:** ________________
**Testé par:** ________________
**Approuvé par:** ________________

---

## Notes Additionnelles

```
Ajoutez vos notes ici:

_____________________________________________

_____________________________________________

_____________________________________________

_____________________________________________
```

---

## Support en Cas de Problème

📧 **Contact:** developper@example.com
📚 **Docs:** `PAYMENT_SYSTEM.md`
🐛 **Bugs:** Vérifier les logs Django
⚡ **Performance:** Vérifier les requêtes BD

---

**Status:** ✅ Prêt pour production
**Version:** 1.0
**Last Updated:** 2024-11-25
