# Generated by Django 3.2 on 2022-01-14 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servis', '0007_izdatnicamagacin_odobren'),
    ]

    operations = [
        migrations.RenameField(
            model_name='izdatnicamagacin',
            old_name='odobren',
            new_name='odbio_magacin',
        ),
        migrations.AddField(
            model_name='izdatnicamagacin',
            name='odobren_sef',
            field=models.BooleanField(default=False),
        ),
    ]
