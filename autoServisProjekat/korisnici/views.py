from django.shortcuts import render, reverse, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User
from .models import Korisnik


# Create your views here.
def index(request):
    return render(request, 'index.html')

def prijava_stranica(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return render(request, 'prijava.html')
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        print(password)
        try:
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                login(request, user=auth_user)
                return redirect(reverse('pregled_servis'))

            else:
                return render(request, 'prijava.html', {"fail": True})
        except Exception as E:
            print(E)
            return render(request, 'prijava.html', {"fail": True})

    else:
        return render(request, 'prijava.html')

@login_required
def odjava(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))





