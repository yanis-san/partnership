from django.core.management.base import BaseCommand
from django.conf import settings
import qrcode
import os
from partnerships.models import PartnershipCode


class Command(BaseCommand):
    help = 'Generates QR codes for all partnership codes'

    def handle(self, *args, **options):
        # Creer le dossier s'il n'existe pas
        qrcode_dir = os.path.join(settings.BASE_DIR, 'static', 'qrcodes')
        os.makedirs(qrcode_dir, exist_ok=True)

        # Récupérer tous les codes actifs
        codes = PartnershipCode.objects.filter(is_active=True)

        if not codes.exists():
            self.stdout.write(self.style.WARNING('Aucun code de partenariat trouvé'))
            return

        count = 0
        for code in codes:
            # URL complète pour le QR code
            url = f'http://localhost:8000/register/?code={code.code}'

            # Générer le QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Créer l'image
            img = qr.make_image(fill_color='black', back_color='white')

            # Sauvegarder le fichier
            filename = f'{code.code.lower()}.png'
            filepath = os.path.join(qrcode_dir, filename)

            img.save(filepath)
            self.stdout.write(
                self.style.SUCCESS(
                    f'OK - QR code cree: {filename}'
                )
            )
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n{count} QR code(s) generes avec succes dans {qrcode_dir}'
            )
        )
