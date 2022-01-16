from django.db import models
from django.contrib.auth.models import User

# Create your models here.

korisnik_pozicije = [
    ("SS", "Sef servisa"),
    ("S", "Servise"),
    ("M", "Magacioner"),
]


class Korisnik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pozicija = models.CharField(max_length=3, blank=False, choices=korisnik_pozicije)

    def __str__(self):
        return self.user.username
