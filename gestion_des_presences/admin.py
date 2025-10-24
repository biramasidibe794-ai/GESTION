# gestion_des_presences/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User, Enseignant, Etudiant, Parent,
    AnneeScolaire, Semestre, Classe, Cours,
    Inscription, Seance, SeanceQR, Presence,
    ActivationToken
)

# ----- User -----
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # champs affichés dans la liste
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active", "is_staff", "date_joined")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    # champs sur la page d’édition
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Infos personnelles", {"fields": ("first_name", "last_name", "email", "telephone")}),
        ("Rôle", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "role", "telephone", "password1", "password2"),
        }),
    )

# ----- Profils -----
@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ("user", "departement", "specialite")
    search_fields = ("user__username", "user__first_name", "user__last_name", "departement", "specialite")

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ("user", "numero_etudiant", "programme")
    search_fields = ("user__username", "user__first_name", "user__last_name", "numero_etudiant", "programme")

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "email", "telephone")
    search_fields = ("nom", "prenom", "email")

# ----- Scolarité -----
@admin.register(AnneeScolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ("annee",)
    search_fields = ("annee",)

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ("nom", "date_debut", "date_fin")
    list_filter = ("date_debut", "date_fin")
    search_fields = ("nom",)

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ("titre",)
    search_fields = ("titre", "description")
    filter_horizontal = ("enseignants", "classes")

# ----- Inscriptions -----
@admin.action(description="Approuver les inscriptions sélectionnées")
def approve_inscriptions(modeladmin, request, queryset):
    from django.utils import timezone
    admin_user = request.user
    for ins in queryset:
        ins.approve(admin_user)

@admin.action(description="Rejeter les inscriptions sélectionnées")
def reject_inscriptions(modeladmin, request, queryset):
    admin_user = request.user
    for ins in queryset:
        ins.reject(admin_user)

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "classe", "statut", "demande_le", "approuve_le", "approuve_par")
    list_filter = ("statut", "classe")
    search_fields = ("etudiant__user__username", "etudiant__user__first_name", "etudiant__user__last_name", "classe__nom")
    actions = [approve_inscriptions, reject_inscriptions]

# ----- Présences & Séances -----
class SeanceQRInline(admin.TabularInline):
    model = SeanceQR
    extra = 0
    readonly_fields = ("token", "expires_at", "rotating")

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ("cours", "classe", "enseignant", "debut", "fin")
    list_filter = ("classe", "enseignant", "debut")
    search_fields = ("cours__titre", "classe__nom", "enseignant__user__last_name", "enseignant__user__first_name")
    inlines = [SeanceQRInline]

@admin.register(SeanceQR)
class SeanceQRAdmin(admin.ModelAdmin):
    list_display = ("seance", "token", "expires_at", "rotating")
    list_filter = ("rotating",)
    search_fields = ("seance__cours__titre",)
    readonly_fields = ("token",)

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "seance", "statut", "horodatage")
    list_filter = ("statut", "seance__classe", "seance__cours")
    search_fields = ("etudiant__user__username", "etudiant__user__first_name", "etudiant__user__last_name")

# ----- Activation -----
@admin.register(ActivationToken)
class ActivationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expires_at", "used_at", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("token", "created_at", "updated_at")
