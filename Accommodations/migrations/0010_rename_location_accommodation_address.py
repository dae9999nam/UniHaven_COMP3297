# Generated by Django 5.1.7 on 2025-04-07 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0009_alter_accommodation_accommodation_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accommodation',
            old_name='location',
            new_name='address',
        ),
    ]
