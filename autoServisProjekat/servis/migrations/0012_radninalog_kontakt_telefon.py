# Generated by Django 3.2 on 2022-01-15 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servis', '0011_remove_radninalog_opis_servisera'),
    ]

    operations = [
        migrations.AddField(
            model_name='radninalog',
            name='kontakt_telefon',
            field=models.CharField(default='06123456789', max_length=15),
        ),
    ]
