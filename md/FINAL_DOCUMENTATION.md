# 📚 DOCUMENTATION COMPLÈTE - École d'Affiliation

**Version:** 2.0 (Finale)
**Date:** 20/11/2025
**État:** ✅ PRÊT POUR DÉPLOIEMENT EN PRODUCTION

---

## TABLE DES MATIÈRES

1. [Architecture Système](#architecture-système)
2. [Guide Administrateur](#guide-administrateur)
3. [Guide Partenaire](#guide-partenaire)
4. [Guide Étudiant](#guide-étudiant)
5. [Configuration Technique](#configuration-technique)
6. [Déploiement](#déploiement)
7. [Dépannage](#dépannage)

---

## ARCHITECTURE SYSTÈME

### Vue d'ensemble

L'application École d'Affiliation est un système de gestion d'inscriptions d'étudiants avec tracking de commissions pour les partenaires (librairies, cafés, magasins, etc.).

**Flux principal:**
```
Étudiant inscrit via code partenaire
          ↓
        Email au partenaire & admin
          ↓
        Admin confirme inscription
          ↓
        Partenaire reçoit commission
          ↓
        Partenaire paye via reçu
          ↓
        Admin valide paiement
```

### Composants clés

| Composant | Rôle |
|-----------|------|
| **Admin Django** | Gestion complète des données, confirmations |
| **Portal Partenaire** | Login, voir étudiantsinscrit, payer |
| **Portal Étudiant** | S'inscrire, recevoir confirmation |
| **Système Email** | Notifications automatiques |
| **Dashboard Paiements** | Suivi des montants & paiements |

### Modèles de données

**Student (Étudiant)**
- Prénom, email, téléphone
- Référence au partenaire
- Programme d'inscription
- Statut confirmation (en attente / confirmé)
- Dates d'inscription

**Partner (Partenaire)**
- Nom, email, type (librairie/café/magasin)
- Montant commission par étudiant (par défaut 1000 DA)
- Compte utilisateur pour login
- Code unique de partenaire
- Statut (actif/inactif/suspendu)

**Payment (Paiement)**
- Montant total à payer
- Montant restant
- Statut (en attente / partiel / payé / annulé)
- Lié au partenaire
- Dates création/paiement

**PaymentReceipt (Reçu)**
- Photo du reçu (image)
- Montant payé
- Lié au paiement
- Notes optionnelles

**PartnershipCode (Code de partenaire)**
- Code unique (ex: LIB4F6)
- Lié au partenaire
- Generates QR code pour inscription
- Peut être actif/inactif

---

## GUIDE ADMINISTRATEUR

### Accès

- **URL:** `https://yourdomain.com/admin/`
- **Identifiants:** Compte superuser créé lors du déploiement
- **Permissions:** Accès complet, gestion de tous les modèles

### Tâches principales

#### 1. Créer un nouveau partenaire

1. Aller dans **Partnerships** → **Partenaires**
2. Cliquer **Ajouter partenaire**
3. Remplir:
   - Nom (ex: "Librairie Central")
   - Type (Librairie, Café, Magasin, etc)
   - Email
   - Téléphone (optionnel)
   - Personne de contact
   - Commission par élève (DA)
4. Sauvegarder

**Note:** Un code de partenaire est généré automatiquement

#### 2. Confirmer une inscription d'étudiant

1. Aller dans **Admin Dashboard** ou **Partnerships** → **Confirmations**
2. Voir la liste des inscriptions en attente
3. Cliquer sur l'étudiant pour voir détails
4. **Button "Valider le paiement":**
   - Créer un paiement
   - Uploader le reçu (photo du paiement)
   - Sauvegarder
5. L'inscription passe à "Confirmée"
6. Le montant 1000 DA est acquis pour le partenaire

#### 3. Valider un paiement partenaire

1. Aller dans **Payments Dashboard** ou view paiements
2. Voir montants restants à payer par partenaire
3. Quand reçu est uploadé:
   - Vérifier montant & image
   - Cliquer **Valider le paiement**
4. Paiement passe à "Payé"
5. Email de confirmation envoyé

#### 4. Générer QR codes

**Pour les partenaires (envoyer à leurs clients):**

1. Aller dans **Students** → **QR Codes**
2. Voir codes & QR codes pour chaque partenaire
3. Imprimer ou partager (email, WhatsApp, etc)

**QR pointe vers:** `https://yourdomain.com/register/?code=LIB4F6`

### Tableaux de bord

#### Admin Dashboard
- Total partenaires actifs
- Étudiants en attente / confirmés
- Montants totaux (gagnés, payés, restants)
- Paiements récents
- Étudiants récents

#### Payments Dashboard
- Tous les partenaires avec montants
- Trier par montant restant
- Statut de paiement
- Vue détaillée par partenaire

---

## GUIDE PARTENAIRE

### Accès au portail

1. **URL:** `https://yourdomain.com/partnerships/login/`
2. **Identifiants:**
   - **Code:** Fourni par l'école (ex: LIB4F6)
   - **Email:** Email du partenaire
   - **Mot de passe:** Défini lors de la création du compte
3. **Cliquer "Se connecter"**

### Portail - Vue d'ensemble

#### Dashboard Personnel
Affiche:
- **Étudiants en attente:** Inscrits mais non confirmés par admin
- **Étudiants confirmés:** Admin a validé, montant acquis (1000 DA chacun)
- **Montant total gagné:** Total commission acquise
- **Montant payé:** Déjà versé à l'école
- **Montant restant dû:** À payer

#### Liste des étudiants
- Tous les étudiants inscrits via votre code
- Nom, email, programme
- Statut confirmation

#### Paiements
- Historique complet des paiements
- Montant de chaque paiement
- Photos des reçus (cliquer pour voir en grand)
- Dates de paiement

### Comment payer

1. Aller dans **Paiements**
2. Cliquer **Nouveau paiement**
3. Entrer montant à payer
4. **Prendre photo du reçu:**
   - Prise d'écran virement bancaire
   - Photo reçu banque
   - Photo ticket paiement
5. Optionnel: Ajouter notes (numéro virement, mode paiement)
6. Cliquer **Valider**
7. Admin vérifie et valide le paiement
8. Email de confirmation envoyé

### Besoin d'aide partenaire

- **Oublié identifiants?** Contactez l'école
- **QR code?** Demandez à l'école
- **Problème paiement?** Support directement

---

## GUIDE ÉTUDIANT

### S'inscrire

#### Option 1: Via QR code
1. **Scannez le QR code** fourni par le partenaire
2. Redirige automatiquement vers formulaire
3. Le code partenaire est pré-rempli ✅

#### Option 2: Via code manuel
1. Aller sur `https://yourdomain.com/register/`
2. Remplir le code partenaire (ex: LIB4F6)
3. Continuer

#### Formulaire d'inscription
- **Nom complet**
- **Email** (unique, pour confirmation)
- **Téléphone**
- **Programme** (sélectionner depuis liste)
- **Code partenaire** (pré-rempli si QR)

Cliquer **S'inscrire**

### Confirmation
1. **Email de confirmation reçu**
   - Détails inscription
   - Partenaire impliqué
   - Prochain pas

2. **Admin approuve** (24-48h typiquement)

3. **Email d'approbation reçu**
   - Inscription officielle confirmée
   - Accès portail (si applicable)

### Après inscription
- Vérifier votre email régulièrement
- Garder le code partenaire (peut servir)
- Attendre approbation admin

---

## CONFIGURATION TECHNIQUE

### Stack technique

**Backend:**
- Django 5.2.8
- Python 3.10+
- PostgreSQL 13+ (production)

**Frontend:**
- HTML5 / CSS3 / JavaScript
- HTMX 2.0.8 (interactive forms)
- Bootstrap 5 (responsive design)

**Serveur:**
- Gunicorn (WSGI server)
- Nginx (reverse proxy)
- Let's Encrypt (SSL/TLS)

### Variables d'environnement (.env.production)

```bash
# === DJANGO ===
DEBUG=False
SECRET_KEY=<GÉNÉRÉ_SÉCURISÉ>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# === DATABASE ===
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecole_affiliation
DB_USER=affiliation_user
DB_PASSWORD=<RANDOM_PASSWORD>
DB_HOST=localhost
DB_PORT=5432

# === EMAIL ===
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=<GOOGLE_APP_PASSWORD>
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# === ADMIN ===
ADMIN_NAME=Admin Principal
ADMIN_EMAIL=admin@yourdomain.com

# === SECURITY ===
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Emails configurés

**1. Inscription étudiant → Étudiant**
- À: Email étudiant
- Objet: Confirmation d'inscription
- Contenu: Détails, partenaire, prochaines étapes

**2. Nouvelle inscription → Partenaire**
- À: Email partenaire
- Objet: Nouvelle inscription via votre code
- Contenu: Qui s'est inscrit, attendre confirmation

**3. Nouvelle inscription → Admin**
- À: Email admin
- Objet: Nouvelle inscription: [étudiant] chez [partenaire]
- Contenu: Détails complets, action requise

### Base de données - Tables principales

```
students_student
├── id (UUID)
├── full_name
├── email
├── phone
├── partner_id (FK Partner)
├── referral_code
├── program_id (FK Program)
├── status
├── is_confirmed
└── timestamps

partnerships_partner
├── id (UUID)
├── name
├── partner_type
├── email
├── phone
├── user_id (FK User)
├── commission_per_student
├── status
└── timestamps

partnerships_payment
├── id (UUID)
├── library_id (FK Partner)
├── amount
├── remaining_amount
├── status
└── timestamps

partnerships_paymentreceipt
├── id (UUID)
├── payment_id (FK Payment)
├── receipt_image
├── amount_paid
├── notes
└── timestamps
```

---

## DÉPLOIEMENT

### Pré-déploiement - Checklist

**Critique:**
- [ ] `SECRET_KEY` généré et unique
- [ ] `DEBUG = False`
- [ ] ALLOWED_HOSTS configuré avec domaine réel
- [ ] Database PostgreSQL créée & connectée
- [ ] Email SMTP configuré & testé
- [ ] ADMIN tuple configuré
- [ ] SSL/TLS certificate en place

**Important:**
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Static files collectés
- [ ] Superuser créé
- [ ] Logs directory créé
- [ ] Media directory permissions (755)
- [ ] Service Gunicorn activé au boot

### Déploiement étapes

1. **Préparer serveur**
   ```bash
   sudo apt update
   sudo apt install python3.10 postgresql nginx git
   ```

2. **Cloner & configurer app**
   ```bash
   git clone <repo>
   cd ecole_affiliation
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements-prod.txt
   ```

3. **Configurer base de données**
   ```bash
   createdb ecole_affiliation
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Configurer Gunicorn**
   - Créer `/etc/systemd/system/ecole-affiliation.service`
   - Démarrer: `sudo systemctl start ecole-affiliation`

5. **Configurer Nginx**
   - Créer config dans `/etc/nginx/sites-available/`
   - Activer: `ln -s .../sites-available/ecole-affiliation /etc/nginx/sites-enabled/`
   - Redémarrer: `sudo systemctl restart nginx`

6. **Configurer SSL**
   ```bash
   sudo certbot certonly --nginx -d yourdomain.com
   ```

7. **Vérifier & tester**
   ```bash
   curl -I https://yourdomain.com
   curl https://yourdomain.com/api/health/
   ```

Voir `DEPLOYMENT_PRODUCTION.md` pour détails complets.

---

## DÉPANNAGE

### Les emails ne s'envoient pas

**Symptômes:** Étudiants reçoivent pas email, logs montrent erreurs SMTP

**Solutions:**
1. Vérifier `.env.production`:
   ```bash
   grep EMAIL .env.production
   ```

2. Tester connexion SMTP:
   ```bash
   python3 << 'EOF'
   import smtplib
   s = smtplib.SMTP('smtp.gmail.com', 587)
   s.starttls()
   s.login('your@email.com', 'app_password')
   print('✅ SMTP OK')
   s.quit()
   EOF
   ```

3. Si Gmail: Vérifier "App Passwords" générés
   - https://myaccount.google.com/apppasswords

### Images reçus ne s'affichent pas

**Symptôme:** Error 404 sur `/media/receipts/...`

**Solutions:**
1. Vérifier `settings.py`:
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

2. Vérifier permissions:
   ```bash
   chmod 755 media/
   chmod 644 media/receipts/*
   ```

3. Recollect static files:
   ```bash
   python manage.py collectstatic --no-input --clear
   ```

### Partenaire ne peut pas se connecter

**Symptôme:** "Email, code ou mot de passe incorrect"

**Solutions:**
1. Vérifier partenaire existe:
   ```bash
   python manage.py shell
   from partnerships.models import Partner, PartnershipCode
   Partner.objects.filter(email='partner@email.com')
   PartnershipCode.objects.all()
   ```

2. Vérifier mot de passe:
   ```bash
   partner = Partner.objects.get(email='...')
   partner.check_password('password')  # doit retourner True
   ```

3. Réinitialiser mot de passe:
   ```bash
   partner.set_password('newpassword')
   partner.save()
   ```

### Base de données lente

**Solution:** Vérifier indexes:
```bash
python manage.py dbshell
SELECT * FROM pg_indexes WHERE tablename = 'partnerships_student';
```

### Erreur 500 en production

**Solutions:**
1. Vérifier logs:
   ```bash
   tail -f /var/log/django/error.log
   ```

2. Vérifier permission fichiers:
   ```bash
   sudo chown -R app:app /home/app/ecole_affiliation/
   ```

3. Redémarrer service:
   ```bash
   sudo systemctl restart ecole-affiliation
   ```

---

## ENDPOINTS API

### Health Check
```
GET /api/health/
Response: {"status": "healthy", "database": "ok"}
```

### QR Code
```
GET /qr/<code>/
Returns: PNG image du QR code
```

### Inscription
```
POST /register/
Body: {
  "full_name": "...",
  "email": "...",
  "phone": "...",
  "referral_code": "...",
  "program": "..."
}
Response: Redirect to success page
```

---

## SUPPORT

### Contacts
- **Admin Support:** admin@ecole.com
- **Technical:** tech@ecole.com
- **Partners:** partners@ecole.com

### Heures de support
- Lundi-Vendredi: 09:00 - 18:00
- Urgences: Sur demande

### Monitorin production
- Checks chaque 5 minutes
- Alertes email si problème
- Dashboard Sentry (optionnel)

---

## CHANGELOG

### Version 2.0 (20/11/2025)
- ✅ Simplification des emails (registration only)
- ✅ Renommage "library" → "partner" en cours
- ✅ Lightbox pour reçus
- ✅ Dashboard partenaire personnel
- ✅ Session 24h pour partenaires
- ✅ Production ready

### Version 1.0 (15/11/2025)
- Système initial
- Payment system
- QR codes
- Admin dashboard

---

**Document généré:** 20 novembre 2025
**Pour:** École d'Affiliation
**État:** ✅ PRODUCTION READY

🚀 **Prêt pour déploiement!**
