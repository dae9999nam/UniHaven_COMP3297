# Generated by Django 5.1.7 on 2025-04-27 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0013_accommodation_geoaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='university',
            field=models.CharField(choices=[('HKU', 'The University of Hong Kong - HKU'), ('HKUST', 'Hong Kong University of Science and Technology - HKUST'), ('CUHK', 'The Chinese University of Hong Kong - CUHK')], default='HKU', max_length=5),
        ),
    ]
