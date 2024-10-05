from django.urls import path
from . import views

# Configuration des URLs du projet `colis`
urlpatterns = [
    # Routes pour la gestion des colis
    path('liste/', views.liste_colis, name='liste_colis'),  # Liste des colis
    path('ajouter/', views.ajouter_colis, name='ajouter'),  # Ajouter un nouveau colis
    path('modifier/<str:reference>/', views.modifier_colis, name='modifier_colis'),  # Modifier un colis
    path('details/<str:reference>/', views.details_colis, name='details_colis'),  # Détails d'un colis
    path('modifier_statut/<str:reference>/', views.modifier_statut_colis, name='modifier_statut_colis'),  # Mettre à jour le statut d'un colis

    # Routes pour la gestion des employés
    path('liste_employes/', views.liste_employes, name='liste_employes'),  # Liste des employés
    path('ajouter_employe/', views.ajouter_employe, name='ajouter_employe'),  # Ajouter un employé
    path('modifier_employe/<int:id>/', views.modifier_employe, name='modifier_employe'),  # Modifier un employé
    path('supprimer_employe/<int:id>/', views.supprimer_employe, name='supprimer_employe'),  # Supprimer un employé
    path('details_employe/<int:id>/', views.details_employe, name='details_employe'),  # Détails d'un employé

    # Routes pour la gestion des clients
    path('liste_clients/', views.liste_clients, name='liste_clients'),  # Liste des clients
    path('ajouter_client/', views.ajouter_client, name='ajouter_client'),  # Ajouter un client
    path('modifier_client/<int:id>/', views.modifier_client, name='modifier_client'),  # Modifier un client
    path('supprimer_client/<int:id>/', views.supprimer_client, name='supprimer_client'),  # Supprimer un client
    path('details_client/<int:id>/', views.details_client, name='details_client'),  # Détails d'un client

    # Route pour le tableau de bord
    path('tableau_bord/', views.tableau_bord, name='tableau_bord'),  # Tableau de bord des entrepôts

    path('facture/<int:colis_id>/', views.generer_facture, name='generer_facture'),
]

# Gestion des erreurs personnalisées
handler404 = 'colis.views.custom_404'  # Gestionnaire pour les erreurs 404
