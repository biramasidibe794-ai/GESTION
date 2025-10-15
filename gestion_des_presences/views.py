from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Anneer
from .models import Etudiant  # Import the Etudiants model
from .models import Enseignant, Cours

def accueil(request):
    return render(request, 'presence/accueil.html')

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


def liste_enseignants(request):
    enseignants = Enseignant.objects.select_related('utilisateur').all()
    return render(request, 'liste_enseignants.html', {'enseignants': enseignants})


def liste_cours(request):
    cours = Cours.objects.select_related('enseignant__utilisateur').all()
    return render(request, 'liste_cours.html', {'cours': cours})

def ajouter_annee(request):
    # page de formulaire (GET) — la soumission POST est gérée par `annees_create` qui retourne JSON
    if request.method == 'GET':
        return render(request, 'ajouter_annee.html')
    return JsonResponse({'success': False}, status=405)