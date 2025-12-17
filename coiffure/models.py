from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

import uuid
import os

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('employe', 'Employé'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employe')

    def __str__(self):
        return self.username

# =============================
# SALON
# =============================

def salon_image_path(instance, filename):
    """Renomme les images avec un UUID unique pour éviter les conflits"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('salons/', filename)

class Salon(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    horaire_ouverture = models.TimeField()
    horaire_fermeture = models.TimeField()
    date_creation = models.DateField()
    actif = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="salons/", blank=True, null=True)
    def __str__(self):
        return self.nom
    
# =============================
# CLIENT
# =============================

class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_inscription = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=20, default="actif")  # actif / inactif
    actif = models.BooleanField(default=True)  # ← AJOUT
    def __str__(self):
        return f"{self.nom} {self.prenom}"

# =============================
# EMPLOYÉ
# =============================


class Employe(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField(blank=True, null=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="employes")
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# =============================
# SERVICE
# =============================


class Service(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duree = models.DurationField(help_text="Durée estimée (hh:mm:ss)")
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.libelle

# =============================
# PRESTATION
# =============================

class Prestation(models.Model):
    # Statuts possibles
    STATUT_CHOICES = [
        ("planifié", "Planifié"),
        ("effectué", "Effectué"),
        ("annulé", "Annulé"),
    ]
    
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    employe = models.ForeignKey('Employe', on_delete=models.SET_NULL, null=True, blank=True)
    date_prestation = models.DateField()
    heure_prestation = models.TimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="planifié")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['date_prestation', 'heure_prestation']
        verbose_name = "Prestation"
        verbose_name_plural = "Prestations"

    def __str__(self):
        return f"{self.client} - {self.service} ({self.date_prestation} {self.heure_prestation})"

    def clean(self):
        # Empêche de planifier une prestation dans le passé
        if self.date_prestation < timezone.now().date():
            raise ValidationError("La date de prestation ne peut pas être dans le passé.")

        # Optionnel : vérifier que l'heure n'est pas passée si c'est aujourd'hui
        if self.date_prestation == timezone.now().date() and self.heure_prestation < timezone.now().time():
            raise ValidationError("L'heure de la prestation ne peut pas être dans le passé.")

    def save(self, *args, **kwargs):
        self.full_clean()  # applique la validation avant d'enregistrer
        super().save(*args, **kwargs)

# =============================
# PRODUIT
# =============================

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nom

# =============================
# RENDEZ-VOUS
# =============================


class RendezVous(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_rdv = models.DateField()
    heure = models.TimeField()
    statut = models.CharField(max_length=20, default="en attente")  # confirmé / en attente / annulé

    def __str__(self):
        return f"{self.client} - {self.service} - {self.date_rdv}"

# =============================
# PAIEMENT
# =============================
class Paiement(models.Model):
    numero_facture = models.CharField(max_length=50, unique=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en attente', 'En attente'),
        ('payé', 'Payé')
    ], default='en attente')

    mode_paiement = models.CharField(max_length=50, choices=(
        ('espèces', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('mobile', 'Paiement mobile')
    ), default='espèces')

    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.numero_facture:
            # Génère un numéro unique aléatoire, par ex. UUID ou incrément
            self.numero_facture = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.numero_facture} - {self.montant} XOF"
    

    from django.db import models

class ModeleCoiffure(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du modèle")
    description = models.TextField(blank=True, verbose_name="Description")
    prix = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Prix")
    duree = models.IntegerField(verbose_name="Durée (minutes)")
    photo = models.ImageField(upload_to='modeles/', blank=True, null=True, verbose_name="Photo du modèle")

    def __str__(self):
        return self.nom



 # =============================
# NOTIFICATION
# =============================
from django.db import models
from django.conf import settings  # ⚡ Nécessaire !

class Notification(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coiffure_notifications"  # ⚡ change pour éviter conflit
    )
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
