from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import (
    Anneer, Etudiant, Enseignant, Cours, Utilisateur, Administrateur,
    Sceance, Presence, Classe, Inscription, Semestre, Parent
)
from .forms import EnseignantForm, CoursForm
from django.shortcuts import redirect
from .forms import EtudiantForm, AnneerForm
from .forms import UtilisateurForm, AdministrateurForm, SceanceForm, PresenceForm, ClasseForm, InscriptionForm, SemestreForm, ParentForm
from django.contrib import messages

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
            obj = form.save()
            messages.success(request, 'Enseignant créé avec succès.')
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
            messages.success(request, 'Enseignant modifié avec succès.')
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
    form = CoursForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Cours créé avec succès.')
                return redirect('liste_cours')
        except Exception as e:
            # Attach a non-field error to the form so it displays in the template
            form.add_error(None, str(e))
    return render(request, 'cours_form.html', {'form': form, 'title': 'Ajouter un cours'})


def cours_update(request, pk):
    c = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours modifié avec succès.')
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
            messages.success(request, 'Étudiant créé avec succès.')
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


# Utilisateur CRUD
def liste_utilisateurs(request):
    users = Utilisateur.objects.all()
    return render(request, 'liste_utilisateurs.html', {'users': users})


def utilisateur_create(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurForm()
    return render(request, 'utilisateur_form.html', {'form': form, 'title': 'Ajouter un utilisateur'})


def utilisateur_update(request, pk):
    u = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurForm(instance=u)
    return render(request, 'utilisateur_form.html', {'form': form, 'title': 'Modifier un utilisateur'})


def utilisateur_delete(request, pk):
    u = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        u.delete()
        return redirect('liste_utilisateurs')
    return render(request, 'confirm_delete.html', {'object': u, 'type': 'utilisateur'})


# Administrateur CRUD
def liste_administrateurs(request):
    items = Administrateur.objects.select_related('utilisateur').all()
    return render(request, 'liste_administrateurs.html', {'items': items})


def administrateur_create(request):
    if request.method == 'POST':
        form = AdministrateurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrateur créé avec succès.')
            return redirect('liste_administrateurs')
    else:
        form = AdministrateurForm()
    return render(request, 'administrateur_form.html', {'form': form, 'title': 'Ajouter un administrateur'})


def administrateur_update(request, pk):
    a = get_object_or_404(Administrateur, pk=pk)
    if request.method == 'POST':
        form = AdministrateurForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect('liste_administrateurs')
    else:
        form = AdministrateurForm(instance=a)
    return render(request, 'administrateur_form.html', {'form': form, 'title': 'Modifier un administrateur'})


def administrateur_delete(request, pk):
    a = get_object_or_404(Administrateur, pk=pk)
    if request.method == 'POST':
        a.delete()
        return redirect('liste_administrateurs')
    return render(request, 'confirm_delete.html', {'object': a, 'type': 'administrateur'})


# Classe CRUD
def liste_classes(request):
    items = Classe.objects.all()
    return render(request, 'liste_classes.html', {'items': items})


def classe_create(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe créée avec succès.')
            return redirect('liste_classes')
    else:
        form = ClasseForm()
    return render(request, 'classe_form.html', {'form': form, 'title': 'Ajouter une classe'})


def classe_update(request, pk):
    c = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return redirect('liste_classes')
    else:
        form = ClasseForm(instance=c)
    return render(request, 'classe_form.html', {'form': form, 'title': 'Modifier une classe'})


def classe_delete(request, pk):
    c = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        c.delete()
        return redirect('liste_classes')
    return render(request, 'confirm_delete.html', {'object': c, 'type': 'classe'})


# Inscription CRUD
def liste_inscriptions(request):
    items = Inscription.objects.select_related('etudiant', 'classe').all()
    return render(request, 'liste_inscriptions.html', {'items': items})


def inscription_create(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription créée avec succès.')
            return redirect('liste_inscriptions')
    else:
        form = InscriptionForm()
    return render(request, 'inscription_form.html', {'form': form, 'title': 'Ajouter une inscription'})


def inscription_delete(request, pk):
    i = get_object_or_404(Inscription, pk=pk)
    if request.method == 'POST':
        i.delete()
        return redirect('liste_inscriptions')
    return render(request, 'confirm_delete.html', {'object': i, 'type': 'inscription'})


# Semestre CRUD
def liste_semestres(request):
    items = Semestre.objects.all()
    return render(request, 'liste_semestres.html', {'items': items})


def semestre_create(request):
    if request.method == 'POST':
        form = SemestreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semestre créé avec succès.')
            return redirect('liste_semestres')
    else:
        form = SemestreForm()
    return render(request, 'semestre_form.html', {'form': form, 'title': 'Ajouter un semestre'})


def semestre_update(request, pk):
    s = get_object_or_404(Semestre, pk=pk)
    if request.method == 'POST':
        form = SemestreForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('liste_semestres')
    else:
        form = SemestreForm(instance=s)
    return render(request, 'semestre_form.html', {'form': form, 'title': 'Modifier un semestre'})


def semestre_delete(request, pk):
    s = get_object_or_404(Semestre, pk=pk)
    if request.method == 'POST':
        s.delete()
        return redirect('liste_semestres')
    return render(request, 'confirm_delete.html', {'object': s, 'type': 'semestre'})


# Parent CRUD
def liste_parents(request):
    items = Parent.objects.all()
    return render(request, 'liste_parents.html', {'items': items})


def parent_create(request):
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parent créé avec succès.')
            return redirect('liste_parents')
    else:
        form = ParentForm()
    return render(request, 'parent_form.html', {'form': form, 'title': 'Ajouter un parent'})


def parent_update(request, pk):
    p = get_object_or_404(Parent, pk=pk)
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('liste_parents')
    else:
        form = ParentForm(instance=p)
    return render(request, 'parent_form.html', {'form': form, 'title': 'Modifier un parent'})


def parent_delete(request, pk):
    p = get_object_or_404(Parent, pk=pk)
    if request.method == 'POST':
        p.delete()
        return redirect('liste_parents')
    return render(request, 'confirm_delete.html', {'object': p, 'type': 'parent'})


# Sceance CRUD
def liste_sceances(request):
    items = Sceance.objects.select_related('etudiant', 'enseignant').all()
    return render(request, 'liste_sceances.html', {'items': items})


def sceance_create(request):
    if request.method == 'POST':
        form = SceanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Séance créée avec succès.')
            return redirect('liste_sceances')
    else:
        form = SceanceForm()
    return render(request, 'sceance_form.html', {'form': form, 'title': 'Ajouter une séance'})


def sceance_update(request, pk):
    s = get_object_or_404(Sceance, pk=pk)
    if request.method == 'POST':
        form = SceanceForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('liste_sceances')
    else:
        form = SceanceForm(instance=s)
    return render(request, 'sceance_form.html', {'form': form, 'title': 'Modifier une séance'})


def sceance_delete(request, pk):
    s = get_object_or_404(Sceance, pk=pk)
    if request.method == 'POST':
        s.delete()
        return redirect('liste_sceances')
    return render(request, 'confirm_delete.html', {'object': s, 'type': 'séance'})


# Presence CRUD
def liste_presences(request):
    items = Presence.objects.select_related('etudiant', 'sceance', 'cours', 'enseignant').all()
    return render(request, 'liste_presences.html', {'items': items})


def presence_create(request):
    if request.method == 'POST':
        form = PresenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Présence enregistrée avec succès.')
            return redirect('liste_presences')
    else:
        form = PresenceForm()
    return render(request, 'presence_form.html', {'form': form, 'title': 'Ajouter une présence'})


def presence_update(request, pk):
    p = get_object_or_404(Presence, pk=pk)
    if request.method == 'POST':
        form = PresenceForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('liste_presences')
    else:
        form = PresenceForm(instance=p)
    return render(request, 'presence_form.html', {'form': form, 'title': 'Modifier une présence'})


def presence_delete(request, pk):
    p = get_object_or_404(Presence, pk=pk)
    if request.method == 'POST':
        p.delete()
        return redirect('liste_presences')
    return render(request, 'confirm_delete.html', {'object': p, 'type': 'présence'})


def admin_index(request):
    # provide quick counts for the dashboard
    context = {
        'counts': {
            'utilisateurs': Utilisateur.objects.count(),
            'administrateurs': Administrateur.objects.count(),
            'enseignants': Enseignant.objects.count(),
            'etudiants': Etudiant.objects.count(),
            'parents': Parent.objects.count(),
            'cours': Cours.objects.count(),
            'sceances': Sceance.objects.count(),
            'presences': Presence.objects.count(),
            'classes': Classe.objects.count(),
            'semestres': Semestre.objects.count(),
            'annees': Anneer.objects.count(),
            'inscriptions': Inscription.objects.count(),
        }
    }
    return render(request, 'admin_index.html', context)