from django import forms
from .models import Enseignant, Cours
from .models import Etudiant, Anneer


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
