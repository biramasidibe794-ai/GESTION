# gestion_des_presences/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from .models import Seance

from .models import (
    User, Enseignant, Etudiant, Parent,
    Cours, Classe, Inscription, Semestre, AnneeScolaire,
    Seance, Presence
)


# --- Admin: création et changement de rôle utilisateur -------------------------
ROLE_CHOICES = (
    ("admin", "Admin"),
    ("enseignant", "Enseignant"),
    ("etudiant", "Étudiant"),
    ("parent", "Parent"),
)

class AdminUserCreateForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Rôle")
    is_active = forms.BooleanField(required=False, initial=True, label="Actif ?")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            css = f.widget.attrs.get("class", "")
            f.widget.attrs["class"] = (css + " form-control").strip()
        # Les checkbox peuvent garder leur style par défaut
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"

class UserRoleForm(forms.ModelForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Rôle")
    is_active = forms.BooleanField(required=False, label="Actif ?")

    class Meta:
        model = User
        fields = ("role", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            if isinstance(f.widget, forms.CheckboxInput):
                f.widget.attrs["class"] = "form-check-input"
            else:
                css = f.widget.attrs.get("class", "")
                f.widget.attrs["class"] = (css + " form-control").strip()


# ---------- Enseignant ----------
class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ["user", "departement", "specialite"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "departement": forms.TextInput(attrs={"class": "form-control"}),
            "specialite": forms.TextInput(attrs={"class": "form-control"}),
        }

# ---------- Cours (M2M: enseignants, classes) ----------
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ["titre", "description", "enseignants", "classes"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "enseignants": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
            "classes": forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        }

# ---------- Étudiant ----------
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ["user", "numero_etudiant", "programme"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "numero_etudiant": forms.TextInput(attrs={"class": "form-control"}),
            "programme": forms.TextInput(attrs={"class": "form-control"}),
        }

# ---------- Année scolaire ----------
class AnneeScolaireForm(forms.ModelForm):
    class Meta:
        model = AnneeScolaire
        fields = ["annee"]
        widgets = {
            "annee": forms.NumberInput(attrs={"class": "form-control", "min": 2000, "max": 2100}),
        }

# ---------- Classe ----------
class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ["nom"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
        }

# ---------- Inscription (étudiant -> classe) ----------
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ["etudiant", "classe"]  # statut géré par défaut ("pending") puis approuvé par admin
        widgets = {
            "etudiant": forms.Select(attrs={"class": "form-select"}),
            "classe": forms.Select(attrs={"class": "form-select"}),
        }

# ---------- Semestre ----------
class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = ["nom", "date_debut", "date_fin"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "date_debut": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "date_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

# ---------- Parent ----------
class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ["nom", "prenom", "email", "telephone", "preferences"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "preferences": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

# ---------- Séance ----------
class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ["cours", "classe", "enseignant", "debut", "fin"]
        widgets = {
            "cours": forms.Select(attrs={"class": "form-select"}),
            "classe": forms.Select(attrs={"class": "form-select"}),
            "enseignant": forms.Select(attrs={"class": "form-select"}),
            "debut": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "fin": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

# ---------- Présence ----------
class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ["etudiant", "seance", "statut"]
        widgets = {
            "etudiant": forms.Select(attrs={"class": "form-select"}),
            "seance": forms.Select(attrs={"class": "form-select"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
        }



class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = "__all__"
        widgets = {
            # Utilise des inputs text pour compat max navigateurs; tu peux passer à datetime-local si tu veux
            "debut": forms.TextInput(attrs={"class": "form-control", "placeholder": "2025-10-23 08:00"}),
            "fin": forms.TextInput(attrs={"class": "form-control", "placeholder": "2025-10-23 10:00"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            css = f.widget.attrs.get("class", "")
            if not isinstance(f.widget, forms.CheckboxInput):
                f.widget.attrs["class"] = (css + " form-control").strip()

    def clean(self):
        cleaned = super().clean()
        debut = cleaned.get("debut")
        fin = cleaned.get("fin")
        if debut and fin and fin <= debut:
            raise ValidationError("L'heure de fin doit être strictement après l'heure de début.")
        return cleaned

class EtudiantAssignClassForm(forms.Form):
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )


class AssignClasseForm(forms.Form):
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        label="Classe",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    statut = forms.ChoiceField(
        choices=getattr(Inscription, "STATUTS", (("approved","Approuvée"),("pending","En attente"),("rejected","Refusée"))),
        initial="approved",
        label="Statut",
        widget=forms.Select(attrs={"class": "form-select"})
    )