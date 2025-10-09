from django.contrib import admin
from .models import Utilisateur, Administrateur, Enseignant, Etudiant, Sceance, Presence, Classe, Cours, Anneer, Parent, Semestre
from django.db import models
from django.utils import timezone

# Enregistrement des modèles dans l'admin Django
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'email', 'role')
    search_fields = ('nom', 'prenom', 'email', 'role')
    list_filter = ('role',)
    
@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'utilisateur__email')

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'departement', 'specialite')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'utilisateur__email', 'departement', 'specialite')
    list_filter = ('departement',)

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'numero_etudiant', 'programme', 'annee')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'utilisateur__email', 'numero_etudiant', 'programme')
    list_filter = ('programme',)
    
@admin.register(Sceance)
class SceanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'cours', 'date', 'heure_debut', 'heure_fin', 'etudiant', 'enseignant')
    search_fields = ('cours', 'etudiant__utilisateur__nom', 'enseignant__utilisateur__nom')
    list_filter = ('date',)

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'description', 'enseignant')
    search_fields = ('titre', 'enseignant__utilisateur__nom')
    list_filter = ('enseignant__departement',)
    
@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'sceance', 'Cours', 'enseignant', 'date', 'statut')
    search_fields = ('etudiant__utilisateur__nom', 'sceance__cours', 'Cours__titre', 'enseignant__utilisateur__nom', 'statut')
    list_filter = ('statut', 'date')

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)
    
@admin.register(Anneer)
class AnneerAdmin(admin.ModelAdmin):
    list_display = ('id', 'annee')
    search_fields = ('annee',)
    
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'email', 'telephone')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    
@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'date_debut', 'date_fin')
    search_fields = ('annee',)
    list_filter = ('date_debut', 'date_fin')