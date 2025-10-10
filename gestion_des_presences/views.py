from django.shortcuts import render
from django.http import HttpResponse
from .models import Etudiant
def accueil(request):
    etudiants = [
        {'nom': 'Dupont', 'prenom': 'Jean',},
        {'nom': 'Martin', 'prenom': 'Claire'},
        {'nom': 'Durand', 'prenom': 'Pierre'},
    ]
    return render(request, 'presence/accueil.html' , {'etudiants': etudiants})

# Nouvelle vue pour lister les étudiants
def liste_etudiants(request):
    etudiants= Etudiant.objects.all()
    return render(request, 'liste_etudiants.html', {'etudiants': etudiants})
