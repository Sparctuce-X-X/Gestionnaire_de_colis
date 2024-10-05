from django.contrib import admin
from .models import Entrepot, Colis, Employe, Client

# Personnalisation de l'affichage du modèle Client
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'adresse')
    search_fields = ('nom', 'email', 'telephone')
    list_filter = ('nom',)

# Personnalisation de l'affichage du modèle Colis
class ColisAdmin(admin.ModelAdmin):
    list_display = ('reference', 'origine', 'destination', 'poids', 'statut', 'entrepot', 'expediteur', 'recepteur')
    search_fields = ('reference', 'origine', 'destination', 'expediteur__nom', 'recepteur__nom')
    list_filter = ('statut', 'entrepot', 'expediteur', 'recepteur')
    list_editable = ('statut', 'entrepot')  # Permet de modifier directement le statut et l'entrepôt dans la liste

# Personnalisation de l'affichage du modèle Employe
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'date_recrutement')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

# Personnalisation de l'affichage du modèle Entrepot
class EntrepotAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse')
    search_fields = ('nom',)
    list_filter = ('nom',)

# Enregistrement des modèles dans l'administration
admin.site.register(Entrepot, EntrepotAdmin)
admin.site.register(Colis, ColisAdmin)
admin.site.register(Employe, EmployeAdmin)
admin.site.register(Client, ClientAdmin)
