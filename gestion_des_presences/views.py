from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Anneer
from .models import Etudiant  # Import the Etudiants model

def accueil(request):
    etudiants = [
        {'nom': 'Dupont', 'prenom': 'Jean',},
        {'nom': 'Martin', 'prenom': 'Claire'},
        {'nom': 'Durand', 'prenom': 'Pierre'},
    ]
    return render(request, 'presence/accueil.html' , {'etudiants': etudiants})

def annees_list(request):
    annees = Anneer.objects.all().order_by('-annee')
    return render(request, 'annee_list.html', {'annees': annees})

def annees_create(request):
    if request.method == 'POST':
        try:
            annee_value = int(request.POST.get('annee'))
            annee = Anneer.objects.create(annee=annee_value)
            return JsonResponse({'success': True, 'annee': {'id': annee.id, 'annee': annee.annee}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=405)

def annees_update(request, pk):
    annee_obj = get_object_or_404(Anneer, pk=pk)
    if request.method == 'POST':
        try:
            annee_value = int(request.POST.get('annee'))
            annee_obj.annee = annee_value
            annee_obj.save()
            return JsonResponse({'success': True, 'annee': {'id': annee_obj.id, 'annee': annee_obj.annee}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=405)

def annees_delete(request, pk):
    annee_obj = get_object_or_404(Anneer, pk=pk)
    if request.method == 'POST':
        annee_obj.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)
def liste_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'liste_etudiants.html', {'etudiants': etudiants})

from django.shortcuts import render, redirect
from .models import Anneer

def liste_annees(request):
    # Récupère toutes les années enregistrées
    annees = Anneer.objects.all().order_by('annee')
    return render(request, 'annees/anne_list.html', {'annees': annees})


def ajouter_annee(request):
    if request.method == 'POST':
        annee_valeur = request.POST.get('annee')
        if annee_valeur:
            Anneer.objects.create(annee=annee_valeur)
        return redirect('liste_annees')
    return render(request, 'ajouter_annee.html')