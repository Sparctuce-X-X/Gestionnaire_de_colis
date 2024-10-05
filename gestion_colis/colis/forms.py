from django import forms
from .models import Colis, Employe, Client  # Importation des modèles nécessaires
from django.utils import timezone
# Formulaire pour modifier le statut d'un colis
class StatutColisForm(forms.ModelForm):
    class Meta:
        model = Colis
        fields = ['statut']
        labels = {
            'statut': 'Nouveau statut',
        }
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulaire pour le modèle Employe
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['user', 'role', 'date_recrutement']
        labels = {
            'user': 'Nom d’utilisateur',
            'role': 'Rôle',
            'date_recrutement': 'Date de recrutement',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'date_recrutement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Formulaire pour le modèle Colis
class ColisForm(forms.ModelForm):
    class Meta:
        model = Colis
        fields = ['reference', 'description', 'poids', 'origine', 'destination', 'statut', 'entrepot', 'date_envoi', 'expediteur', 'recepteur']
        labels = {
            'reference': 'Référence',
            'description': 'Description',
            'poids': 'Poids (kg)',
            'origine': 'Lieu d\'origine',
            'destination': 'Lieu de destination',
            'statut': 'Statut actuel',
            'entrepot': 'Entrepôt associé',
            'date_envoi': 'Date d\'envoi',
            'expediteur': 'Expéditeur',
            'recepteur': 'Récepteur',
        }
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'poids': forms.NumberInput(attrs={'class': 'form-control'}),
            'origine': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'entrepot': forms.Select(attrs={'class': 'form-control'}),
            'date_envoi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expediteur': forms.Select(attrs={'class': 'form-control'}),
            'recepteur': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulaire pour le modèle Client
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone', 'adresse']
        labels = {
            'nom': 'Nom complet',
            'email': 'Adresse e-mail',
            'telephone': 'Numéro de téléphone',
            'adresse': 'Adresse postale',
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }



class WeekSelectionForm(forms.Form):
    start_date = forms.DateField(
        label='Choisissez une date de début',
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )