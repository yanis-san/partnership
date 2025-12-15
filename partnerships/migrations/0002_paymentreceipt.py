# Generated migration for PaymentReceipt model

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('partnerships', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentReceipt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('receipt_image', models.ImageField(help_text='Prenez une photo du reçu de paiement', upload_to='receipts/%Y/%m/%d/', verbose_name='Photo du reçu')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant payé (DA)')),
                ('notes', models.TextField(blank=True, verbose_name='Notes (ex: mode de paiement, date du paiement)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='partnerships.payment', verbose_name='Paiement associé')),
            ],
            options={
                'verbose_name': 'Reçu de paiement',
                'verbose_name_plural': 'Reçus de paiement',
                'ordering': ['-created_at'],
            },
        ),
    ]
