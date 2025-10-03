from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100, default='changeme')
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email})"

    class Meta:
        ordering = ['nom', 'prenom']

class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    permissions = JSONField(default=dict, blank=True)
    def __str__(self):
        return f"Administrateur: {self.utilisateur.nom} {self.utilisateur.prenom}"
class Enseignant(models.Model):
    def __str__(self):
        return f"Enseignant: {self.utilisateur.nom} {self.utilisateur.prenom}"
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numero_etudiant = models.CharField(max_length=20, unique=True)
    programme = models.CharField(max_length=100)
    Anneer=models.ForeignKey('Anneer', on_delete=models.SET_NULL, blank=True, null=True)
    Parents = models.ForeignKey('Parent', on_delete=models.SET_NULL, blank=True, null=True) 
    def __str__(self):
        return f"Etudiant: {self.utilisateur.nom} {self.utilisateur.prenom} ({self.numero_etudiant})"
class Cours(models.Model):
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE) 
    def __str__(self):
        return f"Cours: {self.titre}"
class Presence(models.Model):
    id = models.AutoField(primary_key=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    Cours = models.ForeignKey(Cours, default=1, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    date = models.DateField()
    STATUT_CHOICES = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    def __str__(self):
        return f"Presence: {self.etudiant} - {self.date} - {self.statut}"
class Classe(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    def __str__(self):
        return f"Classe: {self.nom} ({self.horaire})"
class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    date_inscription = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.etudiant} inscrit à {self.classe}"
class Semestre(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)  # e.g., 'Semestre 1'
    date_debut = models.DateField()
    date_fin = models.DateField()
    def __str__(self):
        return f"Semestre: {self.nom}"

class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    notifications_enabled = models.BooleanField(default=True)
    notification_preferences = JSONField(default=dict, blank=True)
    def __str__(self):
        return f"Parent: {self.nom} {self.prenom} ({self.email})"
class Anneer(models.Model):
    id = models.AutoField(primary_key=True)
    annee = models.IntegerField(unique=True, validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    def __str__(self):
        return f"Année: {self.annee}"
