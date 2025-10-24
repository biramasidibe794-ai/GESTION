from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid

# ---------- utilitaire timestamps ----------
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# ---------- utilisateur + profils ----------
class User(AbstractUser, TimeStampedModel):
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

# models.py
class Enseignant(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE,
                                related_name="profil_enseignant",
                                null=True, blank=True)  # <<< temporaire
    departement = models.CharField(max_length=100, blank=True)
    specialite  = models.CharField(max_length=100, blank=True)

class Etudiant(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE,
                                related_name="profil_etudiant",
                                null=True, blank=True)  # <<< temporaire
    numero_etudiant = models.CharField(max_length=20, unique=True)
    programme = models.CharField(max_length=100)

class Parent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return f"Parent: {self.nom} {self.prenom}"

# ---------- activation de compte ----------
class ActivationToken(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="activation_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()          # ex: timezone.now() + timedelta(hours=48)
    used_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        return self.used_at is None and timezone.now() <= self.expires_at

    def __str__(self):
        return f"ActivationToken(user={self.user_id}, used={bool(self.used_at)})"

# ---------- scolarité ----------
class AnneeScolaire(models.Model):
    annee = models.IntegerField(unique=True)
    class Meta:
        verbose_name = "Année scolaire"
        verbose_name_plural = "Années scolaires"
    def __str__(self):
        return str(self.annee)

class Semestre(models.Model):
    nom = models.CharField(max_length=50)        # ex: "Semestre 1"
    date_debut = models.DateField()
    date_fin   = models.DateField()
    def __str__(self):
        return f"{self.nom} ({self.date_debut} → {self.date_fin})"

class Classe(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"Classe: {self.nom}"

class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    enseignants = models.ManyToManyField(Enseignant, related_name="cours", blank=True)
    classes     = models.ManyToManyField(Classe, related_name="cours", blank=True)
    def __str__(self):
        return f"Cours: {self.titre}"

class Inscription(models.Model):
    STATUT_CHOICES = [
        ("pending",  "En attente"),
        ("approved", "Approuvée"),
        ("rejected", "Rejetée"),
    ]
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="inscriptions")
    classe   = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="inscrits")
    statut   = models.CharField(max_length=10, choices=STATUT_CHOICES, default="pending")
    demande_le  = models.DateTimeField(default=timezone.now)
    approuve_le = models.DateTimeField(null=True, blank=True)
    approuve_par = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="inscriptions_validees"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["etudiant", "classe"], name="uniq_inscription_etudiant_classe"),
        ]
        indexes = [models.Index(fields=["classe"]), models.Index(fields=["statut"])]

    def approve(self, admin_user):
        self.statut = "approved"
        self.approuve_le = timezone.now()
        self.approuve_par = admin_user
        self.save(update_fields=["statut", "approuve_le", "approuve_par"])

    def reject(self, admin_user):
        self.statut = "rejected"
        self.approuve_le = timezone.now()
        self.approuve_par = admin_user
        self.save(update_fields=["statut", "approuve_le", "approuve_par"])

    def __str__(self):
        return f"Inscription({self.etudiant} -> {self.classe}) [{self.statut}]"

# ---------- présence & QR ----------
class Seance(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.PROTECT, related_name="seances")
    classe = models.ForeignKey(Classe, on_delete=models.PROTECT, related_name="seances")
    enseignant = models.ForeignKey(Enseignant, on_delete=models.PROTECT, related_name="seances")
    debut = models.DateTimeField()
    fin   = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["debut"]), models.Index(fields=["classe"])]
        verbose_name = "Séance"

    def __str__(self):
        return f"Seance({self.cours.titre} - {self.classe.nom} - {self.debut:%Y-%m-%d %H:%M})"

    def is_now_within_window(self, before_minutes=10, after_minutes=10):
        now = timezone.now()
        return (self.debut - timedelta(minutes=before_minutes)) <= now <= (self.fin + timedelta(minutes=after_minutes))

class SeanceQR(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="qr_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    rotating = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["seance"]), models.Index(fields=["expires_at"])]

    def __str__(self):
        return f"SeanceQR(seance={self.seance_id}, exp={self.expires_at:%H:%M:%S})"

    @classmethod
    def issue(cls, seance, ttl_seconds=60, rotating=True):
        return cls.objects.create(
            seance=seance,
            expires_at=timezone.now() + timedelta(seconds=ttl_seconds),
            rotating=rotating,
        )

    def is_valid(self):
        return timezone.now() <= self.expires_at

class Presence(models.Model):
    STATUT_CHOICES = [('present','Présent'), ('absent','Absent')]
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="presences")
    seance   = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name="presences")
    statut   = models.CharField(max_length=10, choices=STATUT_CHOICES, default='present')
    horodatage = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict, blank=True)  # device/ip/ua/ar

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["etudiant", "seance"], name="uniq_presence_etudiant_seance"),
        ]
        indexes = [models.Index(fields=["seance"]), models.Index(fields=["etudiant"])]

    def __str__(self):
        return f"Presence({self.etudiant} @ {self.seance} => {self.statut})"


class EtudiantCours(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('etudiant', 'cours')

    def __str__(self):
        try:
            return f"{self.etudiant} -> {self.cours}"
        except Exception:
            return super().__str__()

# --- Signals: auto-inscription après affectation à une classe ------------------
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save, sender=Inscription)
def auto_enroll_after_inscription(sender, instance, created, **kwargs):
    """
    Quand une Inscription(etudiant, classe) passe (ou est créée) en 'approved':
    - rattache l'étudiant à tous les Cours de la classe (EtudiantCours)
    - pré-crée des Presence 'absent' pour les Seance FUTURES de cette classe
    """
    if instance.statut != "approved":
        return

    etu = instance.etudiant
    classe = instance.classe

    # 1) Rattacher à tous les cours de la classe
    from .models import Cours, EtudiantCours
    cours_qs = Cours.objects.filter(classes=classe).distinct()
    for cours in cours_qs:
        EtudiantCours.objects.get_or_create(etudiant=etu, cours=cours)

    # 2) Pré-créer des présences 'absent' pour les séances futures
    now = timezone.now()
    from .models import Seance, Presence
    seances = Seance.objects.filter(classe=classe, debut__gte=now)
    for s in seances:
        Presence.objects.get_or_create(
            etudiant=etu, seance=s,
            defaults={"statut": "absent"}  # adapte si tes choices diffèrent
        )
