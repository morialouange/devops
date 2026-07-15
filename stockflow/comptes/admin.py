from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, JournalActivite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'nom', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'nom')
    list_per_page = 20
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations StockFlow', {'fields': ('nom', 'telephone', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations StockFlow', {'fields': ('nom', 'telephone', 'role')}),
    )


@admin.register(JournalActivite)
class JournalActiviteAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'action', 'objet', 'date')
    list_filter = ('date',)
    search_fields = ('utilisateur__nom', 'action', 'objet')
    list_per_page = 20
    readonly_fields = ('date',)
