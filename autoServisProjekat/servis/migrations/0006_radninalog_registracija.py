# Generated by Django 3.2 on 2022-01-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servis', '0005_rename_radni_nalog_stavkeracuna_racun'),
    ]

    operations = [
        migrations.AddField(
            model_name='radninalog',
            name='registracija',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
