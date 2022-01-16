from django.urls import path
from .views import *

urlpatterns = [
    path('', pregled_servis, name="pregled_servis"),
    path('radni_nalog/', radni_nalog_kod, name="radni_nalog_kod"),
    path('provera_kod/', postoji_kod, name="provera_kod"),

    path('kreairaj_nalog/', kreairaj_nalog, name="kreairaj_nalog"),
    path('kreairanje_radnog_naloga/', kreairanje_radnog_naloga, name="kreairanje_radnog_naloga"),

    path('posalji_na_proveru/<int:id>', posalji_na_proveru, name="posalji_na_proveru"),

    path('oznaci_prekinut/<int:id>', oznaci_prekinut, name="oznaci_prekinut"),
    path('oznaci_pr/<int:id>', oznaci_pr, name="oznaci_pr"),
    path('oznaci_ok/<int:id>', oznaci_ok, name="oznaci_ok"),

    path('dodaj_progres/', dodaj_progres, name="dodaj_progres"),
    path('obrisi_progres/<int:id>', obrisi_progres, name="obrisi_progres"),

    path('naruci_deo/', naruci_deo, name="naruci_deo"),
    path('sef_odbio_deo/<int:id>', sef_odbio_deo, name="sef_odbio_deo"),
    path('sef_prihvatio_deo/<int:id>', sef_prihvatio_deo, name="sef_prihvatio_deo"),

    path('magacin_odbio_deo/<int:id>', magacin_odbio_deo, name="magacin_odbio_deo"),
    path('magacin_prihvatio_deo/<int:id>', magacin_prihvatio_deo, name="magacin_prihvatio_deo"),

    path('dodaj_stavku_racun/', dodaj_stavku_racun, name="dodaj_stavku_racun"),

]
