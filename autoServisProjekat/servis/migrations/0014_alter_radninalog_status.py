# Generated by Django 3.2 on 2022-01-15 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servis', '0013_alter_radninalog_registracija'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radninalog',
            name='status',
            field=models.CharField(choices=[('UT', 'Radni nalog u toku'), ('OK', 'Radni nalog je zavrsen uspesno'), ('NO', 'Radni nalog je prekinut'), ('KR', 'Kraj radova, sastavljanje racuna')], default='UT', max_length=5),
        ),
    ]
