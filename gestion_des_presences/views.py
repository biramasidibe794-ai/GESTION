from django.shortcuts import render
from django.http import HttpResponse
def accueil(request):
    etudiants = [
        {'nom': 'Dupont', 'prenom': 'Jean',},
        {'nom': 'Martin', 'prenom': 'Claire'},
        {'nom': 'Durand', 'prenom': 'Pierre'},
    ]
    return render(request, 'presence/accueil.html' , {'etudiants': etudiants})
