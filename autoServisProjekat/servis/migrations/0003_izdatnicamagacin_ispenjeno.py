# Generated by Django 3.2 on 2022-01-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servis', '0002_alter_radninalog_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='izdatnicamagacin',
            name='ispenjeno',
            field=models.BooleanField(default=False),
        ),
    ]
