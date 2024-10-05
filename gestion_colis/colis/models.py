from django.db import models
from django.contrib.auth.models import User

# Modèle pour les Entrepôts
class Entrepot(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nom

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, unique=True)
    adresse = models.TextField()

    def __str__(self):
        return self.nom

    def nb_colis(self):
        return self.colis_envoyes.count()  # Compte le nombre de colis envoyés par le client

    def poids_total(self):
        return sum(colis.poids for colis in self.colis_envoyes.all())  # Somme des poids de tous les colis envoyés
# Modèle pour les Colis
class Colis(models.Model):
    STATUTS = [
        ('EN ATTENTE', 'En attente'),
        ('EN TRANSIT', 'En transit'),
        ('LIVRE', 'Livré'),
    ]

    reference = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    origine = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_envoi = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN ATTENTE')
    entrepot = models.ForeignKey(Entrepot, on_delete=models.SET_NULL, null=True, blank=True)
    expediteur = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='colis_envoyes', null=True, blank=True)
    recepteur = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='colis_recus', null=True, blank=True)
    entrepot = models.ForeignKey(Entrepot, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.reference

# Modèle pour les Employés
class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('ADMIN', 'Administrateur'), ('AGENT', 'Agent de Distribution')], default='AGENT')
    date_recrutement = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.role}"


