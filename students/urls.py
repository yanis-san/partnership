from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from . import views

# Fonction pour vérifier si l'utilisateur est superuser
def is_superuser(user):
    return user.is_superuser

urlpatterns = [
    # Pages publiques - Inscription seulement
    path('', views.StudentRegistrationView.as_view(), name='student-register'),
    path('success/', views.RegistrationSuccessView.as_view(), name='registration-success'),
]

# QR codes et dashboard librairie - SUPERUSER ONLY
urlpatterns += [
    path('qrcode/<str:code>/', login_required(views.generate_qr_code), name='generate-qr-code'),
    path('qrcodes/', user_passes_test(is_superuser)(views.QRCodeListView.as_view()), name='qr-code-list'),
]
