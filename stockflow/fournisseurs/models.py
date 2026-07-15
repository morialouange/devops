from django.conf import settings
from django.db import models


class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    contact_nom = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class CommandeAchat(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('confirmee', 'Confirmée'),
        ('recue', 'Reçue'),
        ('annulee', 'Annulée'),
    ]

    reference = models.CharField(max_length=50, unique=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    date_commande = models.DateTimeField(auto_now_add=True)
    date_reception = models.DateTimeField(null=True, blank=True)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Commande d'achat"
        verbose_name_plural = "Commandes d'achat"
        ordering = ['-date_commande']

    def __str__(self):
        return f"{self.reference} — {self.fournisseur}"


class LigneCommandeAchat(models.Model):
    commande = models.ForeignKey(CommandeAchat, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('catalogue.Produit', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Ligne de commande d\'achat'
        verbose_name_plural = 'Lignes de commandes d\'achat'

    def __str__(self):
        return f"{self.produit} x{self.quantite}"

    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire
