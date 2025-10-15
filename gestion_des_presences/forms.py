from django import forms
from .models import Enseignant, Cours
from .models import Etudiant, Anneer

from .models import Utilisateur, Administrateur, Sceance, Presence, Classe, Inscription, Semestre, Parent


class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['utilisateur', 'departement', 'specialite']
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'departement': forms.TextInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'description', 'enseignant']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'enseignant': forms.Select(attrs={'class': 'form-select'}),
        }


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['utilisateur', 'numero_etudiant', 'programme', 'annee', 'parents']
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'numero_etudiant': forms.TextInput(attrs={'class': 'form-control'}),
            'programme': forms.TextInput(attrs={'class': 'form-control'}),
            'annee': forms.Select(attrs={'class': 'form-select'}),
            'parents': forms.Select(attrs={'class': 'form-select'}),
        }


class AnneerForm(forms.ModelForm):
    class Meta:
        model = Anneer
        fields = ['annee']
        widgets = {
            'annee': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': 2100}),
        }


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'mot_de_passe', 'role', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdministrateurForm(forms.ModelForm):
    class Meta:
        model = Administrateur
        fields = ['utilisateur', 'permissions']
        widgets = {
            'utilisateur': forms.Select(attrs={'class': 'form-select'}),
            'permissions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SceanceForm(forms.ModelForm):
    class Meta:
        model = Sceance
        fields = ['cours', 'date', 'heure_debut', 'heure_fin', 'etudiant', 'enseignant']
        widgets = {
            'cours': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'etudiant': forms.Select(attrs={'class': 'form-select'}),
            'enseignant': forms.Select(attrs={'class': 'form-select'}),
        }


class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['etudiant', 'sceance', 'cours', 'enseignant', 'date', 'statut']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-select'}),
            'sceance': forms.Select(attrs={'class': 'form-select'}),
            'cours': forms.Select(attrs={'class': 'form-select'}),
            'enseignant': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }


class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['etudiant', 'classe']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-select'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
        }


class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = ['nom', 'date_debut', 'date_fin']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['nom', 'prenom', 'email', 'telephone', 'notifications_enabled', 'notification_preferences']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'notifications_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_preferences': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
