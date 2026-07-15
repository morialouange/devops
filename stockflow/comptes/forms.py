from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'votre@email.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': '••••••••'
    }))


class RegisterForm(forms.Form):
    nom = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Nom complet'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'votre@email.com'
    }))
    telephone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': '+243 ...'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': '••••••••'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': '••••••••'
    }))

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            nom=self.cleaned_data['nom'],
            telephone=self.cleaned_data.get('telephone', ''),
            password=self.cleaned_data['password'],
            role='client',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nom', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telephone': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input pr-10', 'placeholder': 'Mot de passe'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input pr-10', 'placeholder': 'Confirmer le mot de passe'
    }))

    class Meta:
        model = User
        fields = ['nom', 'email', 'telephone', 'role', 'is_active']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@exemple.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+243 ...'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }

    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            c for c in User.ROLE_CHOICES if c[0] != 'admin'
        ]
        if self.is_edit:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False
            self.fields['password'].help_text = 'Laisser vide pour conserver le mot de passe actuel'

    def clean(self):
        cleaned = super().clean()
        if not self.is_edit:
            if not cleaned.get('password'):
                self.add_error('password', 'Le mot de passe est requis.')
            elif cleaned.get('password') != cleaned.get('password_confirm'):
                self.add_error('password_confirm', 'Les mots de passe ne correspondent pas.')
        else:
            pwd = cleaned.get('password')
            if pwd and pwd != cleaned.get('password_confirm'):
                self.add_error('password_confirm', 'Les mots de passe ne correspondent pas.')
        return cleaned
