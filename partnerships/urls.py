from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from . import views
import uuid

# Clé secrète pour accéder aux pages admin
ADMIN_SECRET_KEY = "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6"

# Fonction pour vérifier si l'utilisateur est superuser
def is_superuser(user):
    return user.is_superuser

urlpatterns = [
    # Admin Login - Page de connexion admin (secrète)
    path(f'admin-login/{ADMIN_SECRET_KEY}/', views.AdminLoginView.as_view(), name='admin-login'),

    # SUPERUSER ONLY - Admin Home (Centre de Contrôle)
    path('admin-home/', user_passes_test(is_superuser)(views.AdminHomeView.as_view()), name='admin-home'),

    # SUPERUSER ONLY - Dashboard admin et paiements
    path('admin/', user_passes_test(is_superuser)(views.AdminDashboardView.as_view()), name='admin-dashboard'),
    path('stats/', user_passes_test(is_superuser)(views.AdminStatsView.as_view()), name='admin-stats'),
    path('payments/', user_passes_test(is_superuser)(views.PaymentsDashboardView.as_view()), name='payments-dashboard'),
    path('create-partner/', user_passes_test(is_superuser)(views.AdminPartnerCreationView.as_view()), name='create-partner'),
    path('confirmations/', user_passes_test(is_superuser)(views.AdminStudentConfirmationView.as_view()), name='admin-confirmations'),
    path('confirm-student/<uuid:student_id>/', user_passes_test(is_superuser)(views.ConfirmStudentHTMXView.as_view()), name='confirm-student-htmx'),

    # SUPERUSER ONLY - Gestion des paiements avec reçus
    path('payment-form/<uuid:partner_id>/', user_passes_test(is_superuser)(views.PaymentReceiptFormView.as_view()), name='payment-receipt-form'),
    path('payment-upload/<uuid:partner_id>/', user_passes_test(is_superuser)(views.PaymentReceiptUploadView.as_view()), name='payment-receipt-upload'),
    path('payment-history/<uuid:partner_id>/', user_passes_test(is_superuser)(views.PaymentReceiptListView.as_view()), name='payment-history'),

    # Partner dashboard - Public (accessible via code)
    path('partner/<str:code>/', views.PartnerDashboardPublicView.as_view(), name='partner-dashboard'),

    # Partner authentication - Pour les partenaires
    path('login/', views.PartnerLoginView.as_view(), name='partner-login'),
    path('dashboard/', views.PartnerDashboardPersonalView.as_view(), name='partner-dashboard-personal'),
    path('payment-history/', views.PartnerPaymentHistoryView.as_view(), name='partner-payment-history'),
    path('codes/', views.PartnerCodesView.as_view(), name='partner-codes'),
    path('logout/', views.partner_logout_view, name='partner-logout'),

    # Admin logout
    path('admin-logout/', views.admin_logout_view, name='admin-logout'),

    # Partnership request - Demande de partenariat
    path('contact/', views.PartnershipRequestView.as_view(), name='partnership-request'),
    path('contact/success/', views.PartnershipRequestSuccessView.as_view(), name='partnership-request-success'),

    # Admin management - Gestion admin simplifiée
    path('admin/partners/', views.AdminPartnersManagementView.as_view(), name='admin-partners-management'),
    path('admin/partners/<uuid:partner_id>/', views.AdminPartnerDetailView.as_view(), name='admin-partner-detail'),
    path('admin/partners/<uuid:partner_id>/codes/', views.AdminPartnerCodesView.as_view(), name='admin-partner-codes'),
    path('admin/checkpoint/<uuid:partner_id>/', views.AdminCheckpointCreateView.as_view(), name='admin-checkpoint-create'),
    path('admin/confirm-student/<uuid:student_id>/', views.AdminConfirmStudentView.as_view(), name='admin-confirm-student'),

    # Code PDF generation
    path('code/<uuid:code_id>/pdf/', views.GenerateCodePDFView.as_view(), name='generate-code-pdf'),
]
