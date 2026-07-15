from django.contrib import admin
from .models import Fournisseur, CommandeAchat, LigneCommandeAchat


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact_nom', 'email', 'telephone', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'contact_nom', 'email')
    list_per_page = 20


@admin.register(CommandeAchat)
class CommandeAchatAdmin(admin.ModelAdmin):
    list_display = ('reference', 'fournisseur', 'statut', 'date_commande', 'montant_total')
    list_filter = ('statut', 'fournisseur')
    search_fields = ('reference', 'fournisseur__nom')
    list_per_page = 20
    readonly_fields = ('date_commande',)
    raw_id_fields = ('fournisseur', 'cree_par')


class LigneCommandeAchatInline(admin.TabularInline):
    model = LigneCommandeAchat
    extra = 1
    raw_id_fields = ('produit',)


@admin.register(LigneCommandeAchat)
class LigneCommandeAchatAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite', 'prix_unitaire')
    search_fields = ('commande__reference', 'produit__nom')
    list_per_page = 20
    raw_id_fields = ('commande', 'produit')
