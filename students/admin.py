from django.contrib import admin
from .models import Student, Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'partner', 'program', 'status', 'confirmation_display', 'enrollment_date')
    list_filter = ('status', 'is_confirmed', 'program', 'partner', 'enrollment_date')
    search_fields = ('full_name', 'email', 'referral_code')
    readonly_fields = ('id', 'enrollment_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('id', 'full_name', 'email', 'phone')
        }),
        ('Inscription et partenariat', {
            'fields': ('partner', 'referral_code', 'program', 'status', 'is_confirmed')
        }),
        ('Métadonnées', {
            'fields': ('enrollment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def confirmation_display(self, obj):
        """Affiche le statut de confirmation avec un emoji"""
        if obj.is_confirmed:
            return '✅ Confirmé'
        else:
            return '⏳ En attente'
    confirmation_display.short_description = 'Confirmation'
