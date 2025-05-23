# Generated by Django 5.1.7 on 2025-04-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0010_rename_location_accommodation_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation',
            name='distance_from_campus',
        ),
        migrations.AddField(
            model_name='accommodation',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='accommodation_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
