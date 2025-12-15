from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .models import Partner, PartnershipCode, Payment, PartnershipRequest, PaymentCheckpoint


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_code', 'email', 'status', 'total_students_confirmed', 'revenue_real', 'payment_status')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'contact_person')
    readonly_fields = ('id', 'created_at', 'updated_at', 'partner_code', 'revenue_info')
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'name', 'email', 'phone', 'contact_person', 'address', 'status')
        }),
        ('Commission', {
            'fields': ('commission_per_student',)
        }),
        ('Revenus (depuis dernier checkpoint)', {
            'fields': ('revenue_info',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['create_payment_checkpoint']

    def partner_code(self, obj):
        return obj.partner_code
    partner_code.short_description = "Code Partenaire"

    def revenue_info(self, obj):
        """Affiche les informations de revenu"""
        return f"""
        Étudiants confirmés (depuis dernier checkpoint): {obj.total_students_confirmed}
        Revenu estimé: {obj.revenue_estimated:.2f} DA
        Revenu réel: {obj.revenue_real:.2f} DA
        Statut: {obj.payment_status}
        """
    revenue_info.short_description = "Informations de revenu"

    def create_payment_checkpoint(self, request, queryset):
        """Action pour créer un checkpoint de paiement"""
        from django.contrib.admin.views.decorators import staff_member_required
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        if queryset.count() == 1:
            partner = queryset[0]
            # Rediriger vers une page spéciale pour créer le checkpoint
            return HttpResponseRedirect(f"/admin/partnerships/paymentcheckpoint/add/?partner={partner.id}")
        else:
            self.message_user(request, "Veuillez sélectionner un seul partenaire à la fois.")
    create_payment_checkpoint.short_description = "Créer un checkpoint de paiement"


@admin.register(PartnershipCode)
class PartnershipCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'partner', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'partner')
    search_fields = ('code', 'partner__name')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Code', {
            'fields': ('id', 'code', 'partner', 'is_active')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('partner', 'amount_display', 'amount_paid_display', 'remaining_amount_display', 'status_display', 'reference', 'created_at')
    list_filter = ('status', 'created_at', 'partner')
    search_fields = ('partner__name', 'reference')
    readonly_fields = ('id', 'created_at', 'completed_at', 'remaining_amount_display', 'status_display')
    fieldsets = (
        ('Paiement', {
            'fields': ('id', 'partner', 'amount')
        }),
        ('Statut du paiement', {
            'fields': ('remaining_amount_display', 'status_display', 'completed_at'),
            'description': 'Le statut et le montant restant se mettent à jour automatiquement quand vous sauvegardez.'
        }),
        ('Détails', {
            'fields': ('reference', 'notes')
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_completed', 'mark_as_pending']

    def amount_display(self, obj):
        """Afficher le montant à payer"""
        return f"{obj.amount:.2f} DA"
    amount_display.short_description = "Montant à payer"

    def amount_paid_display(self, obj):
        """Afficher le montant payé - recalculé dynamiquement"""
        # Recalculer pour s'assurer que c'est à jour
        obj.update_payment_status()
        paid = obj.amount - obj.remaining_amount
        return f"{paid:.2f} DA"
    amount_paid_display.short_description = "Montant payé"

    def remaining_amount_display(self, obj):
        """Afficher le montant restant - recalculé dynamiquement"""
        # Recalculer pour s'assurer que c'est à jour
        obj.update_payment_status()
        return f"{obj.remaining_amount:.2f} DA"
    remaining_amount_display.short_description = "Montant restant"

    def status_display(self, obj):
        """Afficher le statut avec couleur"""
        # Recalculer pour s'assurer que c'est à jour
        obj.update_payment_status()
        status_map = {
            'pending': '❌ Non payé',
            'partial': '⚠️ Partiel',
            'completed': '✅ Payé',
            'cancelled': '⛔ Annulé'
        }
        return status_map.get(obj.status, obj.get_status_display())
    status_display.short_description = "Statut"

    def mark_as_completed(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.status != Payment.COMPLETED:
                payment.mark_as_completed()
                count += 1
        self.message_user(request, f"{count} paiement(s) marqué(s) comme complété(s).")
    mark_as_completed.short_description = "Marquer comme complété"

    def mark_as_pending(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.status != Payment.PENDING:
                payment.mark_as_pending()
                count += 1
        self.message_user(request, f"{count} paiement(s) marqué(s) comme en attente.")
    mark_as_pending.short_description = "Marquer comme en attente"


@admin.register(PartnershipRequest)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'business_type', 'email', 'phone', 'created_at', 'is_processed')
    list_filter = ('business_type', 'is_processed', 'created_at')
    search_fields = ('business_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Informations du commerce', {
            'fields': ('id', 'business_name', 'business_type', 'email', 'phone', 'address')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Statut', {
            'fields': ('is_processed', 'created_at')
        }),
    )
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        count = queryset.update(is_processed=True)
        self.message_user(request, f"{count} demande(s) marquée(s) comme traitée(s).")
    mark_as_processed.short_description = "Marquer comme traitée"


@admin.register(PaymentCheckpoint)
class PaymentCheckpointAdmin(admin.ModelAdmin):
    list_display = ('partner', 'amount_paid', 'checkpoint_date', 'created_at')
    list_filter = ('partner', 'checkpoint_date', 'created_at')
    search_fields = ('partner__name',)
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Checkpoint', {
            'fields': ('id', 'partner', 'amount_paid', 'checkpoint_date')
        }),
        ('Détails', {
            'fields': ('notes',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('partner')
