from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, nom, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nom, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire de stock'),
        ('vendeur', 'Vendeur / Commercial'),
        ('client', 'Client'),
    ]

    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.nom} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_gestionnaire(self):
        return self.role == 'gestionnaire'

    @property
    def is_vendeur(self):
        return self.role == 'vendeur'

    @property
    def is_client_role(self):
        return self.role == 'client'


class JournalActivite(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    objet = models.CharField(max_length=255, blank=True)
    details = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Journal d'activité"
        verbose_name_plural = "Journaux d'activité"

    def __str__(self):
        return f"{self.utilisateur} — {self.action} ({self.date:%d/%m/%Y %H:%M})"
