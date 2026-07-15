from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('inscription/', views.register_view, name='register'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
    path('utilisateurs/', views.user_list_view, name='user_list'),
    path('utilisateurs/ajouter/', views.user_create_view, name='user_create'),
    path('utilisateurs/<int:pk>/modifier/', views.user_edit_view, name='user_edit'),
    path('utilisateurs/<int:pk>/supprimer/', views.user_delete_view, name='user_delete'),
    path('journal/', views.journal_activite_view, name='journal_activite'),
]
