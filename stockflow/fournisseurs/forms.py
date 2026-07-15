from django import forms
from .models import Fournisseur, CommandeAchat


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'contact_nom', 'email', 'telephone', 'adresse', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_nom': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telephone': forms.TextInput(attrs={'class': 'form-input'}),
            'adresse': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'actif': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }


class CommandeAchatForm(forms.ModelForm):
    class Meta:
        model = CommandeAchat
        fields = ['reference', 'fournisseur', 'statut', 'notes']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-input'}),
            'fournisseur': forms.Select(attrs={'class': 'form-input'}),
            'statut': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
