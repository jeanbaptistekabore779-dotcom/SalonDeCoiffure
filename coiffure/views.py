# 1. Django Core & Shortcuts
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template

# 2. Authentification & Utilisateurs
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required # Important pour la gestion
User = get_user_model()

# 3. Vos Modèles
from .models import (
    Client, Produit, Employe, Service, RendezVous, 
    Salon, Prestation, Paiement, ModeleCoiffure
)
from notifications.models import Notification

# 4. Vos Formulaires
from .forms import (
    PrestationForm, ServiceForm, SalonForm, EmployeForm, 
    PaiementForm, ProduitForm, RendezVousForm, RegisterForm, 
    LoginForm, ModeleCoiffureForm
)

# 5. Utilitaires tiers (PDF, etc.)
from xhtml2pdf import pisa
from datetime import date

# =============================
# PAGE D'ACCUEIL
# =============================
@login_required
def home(request):
    # On initialise les variables pour éviter des erreurs dans le template
    user_role = None
    
    # Si l'utilisateur est connecté, on récupère son rôle lisible (ex: Administrateur)
    if request.user.is_authenticated:
        user_role = request.user.get_role_display()
    
    context = {
        'user_role': user_role,
    }
    return render(request, "coiffure/home.html", context)

def login_view(request):
    return render(request, "coiffure/login.html")

@login_required
def tablebord(request):

    total_clients = Client.objects.count()
    total_produits = Produit.objects.count()
    total_employes = Employe.objects.count()
    total_services = Service.objects.count()
    total_rdv = RendezVous.objects.filter(date_rdv=timezone.now().date()).count()
    total_paiements = Paiement.objects.aggregate(total=Sum("montant"))["total"] or 0

    produits_recents = Produit.objects.order_by('-date_ajout')[:5]
    rdv_prochains = RendezVous.objects.order_by('date_rdv', 'heure')[:10]

    # 🔔 Notifications de l’utilisateur connecté
    user_notifications = Notification.objects.filter(utilisateur=request.user)

    notifs_non_lues = user_notifications.filter(lu=False).count()
    notifications_recents = user_notifications.order_by('-date')[:5]

    context = {
        "clients": total_clients,
        "produits": total_produits,
        "employes": total_employes,
        "services": total_services,
        "rdv": total_rdv,
        "paiements": total_paiements,
        "produits_recents": produits_recents,
        "rdv_prochains": rdv_prochains,

        # notifications dashboard
        "notifications": notifications_recents,
        "notifs_non_lues": notifs_non_lues,
    }

    return render(request, "coiffure/tablebord.html", context)




# =============================
# CLIENTS – CRUD
# =============================

def liste_clients(request):
    clients = Client.objects.all().order_by("-id")
    return render(request, "coiffure/client/liste_clients.html", {"clients": clients})


def ajouter_client(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        date_inscription = request.POST.get("date_inscription")
        statut = request.POST.get("statut")

        # Vérifier si l'email existe déjà
        if Client.objects.filter(email=email).exists():
            messages.error(request, "Un client avec cet email existe déjà.")
            return redirect("ajouter_client")  # ✔️ CORRECTION

        else:
            Client.objects.create(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                date_inscription=date_inscription,
                statut=statut,
            )
            messages.success(request, "Client ajouté avec succès !")
            return redirect("liste_clients")

    return render(request, "coiffure/client/ajouter_client.html")


def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        client.nom = request.POST["nom"]
        client.prenom = request.POST["prenom"]
        client.telephone = request.POST["telephone"]
        client.email = request.POST["email"]
        client.save()
        messages.success(request, "Client modifié avec succès")
        return redirect("liste_clients")
    return render(request, "coiffure/client/modifier_client.html", {"client": client})


def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    messages.warning(request, "Client supprimé")
    return redirect("liste_clients")

# =============================
# PRODUITS – CRUD
# =============================

def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, "coiffure/produit/liste_produits.html", {"produits": produits})
# coiffure/views.py (Section PRODUITS – CRUD)

def ajouter_produit(request):
    if request.method == "POST":
        # Créez le formulaire en le liant aux données POST
        form = ProduitForm(request.POST)
        if form.is_valid():
            # Enregistrez les données si la validation est réussie
            form.save() 
            messages.success(request, "Produit ajouté avec succès")
            return redirect("liste_produits")
        # Si le formulaire n'est pas valide, le code continue pour afficher le formulaire avec les erreurs
    else:
        # Pour le GET (affichage initial), créez un formulaire vide
        form = ProduitForm() 
        
    # Passez l'objet 'form' au template
    return render(request, "coiffure/produit/ajouter_produit.html", {"form": form})

def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == "POST":
        produit.nom = request.POST["nom"]
        produit.description = request.POST["description"]
        produit.prix_unitaire = request.POST["prix_unitaire"]
        produit.stock = request.POST["stock"]
        produit.save()
        messages.success(request, "Produit modifié avec succès")
        return redirect("liste_produits")
    return render(request, "coiffure/produit/modifier_produit.html", {"produit": produit})

def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    produit.delete()
    messages.warning(request, "Produit supprimé")
    return redirect("liste_produits")

# =============================
# EMPLOYÉS – CRUD
# =============================

def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, "coiffure/employe/liste_employes.html", {"employes": employes})

def ajouter_employe(request):
    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employé ajouté")
            return redirect("liste_employes")
    else:
        form = EmployeForm()
    return render(request, "coiffure/employe/ajouter_employe.html", {"form": form})

def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == "POST":
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            messages.success(request, "Employé modifié")
            return redirect("liste_employes")
    else:
        form = EmployeForm(instance=employe)
    return render(request, "coiffure/employe/modifier_employe.html", {"form": form})

def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    employe.delete()
    messages.warning(request, "Employé supprimé")
    return redirect("liste_employes")

# =============================
# SERVICES – CRUD
# =============================

def liste_services(request):
    services = Service.objects.all()
    return render(request, "coiffure/service/liste_services.html", {"services": services})

def ajouter_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service ajouté avec succès !")
            return redirect('liste_services')
    else:
        form = ServiceForm()
    return render(request, 'coiffure/service/ajouter_service.html', {'form': form})

def modifier_service(request, id):

    # Récupère le service à modifier
    service = get_object_or_404(Service, id=id)

    if request.method == "POST":
        # Pré-remplir le formulaire avec l'instance existante + données POST
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service modifié avec succès !")
            return redirect("liste_services")
    else:
        # GET : formulaire pré-rempli avec les valeurs existantes
        form = ServiceForm(instance=service)

    return render(request, "coiffure/service/modifier_service.html", {"form": form})
def supprimer_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.warning(request, "Service supprimé")
    return redirect("liste_services")

# =============================
# RENDEZ-VOUS – CRUD
# =============================


def liste_rdv(request):
    rdvs = RendezVous.objects.all()
    return render(request, "coiffure/rdv/liste_rdv.html", {"rdvs": rdvs})

@login_required
def ajouter_rdv(request):
    clients = Client.objects.all()
    services = Service.objects.all()

    if request.method == "POST":
        rdv = RendezVous.objects.create(
            client_id=request.POST["client"],
            service_id=request.POST["service"],
            date_rdv=request.POST["date_rdv"],
            heure=request.POST["heure"],
            statut=request.POST["statut"]
        )

        # ✅ Notification correcte
        Notification.objects.create(
            utilisateur=request.user,
            message=f"Nouveau rendez-vous : {rdv.client.nom} pour le service {rdv.service.libelle} le {rdv.date_rdv} à {rdv.heure}",
            lu=False
        )

        messages.success(request, "Rendez-vous ajouté et notification créée.")
        return redirect("liste_rdv")

    return render(request, "coiffure/rdv/ajouter_rdv.html", {
        "clients": clients,
        "services": services
    })

@login_required
def modifier_rdv(request, id):
    rdv = get_object_or_404(RendezVous, id=id)
    clients = Client.objects.all()
    services = Service.objects.all()

    if request.method == "POST":
        rdv.client_id = request.POST["client"]
        rdv.service_id = request.POST["service"]
        rdv.date_rdv = request.POST["date_rdv"]
        rdv.heure = request.POST["heure"]
        rdv.statut = request.POST["statut"]
        rdv.save()

        # ✅ Notification modification
        Notification.objects.create(
            utilisateur=request.user,
            message=f"Rendez-vous modifié : {rdv.client.nom} pour {rdv.service.libelle}",
            lu=False
        )

        messages.success(request, "Rendez-vous modifié avec succès")
        return redirect("liste_rdv")

    return render(request, "coiffure/rdv/modifier_rdv.html", {
        "rdv": rdv,
        "clients": clients,
        "services": services
    })

@login_required
def supprimer_rdv(request, id):
    rdv = get_object_or_404(RendezVous, id=id)
    rdv.delete()

    Notification.objects.create(
        utilisateur=request.user,
        message="Un rendez-vous a été supprimé.",
        lu=False
    )

    messages.warning(request, "Rendez-vous supprimé")
    return redirect("liste_rdv")

# =============================
# SALON – CRUD
# =============================
def liste_salons(request):
    salons = Salon.objects.all()
    return render(request, 'coiffure/salon/liste_salons.html', {'salons': salons})

def ajouter_salon(request):
    if request.method == 'POST':
        form = SalonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_salons')
    else:
        form = SalonForm()
    return render(request, 'coiffure/salon/ajouter_salon.html', {'form': form})

def modifier_salon(request, id):
    salon = get_object_or_404(Salon, pk=id)
    
    if request.method == "POST":
        form = SalonForm(request.POST, request.FILES, instance=salon)
        if form.is_valid():
            form.save()
            return redirect('liste_salons')  # redirection vers la liste
        else:
            # Affiche les erreurs dans la console pour debug
            print(form.errors)
    else:
        form = SalonForm(instance=salon)

    return render(request, 'coiffure/salon/modifier_salon.html', {'form': form, 'salon': salon})

def supprimer_salon(request, id):
    salon = get_object_or_404(Salon, id=id)
    salon.delete()
    messages.warning(request, "Salon supprimé")
    return redirect("liste_salons")

# =============================
# PRESTATION – CRUD
# =============================

def liste_prestations(request):
    prestations = Prestation.objects.all()
    return render(request, 'coiffure/prestation/liste_prestations.html', {'prestations': prestations})

def ajouter_prestation(request):
    if request.method == 'POST':
        form = PrestationForm(request.POST)
        if form.is_valid():
            prestation = form.save(commit=False)
            # remplir le montant avec le prix du service sélectionné
            prestation.montant = prestation.service.prix
            prestation.save()
            messages.success(request, "Prestation ajoutée avec succès !")
            return redirect('liste_prestations')
    else:
        form = PrestationForm()
    return render(request, 'coiffure/prestation/ajouter_prestation.html', {'form': form})

def modifier_prestation(request, id):
    prestation = get_object_or_404(Prestation, id=id)
    if request.method == 'POST':
        form = PrestationForm(request.POST, instance=prestation)
        if form.is_valid():
            form.save()
            messages.success(request, "Prestation modifiée")
            return redirect('liste_prestations')
    else:
        form = PrestationForm(instance=prestation)
    return render(request, 'coiffure/prestation/modifier_prestation.html', {'form': form})

def supprimer_prestation(request, id):
    prestation = get_object_or_404(Prestation, id=id)
    prestation.delete()
    messages.warning(request, "Prestation supprimée")
    return redirect('liste_prestations')

# =============================
# PAIEMENT – CRUD
# =============================
def liste_paiements(request):
    paiements = Paiement.objects.all()
    return render(request, 'coiffure/paiement/liste_paiements.html', {'paiements': paiements})

def ajouter_paiement(request):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paiement ajouté")
            return redirect('liste_paiements')
    else:
        form = PaiementForm()
    return render(request, 'coiffure/paiement/ajouter_paiement.html', {'form': form})

def modifier_paiement(request, id):
    paiement = get_object_or_404(Paiement, id=id)
    if request.method == 'POST':
        form = PaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            form.save()
            messages.success(request, "Paiement modifié")
            return redirect('liste_paiements')
    else:
        form = PaiementForm(instance=paiement)
    return render(request, 'coiffure/paiement/modifier_paiement.html', {'form': form})

def supprimer_paiement(request, id):
    paiement = get_object_or_404(Paiement, id=id)
    paiement.delete()
    messages.warning(request, "Paiement supprimé")
    return redirect('liste_paiements')



# =============================
# PAIEMENT – Autres methodes
# =============================
def facture_pdf(request, paiement_id):
    paiement = Paiement.objects.get(id=paiement_id)

    template_path = 'coiffure/paiement/facture.html'
    template = get_template(template_path)
    html = template.render({'paiement': paiement})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="facture_{paiement_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la création PDF')
    return response

def detail_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)
    return render(request, 'coiffure/paiement/detail_paiement.html', {'paiement': paiement})

def historique_paiements(request):
    paiements = Paiement.objects.all()  # récupère tous les paiements
    return render(request, 'coiffure/paiement/liste_paiements.html', {'paiements': paiements})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "coiffure/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect("tablebord")  # Redirection après connexion
    else:
        form = LoginForm()

    return render(request, "coiffure/login.html", {"form": form})

def rapport_view(request):
    salons = Salon.objects.all()
    rapport_data = []

    for salon in salons:
        prestations = Prestation.objects.select_related('client', 'service').order_by('date_prestation')
        total = prestations.aggregate(total_sum=Sum('montant'))['total_sum'] or 0
        recettes_par_jour = prestations.values('date_prestation').annotate(total=Sum('montant')).order_by('date_prestation')

        labels = [p['date_prestation'].strftime("%d/%m") for p in recettes_par_jour]
        data = [float(p['total']) for p in recettes_par_jour]  # ⚡ convertir Decimal en float pour JSON

        rapport_data.append({
            'salon': salon,
            'prestations': prestations,
            'total': total,
            'labels': labels,
            'data': data,
        })

    return render(request, "rapport.html", {
        'rapport_data': rapport_data,
        'date': date.today(),
    })

def parametre_view(request):
    # Récupère tous les salons
    salons = Salon.objects.all()
    
    # Tu peux ajouter d'autres paramètres ici si besoin
    context = {'salons': salons}
    
    return render(request, 'parametre.html', context)

def liste_modeles(request):
    modeles = ModeleCoiffure.objects.all()
    return render(request, "coiffure/modele/liste_modeles.html", {"modeles": modeles})

def ajouter_modele(request):
    if request.method == "POST":
        form = ModeleCoiffureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_modeles')
        else:
            print("Erreurs :", form.errors)
    else:
        form = ModeleCoiffureForm()

    return render(request, "coiffure/modele/ajouter_modele.html", {"form": form})

def modifier_modele(request, id):
    modele = ModeleCoiffure.objects.get(id=id)

    if request.method == "POST":
        form = ModeleCoiffureForm(request.POST, request.FILES, instance=modele)
        if form.is_valid():
            form.save()
            return redirect('liste_modeles')
    else:
        form = ModeleCoiffureForm(instance=modele)

    return render(request, "coiffure/modele/modifier_modele.html", {"form": form})

def supprimer_modele(request, id):
    modele = ModeleCoiffure.objects.get(id=id)
    modele.delete()
    return redirect("liste_modeles")

# Prise de Rendez vous
def prendre_rendezvous(request):
    if request.method == "POST":
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save()

            # 🔔 Création automatique de notification
            Notification.objects.create(
                message=f"Nouveau rendez-vous pris par {rdv.nom_client}"
            )

            return redirect("confirmation_rdv")

    else:
        form = RendezVousForm()

    return render(request, "coiffure/rendezvous.html", {"form": form})

def deconnexion(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion


def quitter(request):
    """
    Page Quitter : affiche un message et propose de revenir à l'accueil.
    """
    return render(request, "quitter.html")


def contact(request):
    return render(request, 'coiffure/contact.html', {})

def detail_salon(request, id):
    salon = get_object_or_404(Salon, id=id)
    return render(request, "coiffure/salon/detail_salon.html", {"salon": salon})


@login_required
def lire_notification(request, notif_id):
    # Récupère la notification spécifique
    notif = get_object_or_404(Notification, id=notif_id, utilisateur=request.user)
    
    # Marque comme lue
    notif.lu = True
    notif.save()
    
    # Redirige où tu veux (ex: tableau de bord)
    return redirect('tablebord')


@login_required
def mark_as_read(request, notif_id):
    """
    Marque une notification comme lue et redirige vers le tableau de bord.
    """
    notif = get_object_or_404(Notification, id=notif_id, utilisateur=request.user)
    notif.lu = True
    notif.save()
    return redirect('tablebord')  # ou vers la page de ton choix

@login_required
@staff_member_required
def utilisateur_profil(request):
    # On réutilise la logique du tableau de bord ou on affiche le profil
    return render(request, 'coiffure/utilisateur.html', {
        'user': request.user
    })

    from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required # Seuls les admins peuvent accéder à cette page
def liste_utilisateurs(request):
    utilisateurs = User.objects.all().order_by('-date_joined')
    return render(request, "utilisateur/liste_utilisateurs.html", {
        "utilisateurs": utilisateurs
    })

@login_required
@staff_member_required
def supprimer_utilisateur(request, id):
    user_to_delete = get_object_or_404(User, id=id)
    if user_to_delete != request.user: # Empêcher de se supprimer soi-même
        user_to_delete.delete()
        messages.warning(request, "Utilisateur supprimé.")
    return redirect("utilisateur/liste_utilisateurs")