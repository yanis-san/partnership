# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Script pour créer des données de test"""
import os
import django
import sys

# Configurer l'encodage
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partnerships.models import Library, PartnershipCode
from students.models import Student

# Créer des librairies partenaires
libs_data = [
    {
        'name': 'Librairie du Centre',
        'email': 'centre@example.com',
        'phone': '021-XXXXXXX',
        'contact_person': 'Ahmed Benameur',
        'address': 'Rue Didouche Mourad, Alger',
        'commission_per_student': 1500,
        'status': 'active'
    },
    {
        'name': 'Librairie Educative',
        'email': 'edu@example.com',
        'phone': '021-YYYYYYY',
        'contact_person': 'Fatima Boudjahed',
        'address': 'Boulevard Zirout Youcef, Alger',
        'commission_per_student': 1200,
        'status': 'active'
    },
    {
        'name': 'Librairie Scolaire Plus',
        'email': 'scolaire@example.com',
        'phone': '021-ZZZZZZZ',
        'contact_person': 'Rachid Mouhammedi',
        'address': 'Rue des Freres Kebab, Alger',
        'commission_per_student': 1000,
        'status': 'active'
    },
]

print("Création des librairies partenaires...")
for lib_data in libs_data:
    lib, created = Library.objects.get_or_create(
        email=lib_data['email'],
        defaults={k: v for k, v in lib_data.items() if k != 'email'}
    )
    if created:
        print("OK: " + lib.name)
    else:
        print("EXIST: " + lib.name)

    # Créer un code de partenariat
    code = f"LIB{str(lib.id)[:3]}".upper()
    pc, created = PartnershipCode.objects.get_or_create(
        library=lib,
        defaults={
            'code': code,
            'is_active': True
        }
    )
    if created:
        print("   Code: " + code)

# Créer des élèves de test
print("\nCréation d'élèves de test...")
libraries = Library.objects.all()
students_data = [
    {
        'full_name': 'Mohamed Bouchema',
        'email': 'mohamed.bouchema@example.com',
        'phone': '0671234567',
        'status': 'active'
    },
    {
        'full_name': 'Aicha Rezgui',
        'email': 'aicha.rezgui@example.com',
        'phone': '0672345678',
        'status': 'active'
    },
    {
        'full_name': 'Omar Karim',
        'email': 'omar.karim@example.com',
        'phone': '0673456789',
        'status': 'active'
    },
    {
        'full_name': 'Yasmine Tlemcani',
        'email': 'yasmine.tlemcani@example.com',
        'phone': '0674567890',
        'status': 'active'
    },
    {
        'full_name': 'Karim Bencheikh',
        'email': 'karim.bencheikh@example.com',
        'phone': '0675678901',
        'status': 'active'
    },
]

lib_idx = 0
for student_data in students_data:
    lib = libraries[lib_idx % len(libraries)]
    pc = lib.partnership_codes.first()

    student, created = Student.objects.get_or_create(
        email=student_data['email'],
        defaults={
            **student_data,
            'library': lib,
            'referral_code': pc.code if pc else ''
        }
    )
    if created:
        print("OK: " + student.full_name + " - " + lib.name)
    else:
        print("EXIST: " + student.full_name)

    lib_idx += 1

print("\nDonnees de test creees avec succes!")
print("\nURLs disponibles:")
print("- Admin: http://localhost:8000/admin/")
print("- Inscription: http://localhost:8000/register/")
print("- Dashboard librairie: http://localhost:8000/library/[CODE]/")
print("- Dashboard admin: http://localhost:8000/admin/dashboard/")
