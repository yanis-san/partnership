# 📋 STATUS REFACTORING: library → partner

**Date:** 20 novembre 2025
**Objectif:** Renommer toutes les références "library" en "partner" pour harmoniser la terminologie

---

## RÉSUMÉ DES CHANGEMENTS

### ✅ COMPLÉTÉ

#### 1. Modèles (models.py)
- ✅ `Student.library` → `Student.partner` (champ ForeignKey)
- ✅ Import mis à jour: `from partnerships.models import Partner`
- ✅ Alias backward-compatibility: `Library = Partner` (fin de file)

#### 2. Admin Django (admin.py)
- ✅ `StudentAdmin.list_display`: `library` → `partner`
- ✅ `StudentAdmin.list_filter`: `library` → `partner`
- ✅ `StudentAdmin.fieldsets`: `library` → `partner`

#### 3. Vues Étudiants (students/views.py)
- ✅ Import: `Library` → `Partner`
- ✅ `StudentRegistrationView`: Appels email sans request param
- ✅ `_print_confirmation_email()`: `student.library` → `student.partner`
- ✅ `PartnerDashboardView`: Classe renommée (anciennement `LibraryDashboardView`)
- ✅ `QRCodeListView`: Contexte `'partner'` au lieu de `'library'`

#### 4. Services Email (email_service.py)
- ✅ `send_partner_notification_email()`: `student.library` → `student.partner`
- ✅ `send_admin_notification_email()`: `student.library` → `student.partner`
- ✅ Signatures simplifiées (sans request param)

#### 5. Vues Partenaires - PARTIELLES (partnerships/views.py)
- ✅ Import: `Library` → `Partner`
- ✅ `AdminDashboardView`:
  - `Library.objects` → `Partner.objects`
  - Contexte: `libraries` → `partners`, `total_libraries` → `total_partners`
- ✅ `AdminStatsView`: `library=partner` dans filters
- ✅ `PaymentsDashboardView`: `Library` → `Partner`, contexte mis à jour
- ✅ `PartnerLoginView`: Classe renommée, session keys → `partner_*`
  - `library_id` → `partner_id`
  - `library_name` → `partner_name`
  - `library_code` → `partner_code`
  - Redirect: `library-login` → `partner-login`
  - Template: `library-login.html` → `partner-login.html`
- ✅ `PartnerDashboardPersonalView`: Classe renommée, contexte → `partner`
  - Session lookup: `partner_id` au lieu de `library_id`
  - Template: `library-dashboard-personal.html` → `partner-dashboard-personal.html`
- ✅ `partner_logout_view()`: Fonction renommée, session keys updated
- ✅ `PartnerPaymentHistoryView`: Classe renommée, contexte → `partner`
  - Template: `library-payment-history.html` → `partner-payment-history.html`

---

## 🔴 À FAIRE

### 1. Templates HTML

**À renommer:**
- [ ] `partnerships/templates/partnerships/library-dashboard.html` → `partner-dashboard-public.html`
- [ ] `partnerships/templates/partnerships/library-dashboard-personal.html` → `partner-dashboard-personal.html`
- [ ] `partnerships/templates/partnerships/library-login.html` → `partner-login.html`
- [ ] `partnerships/templates/partnerships/library-payment-history.html` → `partner-payment-history.html`
- [ ] `students/templates/students/library-dashboard.html` → `partner-dashboard.html`

**À mettre à jour dans les templates:**
- [ ] Remplacer `{{ library }}` par `{{ partner }}`
- [ ] Remplacer `{{ library. }}` par `{{ partner. }}`
- [ ] Remplacer textes "librairie" par "partenaire"
- [ ] URLs: `library-login` → `partner-login`, etc

### 2. URLs (partnerships/urls.py et students/urls.py)

**À vérifier/mettre à jour:**
- [ ] `'library-login'` → `'partner-login'`
- [ ] `'library-dashboard-personal'` → `'partner-dashboard-personal'`
- [ ] `'library-logout'` → `'partner-logout'`
- [ ] `'library-payment-history'` → `'partner-payment-history'`
- [ ] Routes pointant vers `LibraryLoginView` → `PartnerLoginView`
- [ ] Routes pointant vers `LibraryDashboardView` → `PartnerDashboardPublicView`

### 3. Vues Partenaires (partnerships/views.py) - SUITE

Les sections suivantes contiennent encore beaucoup de références "library":
- [ ] `AdminPartnerCreationView` (~ligne 377+): `library=partner` dans PartnershipCode
- [ ] `ConfirmStudentHTMXView` (~ligne 450+): Vérifier context keys
- [ ] `AdminStudentConfirmationView` (~ligne 500+): Références student.library
- [ ] `PaymentReceiptUploadView` (~ligne 550+): student.library references
- [ ] Toutes les autres vues qui référencent `.library` sur models

### 4. Autres fichiers Python

**students/forms.py**
- [ ] Vérifier s'il y a des références library

**partnerships/forms.py**
- [ ] Vérifier s'il y a des références library

**partnerships/admin.py**
- [ ] Vérifier list_display, list_filter, fieldsets pour Partner model
- [ ] Vérifier AuditLog pour références

**Migrations**
- [ ] Créer migration pour `Student.library` → `Student.partner` field rename
  - Commande: `python manage.py makemigrations students`
  - Note: Django peut renommer automatiquement ou créer une migration manuel

### 5. Documentation & Commentaires

- [ ] Mettre à jour docstrings des classes renommées
- [ ] Mettre à jour commentaires code (remplacer "librairie" → "partenaire")
- [ ] Vérifier `help_text` et `verbose_name` des modèles

---

## NOTES TECHNIQUES

### Backward Compatibility

Un alias a été créé à la fin de `partnerships/models.py`:
```python
Library = Partner
```

Cela permet au code existant utilisant `Library.objects` de continuer à fonctionner. **À supprimer après refactoring complet.**

### Stratégie Migration Database

Pour renommer le champ `Student.library` en `Student.partner`:

**Option 1: Migration Automatique (recommandée)**
```bash
# Django détecte le rename et propose
python manage.py makemigrations students
# → Choisir "Rename" quand demandé
```

**Option 2: Migration Manuelle**
Créer une migration qui:
1. Crée nouveau champ `partner`
2. Copie données de `library` → `partner`
3. Supprime ancien champ `library`

### Session Keys

Les session keys ont été mises à jour:
- `library_id` → `partner_id`
- `library_name` → `partner_name`
- `library_code` → `partner_code`

**Impact:** Les sessions existantes des partenaires connectés seront invalidées après déploiement.

### URL Reversal

Mettre à jour tous les `reverse()` et `reverse_lazy()`:
```python
# Avant
redirect('library-login')

# Après
redirect('partner-login')
```

---

## CHECKLIST FINALE

- [ ] Renommer tous les templates
- [ ] Mettre à jour les URLs
- [ ] Mettre à jour toutes les vues restantes
- [ ] Supprimer alias `Library = Partner`
- [ ] Créer & appliquer migration Student.library → partner
- [ ] Mettre à jour help_text & verbose_name des modèles
- [ ] Tests: Inscription → Email → Confirmation → Login → Paiement
- [ ] Tests: Admin dashboard fonctionne
- [ ] Tests: QR codes générés correctement
- [ ] Vérifier tous les redirects fonctionnent
- [ ] Vérifier context keys dans templates
- [ ] Deploy et vérifier logs

---

## GREP COMMANDS POUR TROUVER RÉFÉRENCES

Trouver références restantes:
```bash
# Toutes les occurrences
grep -r "library" --include="*.py" --include="*.html" \
  --exclude-dir=.venv --exclude-dir=migrations .

# Juste les ForeignKey/.library
grep -r "\.library" --include="*.py" --include="*.html" \
  --exclude-dir=.venv .

# Juste dans les templates
grep -r "{{ library" --include="*.html" .

# Juste dans Python code (non-docstring)
grep -r "'library'" --include="*.py" --exclude-dir=.venv .
```

---

## PRIORITÉ FIXES

1. **Haute:** Templates (utilisateurs les voient)
2. **Haute:** URLs (cassent les liens)
3. **Haute:** Vues partenaire restantes
4. **Moyenne:** Migration database
5. **Basse:** Commentaires & docstrings
6. **Basse:** Alias Library (cleanup)

---

## IMPACT UTILISATEURS

- ✅ **Étudiants:** Aucun impact, flux transparent
- ⚠️ **Partenaires:** Sessions invalidées après deploy (re-login nécessaire)
- ✅ **Admins:** Aucun impact, interface unchanged
- ✅ **Emails:** Aucun impact, contenu unchanged

---

## TIME ESTIMATE

- Template rename: 15 min
- URL updates: 10 min
- Views updates: 45 min
- Migration création: 5 min
- Testing complet: 30 min
- **TOTAL: ~2 heures de travail**

---

**Document créé:** 20 novembre 2025
**État:** Refactoring en cours
**Prochaine étape:** Renommer les templates

