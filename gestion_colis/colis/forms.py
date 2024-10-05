from django import forms
from .models import Colis, Employe, Client  # Importation des modèles nécessaires
from django.utils import timezone
from .models import Entrepot, Colis, Employe, Client

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
    expediteur = forms.ModelChoiceField(queryset=Client.objects.all(), label="Expéditeur")
    recepteur = forms.ModelChoiceField(queryset=Client.objects.all(), label="Récepteur")

    class Meta:
        model = Colis
        fields = ['reference', 'description', 'poids', 'origine', 'destination', 'statut', 'expediteur', 'recepteur']


    def __init__(self, *args, **kwargs):
        super(ColisForm, self).__init__(*args, **kwargs)
        # Remplir les choix des champs d'origine et de destination avec les entrepôts
        self.fields['origine'].queryset = Entrepot.objects.all()
        self.fields['destination'].queryset = Entrepot.objects.all()

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