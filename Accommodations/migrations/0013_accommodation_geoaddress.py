# Generated by Django 5.1.7 on 2025-04-14 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0012_accommodation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='GeoAddress',
            field=models.CharField(default='', max_length=200),
        ),
    ]
