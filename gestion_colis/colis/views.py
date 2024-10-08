from django.shortcuts import render, get_object_or_404, redirect
from .models import Colis, Entrepot, Employe, Client
from .forms import ColisForm, EmployeForm, ClientForm, StatutColisForm
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .forms import WeekSelectionForm
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta 
from .utils import send_sms  # Assurez-vous que le chemin est correct


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
            colis = form.save()  # La référence sera générée automatiquement
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
    query = request.GET.get('q', '')
    if query:
        employes = Employe.objects.filter(user__username__icontains=query)
    else:
        employes = Employe.objects.all()
    
    return render(request, 'colis/liste_employes.html', {'employes': employes, 'query': query})


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
    query = request.GET.get('q', '')
    if query:
        clients = Client.objects.filter(nom__icontains=query)
    else:
        clients = Client.objects.all()

    return render(request, 'colis/liste_clients.html', {'clients': clients, 'query': query})


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
    # Gestion des dates pour la semaine
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Lundi
    end_of_week = start_of_week + timedelta(days=6)  # Dimanche

    # Traitement du formulaire
    form = WeekSelectionForm(request.GET or None)

    if form.is_valid():
        # Ici, vous pouvez gérer les dates de la semaine selon la sélection de l'utilisateur
        # Pour l'instant, nous utilisons la semaine actuelle
        pass

    # Récupération des clients et de leurs colis envoyés cette semaine
    clients_data = Client.objects.annotate(
        colis_count=Count('colis_envoyes', filter=Q(colis_envoyes__date_envoi__range=[start_of_week, end_of_week])),
        poids_total=Sum('colis_envoyes__poids', filter=Q(colis_envoyes__date_envoi__range=[start_of_week, end_of_week])),
    )

    # Récupération des entrepôts et du nombre de colis
    entrepots = Entrepot.objects.annotate(
        capacite_utilisee=Count('colis')
    )

    context = {
        'form': form,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'clients_data': clients_data,
        'entrepots': entrepots,
    }

    return render(request, 'colis/tableau_bord.html', context)


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Colis
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle


def generer_facture(request, colis_id):
    colis = get_object_or_404(Colis, id=colis_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{colis.reference}.pdf"'

    # Création du document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 24

    # Titre de la facture
    elements.append(Paragraph("Facture", title_style))
    elements.append(Paragraph(f"Référence: {colis.reference}", styles['Normal']))
    elements.append(Paragraph(f"Date d'envoi: {colis.date_envoi.strftime('%d %B %Y')}", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))  # Ligne vide

    # Informations de l'agence
    elements.append(Paragraph("Yanis K Africa", styles['Normal']))
    elements.append(Paragraph("2 avenue Henri Barbusse", styles['Normal']))
    elements.append(Paragraph("93000 Bobigny", styles['Normal']))
    elements.append(Paragraph("Tel: 06 14 06 29 34", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))  # Ligne vide

    # Détails du colis
    elements.append(Paragraph("Détails du Colis", styles['Heading3']))
    data = [
        ['Expéditeur', f"{colis.expediteur.nom if colis.expediteur else 'Inconnu'} ({colis.expediteur.telephone if colis.expediteur else 'N/A'})"],
        ['Récepteur', f"{colis.recepteur.nom if colis.recepteur else 'Inconnu'} ({colis.recepteur.telephone if colis.recepteur else 'N/A'})"],
        ['Poids Total', f"{colis.poids} kg"],
        ['Statut', colis.statut],
    ]

    # Créer un tableau pour les détails
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Paragraph(" ", styles['Normal']))  # Ligne vide

    # Total
    total_price = colis.poids * 10  # 10 EUR par kg
    elements.append(Paragraph(f"Total à payer: {total_price} EUR", styles['Normal']))

    # Générer le document
    doc.build(elements)
    return response


def modifier_statut_colis(request, reference):
    colis = get_object_or_404(Colis, reference=reference)

    if request.method == 'POST':
        ancien_statut = colis.statut  # Récupérer l'ancien statut
        form = StatutColisForm(request.POST, instance=colis)
        if form.is_valid():
            colis = form.save()  # Enregistrer le colis avec le nouveau statut
            
            # Vérifier si le statut a changé
            if ancien_statut != colis.statut:
                message = f"Le statut de votre colis {colis.reference} a été modifié de '{ancien_statut}' à '{colis.statut}'."
                
                # Envoyer SMS à l'expéditeur et au récepteur
                send_sms(colis.expediteur.telephone, message)
                send_sms(colis.recepteur.telephone, message)

            return redirect('details_colis', reference=colis.reference)
    else:
        form = StatutColisForm(instance=colis)
    
    return render(request, 'colis/modifier_statut.html', {'form': form, 'colis': colis})
