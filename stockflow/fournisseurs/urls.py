from django.urls import path
from . import views

urlpatterns = [
    path('fournisseurs/', views.fournisseur_list_view, name='fournisseur_list'),
    path('fournisseurs/ajouter/', views.fournisseur_create_view, name='fournisseur_create'),
    path('fournisseurs/<int:pk>/modifier/', views.fournisseur_edit_view, name='fournisseur_edit'),
    path('fournisseurs/<int:pk>/supprimer/', views.fournisseur_delete_view, name='fournisseur_delete'),
    path('commandes/', views.commande_achat_list_view, name='commande_achat_list'),
    path('commandes/ajouter/', views.commande_achat_create_view, name='commande_achat_create'),
    path('commandes/<int:pk>/', views.commande_achat_detail_view, name='commande_achat_detail'),
    path('commandes/<int:pk>/modifier/', views.commande_achat_edit_view, name='commande_achat_edit'),
    path('commandes/<int:pk>/supprimer/', views.commande_achat_delete_view, name='commande_achat_delete'),
    path('commandes/<int:pk>/reception/', views.reception_commande_view, name='commande_achat_reception'),
]
