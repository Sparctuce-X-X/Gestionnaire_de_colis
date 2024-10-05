from django.shortcuts import render, get_object_or_404, redirect
from .models import Colis, Entrepot, Employe, Client
from .forms import ColisForm, EmployeForm, ClientForm, StatutColisForm
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .forms import WeekSelectionForm
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta 
from .utils import send_sms 
# -------------- Vues pour la gestion des Colis --------------

def liste_colis(request):
    query = request.GET.get('q', '')
    if query:
        colis_list = Colis.objects.filter(reference__icontains=query).select_related('expediteur', 'recepteur')
    else:
        colis_list = Colis.objects.all().select_related('expediteur', 'recepteur')

    paginator = Paginator(colis_list, 10)  # 10 colis par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'colis/liste.html', {'page_obj': page_obj, 'query': query})




def ajouter_colis(request):
    if request.method == 'POST':
        form = ColisForm(request.POST)
        if form.is_valid():
            colis = form.save()

            # Récupération de l'expéditeur
            expediteur = colis.expediteur
            expediteur_numero = expediteur.telephone  # Assurez-vous que c'est le bon champ

            # Envoi du SMS à l'expéditeur
            message_body = f'Votre colis {colis.reference} a été ajouté avec succès!'
            send_sms(expediteur_numero, message_body)

            return redirect('liste_colis')
    else:
        form = ColisForm()
    return render(request, 'colis/ajouter.html', {'form': form})


def modifier_colis(request, reference):
    colis = get_object_or_404(Colis, reference=reference)
    if request.method == 'POST':
        form = ColisForm(request.POST, instance=colis)
        if form.is_valid():
            form.save()
            return redirect('details_colis', reference=colis.reference)
    else:
        form = ColisForm(instance=colis)
    return render(request, 'colis/modifier.html', {'form': form, 'colis': colis})

def details_colis(request, reference):
    colis = get_object_or_404(Colis, reference=reference)
    return render(request, 'colis/details.html', {'colis': colis})

def modifier_statut_colis(request, reference):
    colis = get_object_or_404(Colis, reference=reference)
    if request.method == 'POST':
        form = StatutColisForm(request.POST, instance=colis)
        if form.is_valid():
            form.save()
            return redirect('details_colis', reference=colis.reference)
    else:
        form = StatutColisForm(instance=colis)
    return render(request, 'colis/modifier_statut.html', {'form': form, 'colis': colis})

# -------------- Vues pour la gestion des Employés --------------

def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'colis/liste_employes.html', {'employes': employes})

def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    return render(request, 'colis/ajouter_employe.html', {'form': form})

def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'colis/modifier_employe.html', {'form': form, 'employe': employe})

def details_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    return render(request, 'colis/details_employe.html', {'employe': employe})

def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == 'POST':
        employe.delete()
        return redirect('liste_employes')
    return render(request, 'colis/supprimer.html', {'employe': employe})

# -------------- Vues pour la gestion des Clients --------------

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'colis/liste_clients.html', {'clients': clients})

def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'colis/ajouter.html', {'form': form})

def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'colis/modifier_client.html', {'form': form, 'client': client})

def details_client(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, 'colis/details_client.html', {'client': client})

def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'colis/supprimer.html', {'client': client})

def tableau_bord(request):
    # Date d'aujourd'hui
    today = timezone.now().date()
    # Obtenir la date du début de la semaine en cours (lundi)
    start_of_week = today - timedelta(days=today.weekday())
    # Obtenir la date de fin de la semaine (dimanche)
    end_of_week = start_of_week + timedelta(days=6)

    # Statistiques de la semaine en cours
    clients_data = Client.objects.annotate(
        colis_count=Count('colis_envoyes', filter=Q(colis_envoyes__date_envoi__range=[start_of_week, end_of_week])),
        poids_total=Sum('colis_envoyes__poids', filter=Q(colis_envoyes__date_envoi__range=[start_of_week, end_of_week])),
    )

    # Statistiques des colis par entrepôt
    entrepots_data = Entrepot.objects.annotate(
        colis_count=Count('colis_origine') + Count('colis_destination'),  # Compte tous les colis associés à l'entrepôt
        poids_total=Sum('colis_origine__poids') + Sum('colis_destination__poids')  # Somme des poids des colis
    )

    context = {
        'clients_data': clients_data,
        'entrepots_data': entrepots_data,  # Ajout des données des entrepôts
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
    }
    
    return render(request, 'colis/tableau_bord.html', context)


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Colis

def generer_facture(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{colis.reference}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Informations de l'agence
    p.drawString(100, height - 50, "Yanis K Africa")
    p.drawString(100, height - 65, "2 avenue Henri Barbusse")
    p.drawString(100, height - 80, "93000 Bobigny")
    p.drawString(100, height - 95, "Tel: 06 14 06 29 34")

    # Détails du colis
    p.drawString(100, height - 120, f"Facture pour le colis {colis.reference}")
    p.drawString(100, height - 140, f"Expéditeur: {colis.expediteur.nom} ({colis.expediteur.telephone})")
    p.drawString(100, height - 160, f"Récepteur: {colis.recepteur.nom} ({colis.recepteur.telephone})")
    p.drawString(100, height - 180, f"Poids total: {colis.poids} kg")
    p.drawString(100, height - 200, f"Nombre de colis: 1")
    
    total_price = colis.poids * 10  # 10 EUR par kg
    p.drawString(100, height - 220, f"Total: {total_price} EUR")
    p.drawString(100, height - 240, "Type de fret: Aérien")

    p.showPage()
    p.save()
    return response

def modifier_statut_colis(request, reference):
    colis = get_object_or_404(Colis, reference=reference)

    if request.method == 'POST':
        # Récupérer l'ancien statut
        ancien_statut = colis.statut
        
        form = StatutColisForm(request.POST, instance=colis)
        if form.is_valid():
            colis = form.save()  # Enregistrer le colis avec le nouveau statut
            
            # Vérifier si le statut a changé
            if ancien_statut != colis.statut:
                message = f"Le statut de votre colis {colis.reference} a est passé de '{ancien_statut}' à '{colis.statut}'."
                
                # Envoyer SMS à l'expéditeur et au récepteur
                send_sms(colis.expediteur.telephone, message)
                send_sms(colis.recepteur.telephone, message)

            return redirect('details_colis', reference=colis.reference)
    else:
        form = StatutColisForm(instance=colis)
    
    return render(request, 'colis/modifier_statut.html', {'form': form, 'colis': colis})