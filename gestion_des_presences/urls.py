from django.urls import path
from . import views
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/ajouter/', views.etudiant_create, name='etudiant_create'),
    path('etudiants/<int:pk>/modifier/', views.etudiant_update, name='etudiant_update'),
    path('etudiants/<int:pk>/supprimer/', views.etudiant_delete, name='etudiant_delete'),
    path('enseignants/', views.liste_enseignants, name='liste_enseignants'),
    path('enseignants/ajouter/', views.enseignant_create, name='enseignant_create'),
    path('enseignants/<int:pk>/modifier/', views.enseignant_update, name='enseignant_update'),
    path('enseignants/<int:pk>/supprimer/', views.enseignant_delete, name='enseignant_delete'),
    path('cours/', views.liste_cours, name='liste_cours'),
    path('cours/ajouter/', views.cours_create, name='cours_create'),
    path('cours/<int:pk>/modifier/', views.cours_update, name='cours_update'),
    path('cours/<int:pk>/supprimer/', views.cours_delete, name='cours_delete'),
    path('annees/', views.annees_list, name='liste_annees'),
    path('annees/ajouter-form/', views.annee_create_form, name='annee_create_form'),
    path('annees/<int:pk>/modifier-form/', views.annee_update_form, name='annee_update_form'),
    path('annees/<int:pk>/supprimer-form/', views.annee_delete_form, name='annee_delete_form'),
    path('annees/create/', views.annees_create, name='annees_create'),
    path('annees/<int:pk>/update/', views.annees_update, name='annees_update'),
    path('annees/<int:pk>/delete/', views.annees_delete, name='annees_delete'),
    path('annees/ajouter/', views.ajouter_annee, name='ajouter_annee'),
    # Utilisateur
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/ajouter/', views.utilisateur_create, name='utilisateur_create'),
    path('utilisateurs/<int:pk>/modifier/', views.utilisateur_update, name='utilisateur_update'),
    path('utilisateurs/<int:pk>/supprimer/', views.utilisateur_delete, name='utilisateur_delete'),
    # Administrateur
    path('administrateurs/', views.liste_administrateurs, name='liste_administrateurs'),
    path('administrateurs/ajouter/', views.administrateur_create, name='administrateur_create'),
    path('administrateurs/<int:pk>/modifier/', views.administrateur_update, name='administrateur_update'),
    path('administrateurs/<int:pk>/supprimer/', views.administrateur_delete, name='administrateur_delete'),
    # Classe
    path('classes/', views.liste_classes, name='liste_classes'),
    path('classes/ajouter/', views.classe_create, name='classe_create'),
    path('classes/<int:pk>/modifier/', views.classe_update, name='classe_update'),
    path('classes/<int:pk>/supprimer/', views.classe_delete, name='classe_delete'),
    # Inscription
    path('inscriptions/', views.liste_inscriptions, name='liste_inscriptions'),
    path('inscriptions/ajouter/', views.inscription_create, name='inscription_create'),
    path('inscriptions/<int:pk>/supprimer/', views.inscription_delete, name='inscription_delete'),
    # Semestre
    path('semestres/', views.liste_semestres, name='liste_semestres'),
    path('semestres/ajouter/', views.semestre_create, name='semestre_create'),
    path('semestres/<int:pk>/modifier/', views.semestre_update, name='semestre_update'),
    path('semestres/<int:pk>/supprimer/', views.semestre_delete, name='semestre_delete'),
    # Parent
    path('parents/', views.liste_parents, name='liste_parents'),
    path('parents/ajouter/', views.parent_create, name='parent_create'),
    path('parents/<int:pk>/modifier/', views.parent_update, name='parent_update'),
    path('parents/<int:pk>/supprimer/', views.parent_delete, name='parent_delete'),
    # Sceance
    path('sceances/', views.liste_sceances, name='liste_sceances'),
    path('sceances/ajouter/', views.sceance_create, name='sceance_create'),
    path('sceances/<int:pk>/modifier/', views.sceance_update, name='sceance_update'),
    path('sceances/<int:pk>/supprimer/', views.sceance_delete, name='sceance_delete'),
    # Presence
    path('presences/', views.liste_presences, name='liste_presences'),
    path('presences/ajouter/', views.presence_create, name='presence_create'),
    path('presences/<int:pk>/modifier/', views.presence_update, name='presence_update'),
    path('presences/<int:pk>/supprimer/', views.presence_delete, name='presence_delete'),
    # Admin index
    path('admin-index/', views.admin_index, name='admin_index'),
]
