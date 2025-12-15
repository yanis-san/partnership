# ⚡ QUICK REFERENCE - École d'Affiliation

**Pour:** Utilisateurs finaux & développeurs
**Mise à jour:** 20/11/2025

---

## 🎯 FOR STUDENTS

### Register Now
```
1. Scan QR code from partner
2. OR go to https://yourdomain.com/register/
3. Fill form (name, email, phone, program, code)
4. Click "S'inscrire"
5. Check email for confirmation
6. Wait for admin approval (24-48h)
```

### After Approval
```
✉️ You receive email confirmation
✨ Inscription is official
📞 Contact admin if questions
```

---

## 🏪 FOR PARTNERS

### Login
```
URL: https://yourdomain.com/partnerships/login/
Code: Provided by school (e.g., LIB4F6)
Email: Your partner email
Password: Set during account creation
```

### Your Dashboard Shows
- Students waiting for confirmation (pending)
- Students confirmed by admin (earned 1000 DA each)
- Total amount earned (commission total)
- Amount already paid
- Amount remaining to pay

### How to Pay
```
1. Go to "Paiements" section
2. Click "Nouveau paiement"
3. Enter amount to pay
4. Take photo of receipt (bank screenshot/proof)
5. Add notes (optional)
6. Click "Valider"
7. Admin verifies and confirms
8. Get confirmation email
```

### Payment History
```
- See all past payments
- View receipt photos (click to zoom)
- Check payment dates
- Track balance
```

---

## 👨‍💼 FOR ADMINS

### Django Admin
```
URL: https://yourdomain.com/admin/
Username: Your superuser account
```

### Main Tasks

**1. Confirm Student Registration**
```
Students → Student list → Click student
Or use Admin Dashboard → Confirmations
Button: "Valider le paiement"
→ Creates payment record for 1000 DA
→ Status changes to "Confirmé"
```

**2. Approve Payment**
```
Partnerships → Payments or Payments Dashboard
Check receipt image
Verify amount is correct
Button: "Valider"
→ Status changes to "Payé"
→ Confirmation email sent
```

**3. Create New Partner**
```
Partnerships → Partenaires → Ajouter
Fill: Name, Type, Email, Commission
Save → Code auto-generated (e.g., LIB4F6)
```

**4. Generate QR Codes**
```
Students → QR Codes
View/Download/Print QR codes
Send to partners
```

### Key Dashboard Pages

| Page | URL | Purpose |
|------|-----|---------|
| Admin | /admin/ | Main control panel |
| Dashboard | /partnerships/admin-dashboard/ | Overview stats |
| Confirmations | /partnerships/admin-student-confirmation/ | Student approvals |
| Payments | /partnerships/payments-dashboard/ | Payment tracking |
| Create Partner | /partnerships/admin-create-partner/ | Add new partners |

---

## 📧 EMAIL FLOW

```
Student registers
    ↓
✉️ Student receives: "Inscription confirmée"
✉️ Partner receives: "Nouvel inscrit via votre code"
✉️ Admin receives: "Nouvel inscrit: [name] chez [partner]"
    ↓
Admin confirms
    ↓
✉️ Payment confirmation sent
```

---

## 💾 DATABASE BACKUP

### Automatic Backups
- Daily at 02:00 AM
- Database dump (.sql.gz)
- Media files (.tar.gz)
- Kept for 30 days

### Manual Backup
```bash
pg_dump ecole_affiliation | gzip > backup_$(date +%Y%m%d).sql.gz
tar -czf media_$(date +%Y%m%d).tar.gz /home/app/ecole_affiliation/media/
```

---

## 🐛 COMMON ISSUES

### "Emails not sending"
```
1. Check .env.production EMAIL settings
2. Test SMTP: Settings → Email settings → Send test
3. Check logs: tail -f /var/log/django/error.log
4. Solution: Re-check Gmail App Passwords
```

### "Images show 404"
```
1. Check MEDIA_URL/MEDIA_ROOT in settings
2. Fix permissions: chmod 755 media/
3. Recollect: python manage.py collectstatic
```

### "Partner can't login"
```
1. Verify partner exists: /admin/partnerships/partner/
2. Check email matches
3. Reset password: Admin → Partner → Set password
4. Ensure code is active: /admin/partnerships/partnershipcode/
```

### "Student didn't receive email"
```
1. Check email is correct in registration
2. Check spam/junk folder
3. Verify SMTP config
4. Check admin email in settings.ADMINS
```

---

## 🚀 DEPLOYMENT QUICK STEPS

```bash
# 1. SSH to server
ssh app@yourdomain.com

# 2. Pull latest code
cd ~/ecole_affiliation
git pull origin main

# 3. Activate venv & install
source venv/bin/activate
pip install -r requirements-prod.txt

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --no-input

# 6. Restart service
sudo systemctl restart ecole-affiliation

# 7. Check status
sudo systemctl status ecole-affiliation

# 8. Check logs
tail -f /var/log/django/error.log
```

---

## 📱 API ENDPOINTS

```
Health Check:
GET /api/health/
→ {"status": "healthy", "database": "ok"}

QR Code (PNG image):
GET /qr/<code>/

Registration Form:
POST /register/
Body: {full_name, email, phone, referral_code, program}
```

---

## 🔐 SECURITY QUICK CHECKS

```bash
# Check SSL
curl -v https://yourdomain.com 2>&1 | grep -i ssl

# Check security headers
curl -I https://yourdomain.com | grep -i "Strict\|Frame\|Content"

# Check database password
grep DB_PASSWORD /home/app/.env.production

# Check .env file permissions
ls -la /home/app/.env.production
→ Should be -rw------- (600)

# Check Django settings
grep DEBUG config/settings.py
→ Should be DEBUG = False
```

---

## 📊 MONITORING

### Check Application Health
```bash
ps aux | grep gunicorn
ps aux | grep nginx
sudo systemctl status ecole-affiliation
```

### Check Disk Space
```bash
df -h
du -sh /home/app/ecole_affiliation/media/
```

### Check Database
```bash
psql ecole_affiliation
\dt  # list tables
SELECT COUNT(*) FROM students_student;
SELECT COUNT(*) FROM partnerships_partner;
```

### Check Logs
```bash
# Django errors
tail -f /var/log/django/error.log

# Nginx errors
tail -f /var/log/nginx/error.log

# Gunicorn
systemctl status ecole-affiliation
```

---

## 🆘 EMERGENCY CONTACTS

- **Admin Support:** admin@ecole.com
- **Technical:** tech@ecole.com
- **Partners:** partners@ecole.com
- **On-Call:** Contact admin for phone

---

## 📚 DOCUMENTATION FILES

```
FINAL_DOCUMENTATION.md  ← Full guide (admin, partner, student, tech)
REFACTORING_STATUS.md   ← What's been done & what's left
DEPLOYMENT_PRODUCTION.md ← Deployment guide (servers, setup, config)
QUICK_REFERENCE.md      ← This file (quick lookups)
WORK_SUMMARY.md         ← Summary of work completed
```

---

## ⚙️ COMMON SETTINGS

**In settings.py:**
```python
DEBUG = False                                    # Production mode
ALLOWED_HOSTS = ['yourdomain.com', ...]        # Your domain
SECURE_SSL_REDIRECT = True                      # Force HTTPS
SESSION_COOKIE_SECURE = True                    # Secure cookies
EMAIL_HOST = 'smtp.gmail.com'                   # Email provider
```

**In .env.production:**
```
SECRET_KEY=django-insecure-xxxxx
ADMIN_EMAIL=admin@yourdomain.com
DB_PASSWORD=complex_password_here
EMAIL_HOST_PASSWORD=google_app_password
```

---

## 🔄 UPDATE CHECKLIST

Before deploying new code:
```
[ ] Pull latest code: git pull
[ ] Install deps: pip install -r requirements.txt
[ ] Run migrations: python manage.py migrate
[ ] Collect static: python manage.py collectstatic
[ ] Test locally: python manage.py runserver
[ ] Push to production
[ ] Restart service: systemctl restart ecole-affiliation
[ ] Check logs: tail -f logs
[ ] Test in browser
```

---

## 📞 QUICK SUPPORT FLOWCHART

```
Issue: Email not sending?
  → Check SMTP config
  → Test Gmail app password
  → Check admin email in ADMINS

Issue: Image shows 404?
  → Check MEDIA_URL/MEDIA_ROOT
  → Fix permissions
  → Recollect static files

Issue: Partner can't login?
  → Check partner exists
  → Verify email & code
  → Reset password
  → Check if code is active

Issue: Student didn't get email?
  → Check email address
  → Check spam folder
  → Check SMTP
  → Resend manually
```

---

**Last Updated:** 20/11/2025
**Version:** 2.0
**Status:** ✅ Production Ready

