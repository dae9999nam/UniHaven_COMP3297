# Generated by Django 5.1.7 on 2025-04-28 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0015_remove_accommodation_university'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='universities',
            field=models.ManyToManyField(related_name='accommodations', to='authentication.university'),
        ),
    ]
