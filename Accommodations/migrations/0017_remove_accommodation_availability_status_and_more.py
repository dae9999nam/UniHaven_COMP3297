# Generated by Django 5.1.7 on 2025-04-30 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0016_accommodation_universities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation',
            name='availability_status',
        ),
        migrations.AddField(
            model_name='accommodation',
            name='availability_enddate',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='availability_startdate',
            field=models.DateField(default=None),
        ),
    ]
