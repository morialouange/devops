from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Fournisseur, CommandeAchat, LigneCommandeAchat
from .forms import FournisseurForm, CommandeAchatForm
from stock.models import Stock, Entrepot, MouvementStock


@login_required
def fournisseur_list_view(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/fournisseur_list.html', {'fournisseurs': fournisseurs})


@login_required
def fournisseur_create_view(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur ajouté.")
            return redirect('fournisseur_list')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseurs/form_simple.html', {'form': form, 'title': 'Ajouter un fournisseur', 'cancel_url': 'fournisseur_list'})


@login_required
def fournisseur_edit_view(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur modifié.")
            return redirect('fournisseur_list')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/form_simple.html', {'form': form, 'title': f'Modifier {fournisseur.nom}', 'cancel_url': 'fournisseur_list'})


@login_required
def fournisseur_delete_view(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        fournisseur.delete()
        messages.success(request, "Fournisseur supprimé.")
        return redirect('fournisseur_list')
    return render(request, 'fournisseurs/confirm_delete.html', {'object': fournisseur, 'cancel_url': 'fournisseur_list'})


@login_required
def commande_achat_list_view(request):
    commandes = CommandeAchat.objects.select_related('fournisseur').all()
    return render(request, 'fournisseurs/commande_achat_list.html', {'commandes': commandes})


@login_required
def commande_achat_create_view(request):
    if request.method == 'POST':
        form = CommandeAchatForm(request.POST)
        if form.is_valid():
            cmd = form.save(commit=False)
            cmd.cree_par = request.user
            cmd.save()
            messages.success(request, "Commande d'achat créée.")
            return redirect('commande_achat_list')
    else:
        form = CommandeAchatForm()
    return render(request, 'fournisseurs/form_simple.html', {'form': form, 'title': 'Nouvelle commande d\'achat', 'cancel_url': 'commande_achat_list'})


@login_required
def commande_achat_detail_view(request, pk):
    commande = get_object_or_404(CommandeAchat.objects.select_related('fournisseur').prefetch_related('lignes__produit'), pk=pk)
    return render(request, 'fournisseurs/commande_achat_detail.html', {'commande': commande})


@login_required
def commande_achat_edit_view(request, pk):
    commande = get_object_or_404(CommandeAchat, pk=pk)
    if request.method == 'POST':
        form = CommandeAchatForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, "Commande d'achat modifiée.")
            return redirect('commande_achat_list')
    else:
        form = CommandeAchatForm(instance=commande)
    return render(request, 'fournisseurs/form_simple.html', {'form': form, 'title': f'Modifier {commande.reference}', 'cancel_url': 'commande_achat_list'})


@login_required
def commande_achat_delete_view(request, pk):
    commande = get_object_or_404(CommandeAchat, pk=pk)
    if request.method == 'POST':
        commande.delete()
        messages.success(request, "Commande d'achat supprimée.")
        return redirect('commande_achat_list')
    return render(request, 'fournisseurs/confirm_delete.html', {'object': commande, 'cancel_url': 'commande_achat_list'})


@login_required
def reception_commande_view(request, pk):
    commande = get_object_or_404(
        CommandeAchat.objects.select_related('fournisseur').prefetch_related('lignes__produit'),
        pk=pk
    )

    if request.method == 'POST':
        if commande.statut == 'recue':
            messages.warning(request, "Cette commande a déjà été réceptionnée.")
            return redirect('commande_achat_detail', pk=pk)

        entrepot = Entrepot.objects.filter(actif=True).order_by('pk').first()
        if not entrepot:
            messages.error(request, "Aucun entrepôt disponible pour la réception.")
            return redirect('commande_achat_detail', pk=pk)

        commande.statut = 'recue'
        commande.date_reception = timezone.now()
        commande.save()

        for ligne in commande.lignes.select_related('produit'):
            stock, _ = Stock.objects.get_or_create(
                produit=ligne.produit,
                entrepot=entrepot,
                defaults={'quantite': 0},
            )
            stock.quantite += ligne.quantite
            stock.save()

            MouvementStock.objects.create(
                produit=ligne.produit,
                entrepot=entrepot,
                type_mouvement='entree',
                quantite=ligne.quantite,
                reference=commande.reference,
                motif=f"Réception commande {commande.reference}",
                utilisateur=request.user,
            )

        messages.success(request, f"Commande {commande.reference} réceptionnée. Stock mis à jour.")
        return redirect('commande_achat_detail', pk=pk)

    return render(request, 'fournisseurs/reception.html', {'commande': commande})
