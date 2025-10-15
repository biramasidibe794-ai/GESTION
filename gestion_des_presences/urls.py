from django.urls import path
from . import views
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('annees/', views.annees_list, name='liste_annees'),
    path('annees/create/', views.annees_create, name='annees_create'),
    path('annees/<int:pk>/update/', views.annees_update, name='annees_update'),
    path('annees/<int:pk>/delete/', views.annees_delete, name='annees_delete'),
    path('annees/ajouter/', views.ajouter_annee, name='ajouter_annee'),
]
