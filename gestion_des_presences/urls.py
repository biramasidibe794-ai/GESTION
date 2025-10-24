from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
     path("dashboard/", views.admin_index, name="admin_index"), 

    path("annees/", views.annees_list, name="liste_annees"),
    path("annees/add/", views.annees_create, name="annees_create"),
    path("annees/<int:pk>/update/", views.annees_update, name="annees_update"),
    path("annees/<int:pk>/delete/", views.annees_delete, name="annees_delete"),
    path("annees/form/add/", views.annee_create_form, name="annee_create_form"),
    path("annees/form/<int:pk>/update/", views.annee_update_form, name="annee_update_form"),
    path("annees/form/<int:pk>/delete/", views.annee_delete_form, name="annee_delete_form"),

    path("etudiants/", views.liste_etudiants, name="liste_etudiants"),
    path("etudiants/add/", views.etudiant_create, name="etudiant_create"),
    path("etudiants/<int:pk>/update/", views.etudiant_update, name="etudiant_update"),
    path("etudiants/<int:pk>/delete/", views.etudiant_delete, name="etudiant_delete"),
    path("etudiants/<int:pk>/assign/", views.etudiant_assign_class, name="etudiant_assign_class"),

    path("enseignants/", views.liste_enseignants, name="liste_enseignants"),
    path("enseignants/add/", views.enseignant_create, name="enseignant_create"),
    path("enseignants/<int:pk>/update/", views.enseignant_update, name="enseignant_update"),
    path("enseignants/<int:pk>/delete/", views.enseignant_delete, name="enseignant_delete"),

    path("cours/", views.liste_cours, name="liste_cours"),
    path("cours/add/", views.cours_create, name="cours_create"),
    path("cours/<int:pk>/update/", views.cours_update, name="cours_update"),
    path("cours/<int:pk>/delete/", views.cours_delete, name="cours_delete"),

    path("classes/", views.liste_classes, name="liste_classes"),
    path("classes/add/", views.classe_create, name="classe_create"),
    path("classes/<int:pk>/update/", views.classe_update, name="classe_update"),
    path("classes/<int:pk>/delete/", views.classe_delete, name="classe_delete"),

    path("inscriptions/", views.liste_inscriptions, name="liste_inscriptions"),
    path("inscriptions/add/", views.inscription_create, name="inscription_create"),
    path("inscriptions/<int:pk>/delete/", views.inscription_delete, name="inscription_delete"),

    path("semestres/", views.liste_semestres, name="liste_semestres"),
    path("semestres/add/", views.semestre_create, name="semestre_create"),
    path("semestres/<int:pk>/update/", views.semestre_update, name="semestre_update"),
    path("semestres/<int:pk>/delete/", views.semestre_delete, name="semestre_delete"),

    path("parents/", views.liste_parents, name="liste_parents"),
    path("parents/add/", views.parent_create, name="parent_create"),
    path("parents/<int:pk>/update/", views.parent_update, name="parent_update"),
    path("parents/<int:pk>/delete/", views.parent_delete, name="parent_delete"),

    path("seances/", views.liste_seances, name="liste_seances"),
    path("seances/add/", views.seance_create, name="seance_create"),
    path("seances/<int:pk>/update/", views.seance_update, name="seance_update"),
    path("seances/<int:pk>/delete/", views.seance_delete, name="seance_delete"),

    path("presences/", views.liste_presences, name="liste_presences"),
    path("presences/add/", views.presence_create, name="presence_create"),
    path("presences/<int:pk>/update/", views.presence_update, name="presence_update"),
    path("presences/<int:pk>/delete/", views.presence_delete, name="presence_delete"),

    path("activate/", views.activate, name="activate"),
    path("presence/scan/", views.scan_qr, name="scan_qr"),
    
    # Authentification / Inscription
    path("signup/", views.signup, name="signup"),
    path("signup/done/", views.signup_done, name="signup_done"),
    path("activate/", views.activate, name="activate"),
    path("activation/resend/", views.resend_activation, name="resend_activation"),
    path("scanner/", views.qr_scanner, name="qr_scanner"),
    path("users/", views.admin_user_list, name="admin_user_list"),
    path("users/add/", views.admin_user_create, name="admin_user_create"),
    path("users/<int:pk>/role/", views.admin_user_update_role, name="admin_user_update_role"),
    path("seances/<int:pk>/qr/", views.seance_qr_page, name="seance_qr_page"),
    path("seances/<int:pk>/qr.png", views.seance_qr_png, name="seance_qr_png"),
    path("moi/seances/", views.etu_mes_seances, name="etu_mes_seances"),
    path("moi/cours/", views.etu_mes_cours, name="etu_mes_cours"),
    path("moi/presences/", views.etu_mes_presences, name="etu_mes_presences"),

        
]
