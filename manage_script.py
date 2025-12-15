# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Gestion utile du système"""
import os
import django
import sys
from decimal import Decimal

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partnerships.models import Library, Payment
from students.models import Student

def show_statistics():
    """Afficher les statistiques globales"""
    print("\n=== STATISTIQUES GLOBALES ===\n")

    libs = Library.objects.all()
    print(f"Librairies: {libs.count()}")

    for lib in libs:
        print(f"\n{lib.name}")
        print(f"  Code: {lib.partner_code}")
        print(f"  Email: {lib.email}")
        print(f"  Eleves: {lib.total_students}")
        print(f"  Commission/eleve: {lib.commission_per_student} DA")
        print(f"  Total genere: {lib.total_earned} DA")
        print(f"  Total paye: {lib.total_paid} DA")
        print(f"  Solde: {lib.remaining_balance} DA")
        print(f"  Statut paiement: {lib.payment_status}")

def create_payment(library_id, amount):
    """Creer un paiement"""
    try:
        lib = Library.objects.get(id=library_id)
        payment = Payment.objects.create(
            library=lib,
            amount=Decimal(amount),
            status=Payment.PENDING
        )
        print(f"Paiement cree: {amount} DA pour {lib.name}")
    except Library.DoesNotExist:
        print("Librairie introuvable")

def mark_payment_completed(payment_id):
    """Marquer un paiement comme complete"""
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.mark_as_completed()
        print(f"Paiement marque comme complete")
    except Payment.DoesNotExist:
        print("Paiement introuvable")

def list_students():
    """Lister tous les eleves"""
    students = Student.objects.all()
    print(f"\nTotal eleves: {students.count()}\n")
    for student in students:
        lib_name = student.library.name if student.library else "Aucune"
        print(f"{student.full_name} - {lib_name}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'stats':
            show_statistics()
        elif cmd == 'students':
            list_students()
        elif cmd == 'payment':
            if len(sys.argv) >= 4:
                create_payment(sys.argv[2], sys.argv[3])
        else:
            print("Commandes disponibles:")
            print("  stats - Afficher les statistiques")
            print("  students - Lister les eleves")
            print("  payment [library_id] [amount] - Creer un paiement")
    else:
        print("Utilisation: python manage_script.py [commande]")
        show_statistics()
