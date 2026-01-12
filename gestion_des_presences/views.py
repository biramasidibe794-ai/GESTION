# gestion_des_presences/views.py
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET  # <-- manquait
from django.urls import reverse
from uuid import uuid4                               # <-- nécessaire pour le QR
from io import BytesIO                                # <-- nécessaire pour le QR
import qrcode     
from datetime import timedelta
from django.utils import timezone
# gestion_des_presences/views.py
from .forms import AssignClasseForm  # <-- AJOUT



from django.contrib import messages
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    # nouveaux modèles
    User, Etudiant, Enseignant, Parent,
    AnneeScolaire, Semestre, Classe, Cours,
    Inscription, Seance, SeanceQR, Presence, ActivationToken
)

# Adapte ces imports à TES noms de formulaires réels
from .forms import (
    EtudiantForm, EnseignantForm, CoursForm, AnneeScolaireForm,
    ClasseForm, InscriptionForm, SemestreForm, ParentForm,
    SeanceForm, PresenceForm
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail

from datetime import timedelta
from .models import ActivationToken, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# -------------------- Années scolaires (JSON + vues) --------------------

def annees_list(request):
    annees = AnneeScolaire.objects.all().order_by("-annee")
    return render(request, "annee_list.html", {"annees": annees})

def annees_create(request):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)
    try:
        annee_value = int(request.POST.get("annee"))
        annee = AnneeScolaire.objects.create(annee=annee_value)
        return JsonResponse({"success": True, "annee": {"id": annee.id, "annee": annee.annee}})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

def annees_update(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)
    annee_obj = get_object_or_404(AnneeScolaire, pk=pk)
    try:
        annee_value = int(request.POST.get("annee"))
        annee_obj.annee = annee_value
        annee_obj.save()
        return JsonResponse({"success": True, "annee": {"id": annee_obj.id, "annee": annee_obj.annee}})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

def annees_delete(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)
    annee_obj = get_object_or_404(AnneeScolaire, pk=pk)
    annee_obj.delete()
    return JsonResponse({"success": True})

def ajouter_annee(request):
    # page de formulaire (GET) — la soumission POST peut passer par annees_create (JSON) ou par annee_create_form
    if request.method == "GET":
        return render(request, "ajouter_annee.html")
    return JsonResponse({"success": False}, status=405)

def annee_create_form(request):
    if request.method == "POST":
        form = AnneeScolaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("liste_annees")
    else:
        form = AnneeScolaireForm()
    return render(request, "ajouter_annee.html", {"form": form})

def annee_update_form(request, pk):
    a = get_object_or_404(AnneeScolaire, pk=pk)
    if request.method == "POST":
        form = AnneeScolaireForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return redirect("liste_annees")
    else:
        form = AnneeScolaireForm(instance=a)
    return render(request, "ajouter_annee.html", {"form": form, "title": "Modifier une année"})

def annee_delete_form(request, pk):
    a = get_object_or_404(AnneeScolaire, pk=pk)
    if request.method == "POST":
        a.delete()
        return redirect("liste_annees")
    return render(request, "confirm_delete.html", {"object": a, "type": "année"})

# -------------------- Étudiants --------------------

def liste_etudiants(request):
    etudiants = Etudiant.objects.select_related("user").all()
    return render(request, "liste_etudiants.html", {"etudiants": etudiants})

def etudiant_create(request):
    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Étudiant créé avec succès.")
            return redirect("liste_etudiants")
    else:
        form = EtudiantForm()
    return render(request, "etudiant_form.html", {"form": form, "title": "Ajouter un étudiant"})

def etudiant_update(request, pk):
    e = get_object_or_404(Etudiant, pk=pk)
    if request.method == "POST":
        form = EtudiantForm(request.POST, instance=e)
        if form.is_valid():
            form.save()
            return redirect("liste_etudiants")
    else:
        form = EtudiantForm(instance=e)
    return render(request, "etudiant_form.html", {"form": form, "title": "Modifier un étudiant"})

def etudiant_delete(request, pk):
    e = get_object_or_404(Etudiant, pk=pk)
    if request.method == "POST":
        e.delete()
        return redirect("liste_etudiants")
    return render(request, "confirm_delete.html", {"object": e, "type": "étudiant"})


@login_required
def etu_mes_seances(request):
    """
    Séances de la/les classe(s) où l'étudiant est inscrit (approved).
    Affiche aujourd'hui + à venir (les plus proches en premier).
    """
    # Profil étudiant
    etu = getattr(request.user, "profil_etudiant", None)
    if not etu:
        messages.error(request, "Vous n'êtes pas un étudiant.")
        return redirect("accueil")

    # Séances liées aux classes où l'inscription est 'approved'
    from .models import Seance, Inscription
    now = timezone.now()

    seances = (
        Seance.objects
        .select_related("classe", "cours", "enseignant__user")
        .filter(
            classe__in=Inscription.objects.filter(etudiant=etu, statut="approved")
                                           .values_list("classe_id", flat=True),
            fin__gte=now  # aujourd'hui et à venir
        )
        .order_by("debut")
    )

    return render(request, "etu_mes_seances.html", {"seances": seances})


@login_required
def etu_mes_cours(request):
    """
    Cours accessibles via la/les classe(s) approuvées de l'étudiant.
    """
    etu = getattr(request.user, "profil_etudiant", None)
    if not etu:
        messages.error(request, "Vous n'êtes pas un étudiant.")
        return redirect("accueil")

    from .models import Cours, Inscription
    cours = (
        Cours.objects.filter(classes__in=Inscription.objects.filter(
            etudiant=etu, statut="approved").values_list("classe_id", flat=True))
        .prefetch_related("enseignants__user", "classes")
        .distinct()
        .order_by("nom")
    )
    return render(request, "etu_mes_cours.html", {"cours": cours})


@login_required
def etu_mes_presences(request):
    """
    Historique des présences de l'étudiant (toutes séances liées à ses classes).
    """
    etu = getattr(request.user, "profil_etudiant", None)
    if not etu:
        messages.error(request, "Vous n'êtes pas un étudiant.")
        return redirect("accueil")

    from .models import Presence
    presences = (
        Presence.objects
        .select_related("seance__classe", "seance__cours", "seance__enseignant__user")
        .filter(etudiant=etu)
        .order_by("-seance__debut")
    )
    return render(request, "etu_mes_presences.html", {"presences": presences})

# -------------------- Enseignants --------------------

def liste_enseignants(request):
    enseignants = Enseignant.objects.select_related("user").all()
    return render(request, "liste_enseignants.html", {"enseignants": enseignants})

def enseignant_create(request):
    if request.method == "POST":
        form = EnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enseignant créé avec succès.")
            return redirect("liste_enseignants")
    else:
        form = EnseignantForm()
    return render(request, "enseignant_form.html", {"form": form, "title": "Ajouter un enseignant"})

def enseignant_update(request, pk):
    ens = get_object_or_404(Enseignant, pk=pk)
    if request.method == "POST":
        form = EnseignantForm(request.POST, instance=ens)
        if form.is_valid():
            form.save()
            messages.success(request, "Enseignant modifié avec succès.")
            return redirect("liste_enseignants")
    else:
        form = EnseignantForm(instance=ens)
    return render(request, "enseignant_form.html", {"form": form, "title": "Modifier un enseignant"})

def enseignant_delete(request, pk):
    ens = get_object_or_404(Enseignant, pk=pk)
    if request.method == "POST":
        ens.delete()
        return redirect("liste_enseignants")
    return render(request, "confirm_delete.html", {"object": ens, "type": "enseignant"})

# -------------------- Cours --------------------

def liste_cours(request):
    # Cours possède M2M vers enseignants et classes → prefetch_related
    cours = Cours.objects.prefetch_related("enseignants__user", "classes").all()
    return render(request, "liste_cours.html", {"cours": cours})

def cours_create(request):
    form = CoursForm(request.POST or None)
    if request.method == "POST":
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Cours créé avec succès.")
                return redirect("liste_cours")
        except Exception as e:
            form.add_error(None, str(e))
    return render(request, "cours_form.html", {"form": form, "title": "Ajouter un cours"})

def cours_update(request, pk):
    c = get_object_or_404(Cours, pk=pk)
    if request.method == "POST":
        form = CoursForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours modifié avec succès.")
            return redirect("liste_cours")
    else:
        form = CoursForm(instance=c)
    return render(request, "cours_form.html", {"form": form, "title": "Modifier un cours"})

def cours_delete(request, pk):
    c = get_object_or_404(Cours, pk=pk)
    if request.method == "POST":
        c.delete()
        return redirect("liste_cours")
    return render(request, "confirm_delete.html", {"object": c, "type": "cours"})

# -------------------- Classes --------------------

def liste_classes(request):
    items = Classe.objects.all()
    return render(request, "liste_classes.html", {"items": items})

def classe_create(request):
    if request.method == "POST":
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Classe créée avec succès.")
            return redirect("liste_classes")
    else:
        form = ClasseForm()
    return render(request, "classe_form.html", {"form": form, "title": "Ajouter une classe"})

def classe_update(request, pk):
    c = get_object_or_404(Classe, pk=pk)
    if request.method == "POST":
        form = ClasseForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return redirect("liste_classes")
    else:
        form = ClasseForm(instance=c)
    return render(request, "classe_form.html", {"form": form, "title": "Modifier une classe"})

def classe_delete(request, pk):
    c = get_object_or_404(Classe, pk=pk)
    if request.method == "POST":
        c.delete()
        return redirect("liste_classes")
    return render(request, "confirm_delete.html", {"object": c, "type": "classe"})

# -------------------- Inscriptions (étudiant -> classe) --------------------

def liste_inscriptions(request):
    items = Inscription.objects.select_related("etudiant__user", "classe").all()
    return render(request, "liste_inscriptions.html", {"items": items})

def inscription_create(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription créée avec succès.")
            return redirect("liste_inscriptions")
    else:
        form = InscriptionForm()
    return render(request, "inscription_form.html", {"form": form, "title": "Ajouter une inscription"})

def inscription_delete(request, pk):
    i = get_object_or_404(Inscription, pk=pk)
    if request.method == "POST":
        i.delete()
        return redirect("liste_inscriptions")
    return render(request, "confirm_delete.html", {"object": i, "type": "inscription"})

# -------------------- Semestres --------------------

def liste_semestres(request):
    items = Semestre.objects.all()
    return render(request, "liste_semestres.html", {"items": items})

def semestre_create(request):
    if request.method == "POST":
        form = SemestreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Semestre créé avec succès.")
            return redirect("liste_semestres")
    else:
        form = SemestreForm()
    return render(request, "semestre_form.html", {"form": form, "title": "Ajouter un semestre"})

def semestre_update(request, pk):
    s = get_object_or_404(Semestre, pk=pk)
    if request.method == "POST":
        form = SemestreForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect("liste_semestres")
    else:
        form = SemestreForm(instance=s)
    return render(request, "semestre_form.html", {"form": form, "title": "Modifier un semestre"})

def semestre_delete(request, pk):
    s = get_object_or_404(Semestre, pk=pk)
    if request.method == "POST":
        s.delete()
        return redirect("liste_semestres")
    return render(request, "confirm_delete.html", {"object": s, "type": "semestre"})

# -------------------- Parents --------------------

def liste_parents(request):
    items = Parent.objects.all()
    return render(request, "liste_parents.html", {"items": items})

def parent_create(request):
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parent créé avec succès.")
            return redirect("liste_parents")
    else:
        form = ParentForm()
    return render(request, "parent_form.html", {"form": form, "title": "Ajouter un parent"})

def parent_update(request, pk):
    p = get_object_or_404(Parent, pk=pk)
    if request.method == "POST":
        form = ParentForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect("liste_parents")
    else:
        form = ParentForm(instance=p)
    return render(request, "parent_form.html", {"form": form, "title": "Modifier un parent"})

def parent_delete(request, pk):
    p = get_object_or_404(Parent, pk=pk)
    if request.method == "POST":
        p.delete()
        return redirect("liste_parents")
    return render(request, "confirm_delete.html", {"object": p, "type": "parent"})

# -------------------- Séances --------------------

def liste_seances(request):
    items = Seance.objects.select_related("classe", "cours", "enseignant__user").all()
    return render(request, "liste_seances.html", {"items": items})

def seance_create(request):
    if request.method == "POST":
        form = SeanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Séance créée avec succès.")
            return redirect("liste_seances")
    else:
        form = SeanceForm()
    return render(request, "seance_form.html", {"form": form, "title": "Ajouter une séance"})

def seance_update(request, pk):
    s = get_object_or_404(Seance, pk=pk)
    if request.method == "POST":
        form = SeanceForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect("liste_seances")
    else:
        form = SeanceForm(instance=s)
    return render(request, "seance_form.html", {"form": form, "title": "Modifier une séance"})

def seance_delete(request, pk):
    s = get_object_or_404(Seance, pk=pk)
    if request.method == "POST":
        s.delete()
        return redirect("liste_seances")
    return render(request, "confirm_delete.html", {"object": s, "type": "séance"})

# -------------------- Présences --------------------

def liste_presences(request):
    items = (
        Presence.objects
        .select_related("etudiant__user", "seance__classe", "seance__cours", "seance__enseignant__user")
        .all()
    )
    return render(request, "liste_presences.html", {"items": items})

def presence_create(request):
    if request.method == "POST":
        form = PresenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Présence enregistrée avec succès.")
            return redirect("liste_presences")
    else:
        form = PresenceForm()
    return render(request, "presence_form.html", {"form": form, "title": "Ajouter une présence"})

def presence_update(request, pk):
    p = get_object_or_404(Presence, pk=pk)
    if request.method == "POST":
        form = PresenceForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect("liste_presences")
    else:
        form = PresenceForm(instance=p)
    return render(request, "presence_form.html", {"form": form, "title": "Modifier une présence"})

def presence_delete(request, pk):
    p = get_object_or_404(Presence, pk=pk)
    if request.method == "POST":
        p.delete()
        return redirect("liste_presences")
    return render(request, "confirm_delete.html", {"object": p, "type": "présence"})

# -------------------- Activation compte & Scan QR (utilitaires) --------------------

def activate(request):
    token_str = request.GET.get("t")
    if not token_str:
        return HttpResponseBadRequest("Token manquant")
    tok = get_object_or_404(ActivationToken, token=token_str)
    if tok.used_at is not None or tok.expires_at < timezone.now():
        return HttpResponseForbidden("Token invalide ou expiré")
    tok.user.is_active = True
    tok.user.save(update_fields=["is_active"])
    tok.used_at = timezone.now()
    tok.save(update_fields=["used_at"])
    return HttpResponse("Compte activé, vous pouvez vous connecter.")

def scan_qr(request):
    if not request.user.is_authenticated or getattr(request.user, "role", None) != "etudiant":
        return HttpResponseForbidden("Authentification requise (étudiant).")

    token_str = request.GET.get("t")
    if not token_str:
        return HttpResponseBadRequest("Token manquant")

    qr = get_object_or_404(SeanceQR, token=token_str)
    if qr.expires_at < timezone.now():
        return HttpResponseForbidden("QR expiré")

    seance = qr.seance
    now = timezone.now()
    if not (seance.debut - timedelta(minutes=10) <= now <= seance.fin + timedelta(minutes=10)):
        return HttpResponseForbidden("Hors fenêtre")

    etu = getattr(request.user, "profil_etudiant", None)
    if not etu:
        return HttpResponseForbidden("Profil étudiant requis.")

    approved = Inscription.objects.filter(etudiant=etu, classe=seance.classe, statut="approved").exists()
    if not approved:
        return HttpResponseForbidden("Non inscrit à cette classe.")

    Presence.objects.get_or_create(etudiant=etu, seance=seance, defaults={"statut": "present"})
    return HttpResponse("Présence enregistrée.")

# -------------------- Tableau de bord --------------------
def admin_index(request):
    context = {
        "counts": {
            "utilisateurs": User.objects.count(),
            "administrateurs": User.objects.filter(role="admin").count() + User.objects.filter(is_staff=True).count(),
            "enseignants": Enseignant.objects.count(),
            "etudiants": Etudiant.objects.count(),
            "parents": Parent.objects.count(),
            "cours": Cours.objects.count(),
            "seances": Seance.objects.count(),
            "presences": Presence.objects.count(),
            "classes": Classe.objects.count(),
            "semestres": Semestre.objects.count(),
            "annees": AnneeScolaire.objects.count(),
            "inscriptions": Inscription.objects.count(),
        }
    }
    return render(request, "admin_index.html", context)




# --- Formulaires -----------------------------------------------------------------
class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"


class NiceAuthForm(AuthenticationForm):
    """Forme de connexion améliorée avec message explicite si compte inactif."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("Votre compte n'est pas encore activé. Veuillez vérifier votre email."),
                code="inactive"
            )


# --- Inscription -----------------------------------------------------------------
from .forms import SignupForm

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.is_active = False  # activation par email
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            # lien d’activation
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activate_url = request.build_absolute_uri(
                reverse("activate") + f"?uid={uid}&token={token}"
            )

            # envoi email (console backend => visible dans la console)
            subject = "Active ton compte"
            message = render_to_string(
                "emails/activation.txt",
                {"user": user, "activate_url": activate_url}
            )
            send_mail(subject, message, None, [user.email], fail_silently=True)

            return redirect("signup_done")
        # sinon: laisser retomber pour ré-afficher le formulaire avec erreurs (200)
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


def signup_done(request):
    return render(request, "registration/signup_done.html")


def activate(request):
    uid = request.GET.get("uid")
    token = request.GET.get("token")
    if not uid or not token:
        messages.error(request, "Lien d’activation invalide.")
        return redirect("signup")

    try:
        uid_int = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid_int)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Compte activé, bienvenue !")
        login(request, user)
        return redirect("admin_index")  # ou "accueil"
    else:
        messages.error(request, "Lien d’activation invalide ou expiré.")
        return redirect("signup")

def resend_activation(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").lower().strip()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, "Aucun compte avec cet email.")
            return redirect("resend_activation")

        if user.is_active:
            messages.info(request, "Ce compte est déjà activé.")
            return redirect("login")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activate_url = request.build_absolute_uri(
            reverse("activate") + f"?uid={uid}&token={token}"
        )
        subject = "Nouveau lien d’activation"
        message = render_to_string("emails/activation.txt", {"user": user, "activate_url": activate_url})
        send_mail(subject, message, None, [user.email], fail_silently=True)

        messages.success(request, "Lien d’activation renvoyé. Vérifie la console email.")
        return redirect("signup_done")

    return render(request, "resend_activation.html")


# --- Renvoyer l’activation -------------------------------------------------------
def resend_activation(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Veuillez entrer une adresse e-mail.")
            return redirect("resend_activation")

        users = User.objects.filter(email=email, is_active=False)
        if not users.exists():
            messages.error(request, "Aucun compte inactif trouvé avec cet email.")
            return redirect("resend_activation")

        # Si plusieurs comptes (cas de test), on prend le dernier créé
        user = users.order_by("-date_joined").first()

        token = ActivationToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=48)
        )

        activation_url = request.build_absolute_uri(
            reverse("activate") + f"?t={token.token}"
        )

        send_mail(
            subject="Nouveau lien d’activation — Présences",
            message=f"Bonjour {user.first_name or user.username},\n\n"
                    f"Voici votre nouveau lien d’activation : {activation_url}\n\n"
                    "Ce lien expire dans 48 heures.",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True,
        )

        messages.success(request, "Un nouveau lien d’activation a été envoyé.")
        return redirect("signup_done")

    return render(request, "registration/resend_activation.html")


def accueil(request):
    """
    Accueil conforme au rôle.
    - admin (ou staff): redirigé vers le dashboard admin_index
    - enseignant: accueil enseignant avec prochaines séances + raccourcis
    - etudiant: accueil étudiant avec prochaines séances de sa classe + compteur de présence
    - parent: accueil parent avec résumé des présences des enfants
    - invité: landing publique
    """
    # Invité → page publique
    if not request.user.is_authenticated:
        return render(request, "presence/accueil.html", {
            "role": "guest",
        })

    user = request.user
    role = getattr(user, "role", "") or ""

    # Admin/staff → dashboard existant
    if user.is_staff or role == "admin":
        return redirect("admin_index")

    ctx = {"role": role}

    now = timezone.now()
    today_start = timezone.localtime(now).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # ENSEIGNANT
    if role == "enseignant":
        # L'objet Enseignant relié à l'utilisateur
        try:
            ens = Enseignant.objects.select_related("user").get(user=user)
        except Enseignant.DoesNotExist:
            ens = None

        prochaines_seances = (
            Seance.objects
            .select_related("classe", "cours")
            .filter(enseignant=ens, debut__gte=now)
            .order_by("debut")[:6]
        )

        # Compteurs rapides (peuvent servir pour KPI)
        total_cours = Cours.objects.filter(enseignants=ens).count() if ens else 0
        seances_aujourdhui = Seance.objects.filter(enseignant=ens, debut__gte=today_start, debut__lt=today_end).count() if ens else 0

        ctx.update({
            "prochaines_seances": prochaines_seances,
            "kpi": {
                "total_cours": total_cours,
                "seances_aujourdhui": seances_aujourdhui,
            }
        })
        return render(request, "presence/accueil.html", ctx)

    # ETUDIANT
    if role == "etudiant":
        try:
            etu = Etudiant.objects.select_related("user").get(user=user)
        except Etudiant.DoesNotExist:
            etu = None

        # Classes où l’étudiant est "approved"
        classes_ids = list(
            Inscription.objects
            .filter(etudiant=etu, statut="approved")
            .values_list("classe_id", flat=True)
        ) if etu else []

        # Prochaines séances des classes de l’étudiant
        prochaines_seances = (
            Seance.objects
            .select_related("classe", "cours", "enseignant__user")
            .filter(classe_id__in=classes_ids, debut__gte=now)
            .order_by("debut")[:6]
        ) if classes_ids else []

        # Stats simples de présence
        total_seances = Seance.objects.filter(classe_id__in=classes_ids, debut__lt=now).count() if classes_ids else 0
        total_presences = Presence.objects.filter(etudiant=etu, statut="present").count() if etu else 0
        taux_presence = 0
        if total_seances > 0:
            taux_presence = round((total_presences / total_seances) * 100)

        ctx.update({
            "prochaines_seances": prochaines_seances,
            "kpi": {
                "total_seances": total_seances,
                "total_presences": total_presences,
                "taux_presence": taux_presence,
            }
        })
        return render(request, "presence/accueil.html", ctx)

    # PARENT
    if role == "parent":
        try:
            parent = Parent.objects.select_related("user").get(user=user)
        except Parent.DoesNotExist:
            parent = None

        # Supposons que Parent a une relation M2M vers Etudiant (à adapter si besoin)
        enfants = []
        if parent and hasattr(parent, "enfants"):
            enfants = list(parent.enfants.select_related("user").all())

        # Résumé présences par enfant (présent / total)
        enfants_stats = []
        for e in enfants:
            total_pres = Presence.objects.filter(etudiant=e).count()
            presents = Presence.objects.filter(etudiant=e, statut="present").count()
            taux = round((presents / total_pres) * 100) if total_pres else 0
            enfants_stats.append({
                "etudiant": e,
                "presents": presents,
                "total": total_pres,
                "taux": taux,
            })

        ctx.update({
            "enfants": enfants,
            "enfants_stats": enfants_stats,
        })
        return render(request, "presence/accueil.html", ctx)

    # Rôle inconnu → page générique authentifiée
    return render(request, "presence/accueil.html", {"role": "user"})

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

def _is_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, "role", "") == "admin")

def _is_teacher(user):
    return user.is_authenticated and (getattr(user, "role", "") == "enseignant")

def _is_student(user):
    return user.is_authenticated and (getattr(user, "role", "") == "etudiant")

@login_required
def qr_scanner(request):
    """
    Page qui ouvre la caméra et lit un QR.
    - Rôle autorisé : 'etudiant' par défaut. 
      (Tu peux aussi autoriser enseignants/admins si tu veux leur permettre de tester.)
    """
    role = getattr(request.user, "role", "") or ""
    if not (_is_student(request.user) or _is_teacher(request.user) or _is_admin(request.user)):
        return HttpResponseForbidden("Rôle non autorisé pour scanner.")

    # Info utile au template (pour afficher des conseils HTTPS, etc.)
    ctx = {
        "role": role,
    }
    return render(request, "presence/scanner.html", ctx)


# --- Admin: gestion des utilisateurs (liste, création, changement de rôle) ----
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import AdminUserCreateForm, UserRoleForm
from .models import User, Etudiant, Enseignant, Parent

def is_admin(user):
    return user.is_authenticated and (user.is_staff or getattr(user, "role", "") == "admin")

def ensure_profile_for_role(user):
    """
    Crée le profil lié selon le rôle si manquant.
    - etudiant  -> Etudiant(user=user)
    - enseignant-> Enseignant(user=user)
    - parent    -> Parent(user=user)
    """
    role = getattr(user, "role", "")
    try:
        if role == "etudiant":
            Etudiant.objects.get_or_create(user=user)
        elif role == "enseignant":
            Enseignant.objects.get_or_create(user=user)
        elif role == "parent":
            Parent.objects.get_or_create(user=user)
        # pour 'admin' rien à créer
    except Exception:
        # on n'explose pas l'action; on peut logger si besoin
        pass

@login_required
@user_passes_test(is_admin)
def admin_user_list(request):
    """
    Liste des utilisateurs avec filtre rapide par rôle et recherche.
    """
    qs = User.objects.all().order_by("-date_joined")
    role = request.GET.get("role") or ""
    q = request.GET.get("q") or ""
    if role:
        qs = qs.filter(role=role)
    if q:
        qs = qs.filter(username__icontains=q) | qs.filter(first_name__icontains=q) | qs.filter(last_name__icontains=q) | qs.filter(email__icontains=q)

    return render(request, "users/user_list.html", {
        "users": qs[:200],  # limite affichage
        "role": role, "q": q
    })

@login_required
@user_passes_test(is_admin)
@transaction.atomic
def admin_user_create(request):
    """
    Création d'un utilisateur avec rôle. 
    L'admin peut choisir 'is_active' (activer le compte immédiatement).
    """
    if request.method == "POST":
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Le formulaires inclut déjà 'role' et 'is_active'
            user.role = form.cleaned_data["role"]
            user.is_active = form.cleaned_data["is_active"]
            user.save()
            ensure_profile_for_role(user)
            messages.success(request, f"Utilisateur {user.username} créé avec rôle « {user.role} ».")
            return redirect("admin_user_list")
    else:
        form = AdminUserCreateForm()

    return render(request, "users/user_form.html", {"form": form, "title": "Créer un utilisateur"})

@login_required
@user_passes_test(is_admin)
@transaction.atomic
def admin_user_update_role(request, pk):
    """
    Modifier le rôle (et l'état actif) d'un utilisateur existant.
    """
    u = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserRoleForm(request.POST, instance=u)
        if form.is_valid():
            user = form.save()
            ensure_profile_for_role(user)
            messages.success(request, f"Rôle de {user.username} mis à jour en « {user.role} ».")            
            return redirect("admin_user_list")
    else:
        form = UserRoleForm(instance=u)

    return render(request, "users/user_role_form.html", {
        "form": form, "title": f"Rôle de {u.username}", "user_obj": u
    })

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Etudiant, Inscription
from .forms import AssignClasseForm


def _etudiant_display_name(etu: Etudiant) -> str:
    """
    Renvoie un nom d'affichage robuste pour un étudiant,
    même s'il n'a pas de user lié.
    """
    # Si un compte utilisateur est lié
    if getattr(etu, "user_id", None):
        full = (etu.user.get_full_name() or "").strip()
        if full:
            return full
        if getattr(etu.user, "username", None):
            return etu.user.username

    # Sinon : essaye nom/prenom, puis matricule, puis fallback
    nom = (getattr(etu, "nom", "") or "").strip()
    prenom = (getattr(etu, "prenom", "") or "").strip()
    if nom or prenom:
        return (nom + " " + prenom).strip()

    matricule = getattr(etu, "matricule", None)
    if matricule:
        return str(matricule)

    return f"Étudiant #{etu.pk}"


@login_required
def etudiant_assign_class(request, pk):
    etu = get_object_or_404(Etudiant, pk=pk)
    display_name = _etudiant_display_name(etu)

    if request.method == "POST":
        form = AssignClasseForm(request.POST)
        if form.is_valid():
            classe = form.cleaned_data["classe"]
            statut = form.cleaned_data["statut"]

            # Si tu stockes aussi la classe sur le profil étudiant
            if hasattr(etu, "classe"):
                etu.classe = classe
                etu.save(update_fields=["classe"])

            insc, created = Inscription.objects.update_or_create(
                etudiant=etu,
                classe=classe,
                defaults={"statut": statut},
            )

            # 🔒 Utilise toujours display_name (ne JAMAIS appeler etu.user.*
            # sans vérifier qu'il existe)
            if created:
                messages.success(request, f"{display_name} assigné(e) à {classe} ({statut}).")
            else:
                messages.success(request, f"Inscription mise à jour pour {display_name} → {classe} ({statut}).")

            # (optionnel) redirige vers la liste
            return redirect("liste_etudiants")
    else:
        form = AssignClasseForm()

    return render(
        request,
        "etudiant_assign_class.html",
        {
            "form": form,
            "etudiant": etu,
            "display_name": display_name,  # Le template peut l'utiliser
        },
    )



# 3.2) Page QR d'une séance (affiche l'image + lien, régénère si expiré)
@login_required
def seance_qr_page(request, pk):
    s = get_object_or_404(Seance, pk=pk)
    # On (re)génère un token s'il n'y en a pas/plus
    qr, created = SeanceQR.objects.get_or_create(
        seance=s,
        defaults={"expires_at": timezone.now() + timedelta(minutes=15)}
    )
    if qr.expires_at < timezone.now():
        qr.token = uuid4()
        qr.expires_at = timezone.now() + timedelta(minutes=15)
        qr.save(update_fields=["token", "expires_at"])

    scan_url = request.build_absolute_uri(
        reverse("scan_qr") + f"?t={qr.token}"
    )
    return render(request, "seance_qr.html", {"seance": s, "qr": qr, "scan_url": scan_url})


# 3.3) Image PNG du QR (utilisé par la page ci-dessus)
@require_GET
@login_required
def seance_qr_png(request, pk):
    s = get_object_or_404(Seance, pk=pk)
    qr = SeanceQR.objects.filter(seance=s).order_by("-id").first()
    if not qr or qr.expires_at < timezone.now():
        qr = SeanceQR.objects.create(
            seance=s,
            expires_at=timezone.now() + timedelta(minutes=15),
            token=uuid4()
        )
    scan_url = request.build_absolute_uri(
        reverse("scan_qr") + f"?t={qr.token}"
    )
    img = qrcode.make(scan_url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return HttpResponse(buf.getvalue(), content_type="image/png")



@login_required
def etudiant_assign_class(request, pk):
    """
    Assigne un étudiant à une classe via une Inscription (statut configurable).
    - Si une inscription existe déjà pour (etudiant, classe), on la met à jour.
    - Sinon, on la crée. (tes signaux feront le reste: EtudiantCours, Présences futures, etc.)
    """
    etu = get_object_or_404(Etudiant, pk=pk)

    if request.method == "POST":
        form = AssignClasseForm(request.POST)
        if form.is_valid():
            classe = form.cleaned_data["classe"]
            statut = form.cleaned_data["statut"]

            insc, created = Inscription.objects.update_or_create(
                etudiant=etu,
                classe=classe,
                defaults={"statut": statut}
            )

            if created:
                messages.success(request, f"{etu.user.get_full_name() or etu.user.username} assigné(e) à {classe} ({statut}).")
            else:
                messages.success(request, f"Inscription mise à jour pour {etu.user.get_full_name() or etu.user.username} → {classe} ({statut}).")

            return redirect("liste_etudiants")
    else:
        form = AssignClasseForm()

    return render(request, "etudiant_assign_class.html", {"form": form, "etudiant": etu})