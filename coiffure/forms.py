from django import forms
from .models import Client, Employe, Service, Produit, Paiement, RendezVous, Salon, Prestation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# === CLIENT FORM ===
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom','prenom','telephone','email','statut']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

# === EMPLOYE FORM ===
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom','prenom','telephone','date_naissance','service','salon']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'service': forms.Select(attrs={'class':'form-select'}),
            'salon': forms.Select(attrs={'class':'form-select'}),
        }

# === SALON FORM ===


class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = [
            'nom', 'adresse', 'telephone', 'email',
            'horaire_ouverture', 'horaire_fermeture',
            'date_creation', 'actif', 'description', 'image'
        ]

        widgets = {
            'horaire_ouverture': forms.TimeInput(attrs={'type': 'time'}),
            'horaire_fermeture': forms.TimeInput(attrs={'type': 'time'}),
            'date_creation': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PrestationForm(forms.ModelForm):
    montant = forms.DecimalField(
        label="Montant",
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'id':'id_montant'})
    )

    class Meta:
        model = Prestation
        fields = ['client', 'service', 'employe', 'date_prestation', 'heure_prestation', 'statut', 'commentaire', 'montant']
        widgets = {
            'client': forms.Select(attrs={'class':'form-select'}),
            'service': forms.Select(attrs={'class':'form-select', 'id':'id_service'}),
            'employe': forms.Select(attrs={'class':'form-select'}),
            'date_prestation': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'heure_prestation': forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
            'statut': forms.Select(attrs={'class':'form-select'}),
            'commentaire': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

        }


# === SERVICE FORM ===
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['libelle', 'description', 'duree', 'prix']
        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duree': forms.TimeInput(attrs={'class': 'form-control', 'type':'time'}),
            'prix': forms.NumberInput(attrs={'class':'form-control', 'step':'100','min':'0'}),
        }

# === PRODUIT FORM ===
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix_unitaire', 'stock']
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'prix_unitaire': forms.NumberInput(attrs={'class':'form-control','step':'100','min':'0'}),
            'stock': forms.NumberInput(attrs={'class':'form-control','min':'0'}),
        }

# === RENDEZ-VOUS FORM ===
class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['client', 'service', 'date_rdv', 'heure', 'statut']
        widgets = {
            'client': forms.Select(attrs={'class':'form-select'}),
            'service': forms.Select(attrs={'class':'form-select'}),
            'date_rdv': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'heure': forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
            'statut': forms.Select(attrs={'class':'form-select'}),
        }

# === PAIEMENT FORM ===
class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['prestation', 'client', 'montant', 'statut']
        widgets = {
            'prestation': forms.Select(attrs={'class':'form-select'}),
            'client': forms.Select(attrs={'class':'form-select'}),
            'montant': forms.NumberInput(attrs={'class':'form-control','step':'100','min':'0'}),
            'statut': forms.Select(attrs={'class':'form-select'}),
        }



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Ajouter les classes Bootstrap automatiquement
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

from django import forms
from .models import ModeleCoiffure

class ModeleCoiffureForm(forms.ModelForm):
    class Meta:
        model = ModeleCoiffure
        fields = ['nom', 'description', 'prix', 'duree', 'photo']
