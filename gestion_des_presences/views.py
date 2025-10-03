from django.shortcuts import render, get_object_or_404, redirect
from .models import Anneer
from .forms import AnneerForm # type: ignore

# --- Liste des années ---
def liste_annees(request):
    annees = Anneer.objects.all().order_by('annee')
    return render(request, 'liste_annees.html', {'annees': annees})

# --- Ajouter une année ---
def ajouter_annee(request):
    if request.method == 'POST':
        form = AnneerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_annees')
    else:
        form = AnneerForm()
    return render(request, 'form_annee.html', {'form': form, 'action': 'Ajouter'})

# --- Modifier une année ---
def modifier_annee(request, annee_id):
    annee = get_object_or_404(Anneer, id=annee_id)
    if request.method == 'POST':
        form = AnneerForm(request.POST, instance=annee)
        if form.is_valid():
            form.save()
            return redirect('liste_annees')
    else:
        form = AnneerForm(instance=annee)
    return render(request, 'form_annee.html', {'form': form, 'action': 'Modifier'})

# --- Supprimer une année ---
def supprimer_annee(request, annee_id):
    annee = get_object_or_404(Anneer, id=annee_id)
    if request.method == 'POST':
        annee.delete()
        return redirect('liste_annees')
    return render(request, 'supprimer_annee.html', {'annee': annee})