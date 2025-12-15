"""Service pour envoyer les emails d'inscription - SIMPLIFIÉ"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_student_registration_email(student):
    """Envoie un email de confirmation à l'étudiant"""
    subject = "Inscription réussie - École d'Affiliation"

    context = {
        'student': student,
    }

    message = render_to_string('emails/student_registration.txt', context)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=False,
        )
        print(f"✅ Email envoyé à l'étudiant: {student.email}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi à {student.email}: {str(e)}")
        return False


def send_partner_notification_email(student):
    """Envoie une notification au partenaire pour une nouvelle inscription"""
    if not student.partner:
        return False

    partner = student.partner
    subject = f"Nouvelle inscription via votre code {student.referral_code}"

    context = {
        'student': student,
        'partner': partner,
    }

    message = render_to_string('emails/partner_notification.txt', context)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[partner.email],
            fail_silently=False,
        )
        print(f"✅ Notification envoyée au partenaire: {partner.email}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi au partenaire: {str(e)}")
        return False


def send_admin_notification_email(student):
    """Envoie une notification aux admins"""
    if not student.partner:
        return False

    partner = student.partner
    admin_emails = [admin[1] for admin in settings.ADMINS]

    if not admin_emails:
        print("⚠️ Aucun email admin configuré")
        return False

    subject = f"Nouvelle inscription: {student.full_name} chez {partner.name}"

    context = {
        'student': student,
        'partner': partner,
    }

    message = render_to_string('emails/admin_notification.txt', context)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False,
        )
        print(f"✅ Notification admin envoyée: {', '.join(admin_emails)}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi aux admins: {str(e)}")
        return False
