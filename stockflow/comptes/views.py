from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import LoginForm, RegisterForm, ProfileForm, UserForm
from .models import JournalActivite

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'comptes/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès. Connectez-vous.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'comptes/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'comptes/profile.html', {'form': form})


@login_required
def user_list_view(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'comptes/user_list.html', {'users': users})


@login_required
def user_create_view(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                nom=form.cleaned_data['nom'],
                telephone=form.cleaned_data.get('telephone', ''),
                role=form.cleaned_data['role'],
                is_active=form.cleaned_data['is_active'],
                password=form.cleaned_data['password'],
            )
            messages.success(request, f"Utilisateur {user.nom} créé avec succès.")
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'comptes/form_user.html', {'form': form, 'title': 'Créer un utilisateur', 'cancel_url': 'user_list'})


@login_required
def user_edit_view(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    user_obj = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj, is_edit=True)
        if form.is_valid():
            user = form.save(commit=False)
            pwd = form.cleaned_data.get('password')
            if pwd:
                user.set_password(pwd)
            user.save()
            messages.success(request, "Utilisateur mis à jour.")
            return redirect('user_list')
    else:
        form = UserForm(instance=user_obj, is_edit=True)
    return render(request, 'comptes/form_user.html', {'form': form, 'title': f'Modifier {user_obj.nom}', 'cancel_url': 'user_list'})


@login_required
def user_delete_view(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    user_obj = User.objects.get(pk=pk)
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "Utilisateur supprimé.")
        return redirect('user_list')
    return render(request, 'comptes/confirm_delete_user.html', {'object': user_obj})


@login_required
def journal_activite_view(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    entries = JournalActivite.objects.select_related('utilisateur').all()
    user_id = request.GET.get('user')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if user_id:
        entries = entries.filter(utilisateur_id=user_id)
    if date_from:
        entries = entries.filter(date__date__gte=date_from)
    if date_to:
        entries = entries.filter(date__date__lte=date_to)
    paginator = Paginator(entries, 50)
    page = request.GET.get('page')
    entries = paginator.get_page(page)
    users = User.objects.all().order_by('nom')
    return render(request, 'comptes/journal_list.html', {
        'entries': entries,
        'users': users,
        'current_user_id': user_id or '',
        'date_from': date_from or '',
        'date_to': date_to or '',
    })
