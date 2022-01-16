from django.shortcuts import render, reverse, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.contrib.auth.models import User
from korisnici.models import Korisnik
from .models import *

import string
import random


# Create your views here.

@login_required
def pregled_servis(request):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    context = {"user": user, "korisnik": korisnik}
    if korisnik.pozicija == "SS" or korisnik.pozicija == "S":
        nalozi_u_toku = RadniNalog.objects.filter(status="UT")
        context['radni_nalozi'] = nalozi_u_toku
        if korisnik.pozicija == "SS":
            zahtevi_porucivanje = IzdatnicaMagacin.objects.filter(status="OS")
            context['zahtevi_porucivanje'] = zahtevi_porucivanje
            nalozi_za_proveru = RadniNalog.objects.filter(Q(status="KR") | Q(status="PR"))
            context['nalozi_za_proveru'] = nalozi_za_proveru
            print(zahtevi_porucivanje)
            svi_zahtevi = RadniNalog.objects.all()
            context['svi_zahtevi'] = svi_zahtevi
    elif korisnik.pozicija == "M":
        zahtevi_porucivanje = IzdatnicaMagacin.objects.filter(status="SP")
        context['zahtevi_porucivanje'] = zahtevi_porucivanje

    return render(request, 'servis/pregled.html', context)


@csrf_exempt
def postoji_kod(request):
    kod = request.POST["kod_slucaja"]
    try:
        radni_nalog = RadniNalog.objects.get(radni_nalog_kod=kod)
        return HttpResponse('OK')
    except:
        return HttpResponse('NO')


def radni_nalog_kod(request):
    kod = request.GET['kod_slucaja']
    context = {}
    try:
        user = request.user
        korisnik = Korisnik.objects.get(user=user)
        context['korisnik'] = korisnik
    except:
        pass
    try:
        radni_nalog = RadniNalog.objects.get(radni_nalog_kod=kod)
        context['nalog'] = radni_nalog
        proges_naloga = ProgresRadnogNaloga.objects.filter(radni_nalog=radni_nalog)
        context['progres'] = proges_naloga
        izdatnica = IzdatnicaMagacin.objects.filter(radni_nalog=radni_nalog, status="OK")
        context['delovi'] = izdatnica
        naruceni_delovi = IzdatnicaMagacin.objects.filter(radni_nalog=radni_nalog)
        context['naruceni_delovi'] = naruceni_delovi
        # delovi = DeloviIzdatnica.objects.filter(izdatnica__radni_nalog=radni_nalog)
        # context['delovi'] = delovi

        try:
            racun = Racun.objects.get(radni_nalog=radni_nalog)
            context['racun'] = racun
            stavke_racuna = StavkeRacuna.objects.filter(racun=racun)
            context['stavke_racuna'] = stavke_racuna
            print(racun)
        except Exception as e:
            print(e)

    except:
        return redirect(reverse('index'))

    return render(request, 'servis/nalog_pregled.html', context)


@login_required
def dodaj_progres(request):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    radni_nalog = RadniNalog.objects.get(id=request.POST['id'])
    if radni_nalog.status != "UT":
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        return redirect(a)

    opis = request.POST['opis_progresa']
    if len(opis) < 1:
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)

    nov_progres = ProgresRadnogNaloga.objects.create(opis_progresa=opis, zabelezio=user, radni_nalog=radni_nalog)
    nov_progres.save()

    a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
    print(a)
    print(redirect(a))
    return redirect(a)


@login_required
def obrisi_progres(request, id):
    progres = ProgresRadnogNaloga.objects.get(id=id)
    radni_nalog = RadniNalog.objects.get(id=progres.radni_nalog.id)
    progres.delete()

    a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
    print(a)
    print(redirect(a))
    return redirect(a)


@login_required
def naruci_deo(request):
    user = request.user
    radni_nalog = RadniNalog.objects.get(id=request.POST['radni_nalog_id'])

    naziv = request.POST['naziv_dela']
    kolicina = request.POST['kolicina']

    if len(naziv) < 1:
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)

    izdatnica = IzdatnicaMagacin.objects.create(radni_nalog=radni_nalog, izdatnicu_podneo=user, komada=kolicina,
                                                potrebni_deo=naziv)
    izdatnica.save()
    # deo = DeloviIzdatnica.objects.create(komada=kolicina, potrebni_deo=naziv, izdatnica=izdatnica)
    # deo.save()

    a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
    print(a)
    print(redirect(a))
    return redirect(a)


@login_required
def sef_odbio_deo(request, id):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija != "SS":
        return redirect(reverse('pregled_servis'))
    deo = IzdatnicaMagacin.objects.get(id=id)
    deo.status = "SO"
    deo.save()
    return redirect(reverse('pregled_servis'))


@login_required
def sef_prihvatio_deo(request, id):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija != "SS":
        return redirect(reverse('pregled_servis'))
    deo = IzdatnicaMagacin.objects.get(id=id)
    deo.status = "SP"
    deo.save()
    return redirect(reverse('pregled_servis'))


@login_required
def magacin_odbio_deo(request, id):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija != "M":
        return redirect(reverse('pregled_servis'))
    deo = IzdatnicaMagacin.objects.get(id=id)
    deo.status = "MO"
    deo.save()
    return redirect(reverse('pregled_servis'))


@login_required
def magacin_prihvatio_deo(request, id):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija != "M":
        return redirect(reverse('pregled_servis'))
    deo = IzdatnicaMagacin.objects.get(id=id)
    deo.status = "OK"
    deo.save()
    progres = ProgresRadnogNaloga.objects.create(radni_nalog=deo.radni_nalog, zabelezio=user,
                                                 opis_progresa="Dostavljen deo: " + deo.potrebni_deo)
    progres.save()
    return redirect(reverse('pregled_servis'))


@login_required
def kreairaj_nalog(request):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    context = {}
    if korisnik.pozicija != "SS":
        return redirect(reverse('pregled_servis'))

    context['user'] = user
    context['korisnik'] = korisnik
    return render(request, 'servis/kreiraj_radni_nalog.html', context)


@login_required
def kreairanje_radnog_naloga(request):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    context = {}
    if korisnik.pozicija != "SS":
        return redirect(reverse('pregled_servis'))

    context['user'] = user
    context['korisnik'] = korisnik
    registracija = request.POST['registracija']
    if len(registracija) < 1:
        registracija = "---"
    nov_radni_nalog = RadniNalog.objects.create(
        radni_nalog_podneo=user,
        radni_nalog_kod=''.join(random.choice(string.ascii_lowercase) for x in range(10)),
        ime_prezime_klijenta=request.POST['klijent'],
        kontakt_telefon=request.POST['kontakt'],
        marka_automobila=request.POST['marka'],
        model_automobila=request.POST['model'],
        registracija=registracija,
        opis_kvara=request.POST['opis']
    )
    nov_radni_nalog.save()

    a = reverse('radni_nalog_kod') + "?kod_slucaja=" + nov_radni_nalog.radni_nalog_kod
    print(a)
    print(redirect(a))
    return redirect(a)


@login_required
def posalji_na_proveru(request, id):
    print("OK")
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija == "SS" or korisnik.pozicija == "S":
        print("KK")
        radni_nalog = RadniNalog.objects.get(id=id)
        radni_nalog.status = "KR"
        radni_nalog.save()
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)

    print("AA")
    return redirect(reverse('pregled_servis'))


@login_required
def oznaci_prekinut(request, id):
    print("OK")
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija == "SS":
        print("KK")
        radni_nalog = RadniNalog.objects.get(id=id)
        radni_nalog.status = "NO"
        radni_nalog.save()
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)

    print("AA")
    return redirect(reverse('pregled_servis'))


@login_required
def oznaci_ok(request, id):
    print("OK")
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija == "SS":
        print("KK")
        radni_nalog = RadniNalog.objects.get(id=id)
        radni_nalog.status = "OK"
        radni_nalog.save()
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)

    print("AA")
    return redirect(reverse('pregled_servis'))


@login_required
def oznaci_pr(request, id):
    print("OK")
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija == "SS":
        print("KK")
        radni_nalog = RadniNalog.objects.get(id=id)
        radni_nalog.status = "PR"
        radni_nalog.save()
        nov_racun = Racun.objects.create(radni_nalog=radni_nalog, racun_izdao=user)
        nov_racun.save()
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)

    print("AA")
    return redirect(reverse('pregled_servis'))


@login_required
def dodaj_stavku_racun(request):
    user = request.user
    korisnik = Korisnik.objects.get(user=user)
    if korisnik.pozicija == "SS":
        radni_nalog = RadniNalog.objects.get(id=request.POST['id'])
        if radni_nalog.status != "PR":
            a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
            return redirect(a)

        naziv_stavke = request.POST['naziv_stavke']
        opis = request.POST['opis_stavke']
        cena = float(request.POST['cena_stavke'])
        racun = Racun.objects.get(radni_nalog=radni_nalog)

        if len(opis) < 1:
            opis = "Nema opisa"

        nova_stavka = StavkeRacuna.objects.create(racun=racun, naziv_stavke=naziv_stavke, opis_stavke=opis,
                                                  cena_stavke=cena)
        nova_stavka.save()
        racun.ukupna_cena += cena
        racun.save()
        a = reverse('radni_nalog_kod') + "?kod_slucaja=" + radni_nalog.radni_nalog_kod
        print(a)
        print(redirect(a))
        return redirect(a)
    else:
        return redirect(reverse('index'))
