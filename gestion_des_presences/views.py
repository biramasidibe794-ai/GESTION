from django.shortcuts import render
from django.http import HttpResponse
from .models import Etudiants
def accueil(request):
    etudiants = [
        {'nom': 'Dupont', 'prenom': 'Jean',},
        {'nom': 'Martin', 'prenom': 'Claire'},
        {'nom': 'Durand', 'prenom': 'Pierre'},
    ]
    return render(request, 'presence/accueil.html' , {'etudiants': etudiants})


def liste_etudiants(request):
    etudiants= Etudiants.objects.all()
    return render(request, 'presence/liste_etudiants.html', {'etudiants': etudiants})
