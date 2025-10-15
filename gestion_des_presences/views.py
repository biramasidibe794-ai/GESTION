from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Anneer
from .models import Etudiant  # Import the Etudiants model
from .models import Enseignant, Cours
from .forms import EnseignantForm, CoursForm
from django.shortcuts import redirect
from .forms import EtudiantForm, AnneerForm

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


# Enseignants CRUD
def enseignant_create(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_enseignants')
    else:
        form = EnseignantForm()
    return render(request, 'enseignant_form.html', {'form': form, 'title': 'Ajouter un enseignant'})


def enseignant_update(request, pk):
    ens = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        form = EnseignantForm(request.POST, instance=ens)
        if form.is_valid():
            form.save()
            return redirect('liste_enseignants')
    else:
        form = EnseignantForm(instance=ens)
    return render(request, 'enseignant_form.html', {'form': form, 'title': 'Modifier un enseignant'})


def enseignant_delete(request, pk):
    ens = get_object_or_404(Enseignant, pk=pk)
    if request.method == 'POST':
        ens.delete()
        return redirect('liste_enseignants')
    return render(request, 'confirm_delete.html', {'object': ens, 'type': 'enseignant'})


# Cours CRUD
def cours_create(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cours')
    else:
        form = CoursForm()
    return render(request, 'cours_form.html', {'form': form, 'title': 'Ajouter un cours'})


def cours_update(request, pk):
    c = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return redirect('liste_cours')
    else:
        form = CoursForm(instance=c)
    return render(request, 'cours_form.html', {'form': form, 'title': 'Modifier un cours'})


def cours_delete(request, pk):
    c = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        c.delete()
        return redirect('liste_cours')
    return render(request, 'confirm_delete.html', {'object': c, 'type': 'cours'})

def ajouter_annee(request):
    # page de formulaire (GET) — la soumission POST est gérée par `annees_create` qui retourne JSON
    if request.method == 'GET':
        return render(request, 'ajouter_annee.html')
    return JsonResponse({'success': False}, status=405)


# Etudiant CRUD
def etudiant_create(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_etudiants')
    else:
        form = EtudiantForm()
    return render(request, 'etudiant_form.html', {'form': form, 'title': 'Ajouter un étudiant'})


def etudiant_update(request, pk):
    e = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=e)
        if form.is_valid():
            form.save()
            return redirect('liste_etudiants')
    else:
        form = EtudiantForm(instance=e)
    return render(request, 'etudiant_form.html', {'form': form, 'title': 'Modifier un étudiant'})


def etudiant_delete(request, pk):
    e = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        e.delete()
        return redirect('liste_etudiants')
    return render(request, 'confirm_delete.html', {'object': e, 'type': 'étudiant'})


# Annee form-based create/update/delete (UI)
def annee_create_form(request):
    if request.method == 'POST':
        form = AnneerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_annees')
    else:
        form = AnneerForm()
    return render(request, 'ajouter_annee.html', {'form': form})


def annee_update_form(request, pk):
    a = get_object_or_404(Anneer, pk=pk)
    if request.method == 'POST':
        form = AnneerForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect('liste_annees')
    else:
        form = AnneerForm(instance=a)
    return render(request, 'ajouter_annee.html', {'form': form, 'title': 'Modifier une année'})


def annee_delete_form(request, pk):
    a = get_object_or_404(Anneer, pk=pk)
    if request.method == 'POST':
        a.delete()
        return redirect('liste_annees')
    return render(request, 'confirm_delete.html', {'object': a, 'type': 'année'})