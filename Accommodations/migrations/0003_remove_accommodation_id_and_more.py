# Generated by Django 5.1.7 on 2025-04-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodations', '0002_remove_accommodation_accommodation_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation',
            name='id',
        ),
        migrations.AddField(
            model_name='accommodation',
            name='accommodation_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
