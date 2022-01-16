from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

marke_automobila = [
    ("BMW", "BMW"),
    ("Audi", "Audi"),
    ("Citroen", "Citroen"),
    ("Fiat", "Fiat"),
    ("Renault", "Renault"),

    ("Alfa Romeo", "Alfa Romeo"),
    ("Mercedes", "Mercedes"),
    ("Toyota", "Toyota"),
    ("KIA", "KIA"),
    ("Ford", "Ford"),
    ("Skoda", "Skoda"),
]

status_radni_nalog = [
    ("UT", "Radni nalog u toku"),
    ("OK", "Radni nalog je zavrsen uspesno"),
    ("NO", "Radni nalog je prekinut"),
    ("PR", "Pravljenje racuna"),
    ("KR", "Kraj radova, sastavljanje racuna"),
]

status_porucivanje = [
    ("OS", "Ceka se odobrenje sefa"),
    ("SO", "Sef je odbio porucivanje"),
    ("SP", "Sef porucio delove iz magacina"),
    ("MO", "Magacin odbio porudzbinu"),
    ("OK", "Magacin dostavio porudzbinu"),
]

# Create your models here.
class RadniNalog(models.Model):
    radni_nalog_podneo = models.ForeignKey(User, on_delete=models.CASCADE)
    datum_podnosenja_radnog_naloga = models.DateTimeField(default=timezone.now)

    radni_nalog_kod = models.CharField(max_length=20, blank=False)

    ime_prezime_klijenta = models.CharField(max_length=200, blank=False)
    kontakt_telefon = models.CharField(max_length=15, default="06123456789")
    opis_kvara = models.TextField(blank=False)

    marka_automobila = models.CharField(max_length=30, choices=marke_automobila, blank=False)
    model_automobila = models.CharField(max_length=100, blank=False)
    registracija = models.CharField(max_length=15, blank=True, default="---")

    status = models.CharField(max_length=5, blank=False, choices=status_radni_nalog, default="UT")

    def __str__(self):
        return self.radni_nalog_kod


class ProgresRadnogNaloga(models.Model):
    radni_nalog = models.ForeignKey(RadniNalog, on_delete=models.CASCADE)
    zabelezio = models.ForeignKey(User, on_delete=models.CASCADE)
    datum_belezenja_progresa = models.DateTimeField(default=timezone.now)

    opis_progresa = models.TextField(blank=False)



class IzdatnicaMagacin(models.Model):
    radni_nalog = models.ForeignKey(RadniNalog, on_delete=models.CASCADE)
    izdatnicu_podneo = models.ForeignKey(User, on_delete=models.CASCADE)
    datum_podnosenje_izdatnice = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=10, blank=False, choices=status_porucivanje, default="OS")

    potrebni_deo = models.CharField(max_length=200, blank=False)
    komada = models.PositiveIntegerField(blank=False, default=1)


class Racun(models.Model):
    radni_nalog = models.OneToOneField(RadniNalog, on_delete=models.CASCADE)

    racun_izdao = models.ForeignKey(User, on_delete=models.CASCADE)
    datum_izdavanja_racuna = models.DateTimeField(default=timezone.now)

    ukupna_cena = models.FloatField(blank=False, default=0)


class StavkeRacuna(models.Model):
    racun = models.ForeignKey(Racun, on_delete=models.CASCADE)
    naziv_stavke = models.CharField(max_length=200, blank=False)
    opis_stavke = models.TextField(blank=False)

    cena_stavke = models.FloatField(blank=False)
