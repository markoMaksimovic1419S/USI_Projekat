# Generated by Django 3.2 on 2022-01-13 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radninalog',
            name='status',
            field=models.CharField(choices=[('UT', 'Radni nalog u toku'), ('OK', 'Radni nalog je zavrsen uspesno'), ('NO', 'Radni nalog je prekinut')], default='UT', max_length=5),
        ),
    ]