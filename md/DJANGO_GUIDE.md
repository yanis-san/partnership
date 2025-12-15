# 🎯 IRL AD - Guide Complet Django

Migration complète de Flask vers Django avec authentification et autorisation.

---

## 📋 Table des matières

1. [Setup initial](#setup-initial)
2. [Structure du projet](#structure-du-projet)
3. [Configuration Django](#configuration-django)
4. [Modèles de données](#modèles-de-données)
5. [Authentification & Autorisation](#authentification--autorisation)
6. [Formulaires](#formulaires)
7. [Vues (Views)](#vues-views)
8. [Templates](#templates)
9. [Urls](#urls)
10. [Commandes Django](#commandes-django)

---

## 🚀 Setup Initial

### 1. Installation des dépendances

```bash
# Créer dossier du projet
mkdir irl_ad_django
cd irl_ad_django

# Créer virtual env
python -m venv venv

# Activer
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer Django et dépendances
pip install django
pip install django-extensions
pip install pillow  # Pour les images
pip install python-dotenv
```

### 2. Créer le projet Django

```bash
# Créer le projet
django-admin startproject config .

# Créer l'app principale
python manage.py startapp core

# Créer app pour auth
python manage.py startapp accounts
```

### 3. Structure du projet

```
irl_ad_django/
├── venv/
├── config/
│   ├── __init__.py
│   ├── settings.py          ← À modifier
│   ├── urls.py              ← À modifier
│   ├── asgi.py
│   └── wsgi.py
├── core/                    ← App principale
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            ← À créer
│   ├── views.py             ← À créer
│   ├── urls.py              ← À créer
│   ├── forms.py             ← À créer
│   └── tests.py
├── accounts/                ← App authentification
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── models.py            ← À créer
│   ├── views.py             ← À créer
│   ├── urls.py              ← À créer
│   ├── forms.py             ← À créer
│   └── decorators.py        ← À créer
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
├── .env
├── manage.py
└── requirements.txt
```

---

## ⚙️ Configuration Django

### 1. config/settings.py

```python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET KEY - CHANGE EN PRODUCTION
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

# DEBUG
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# INSTALLED APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps locales
    'core',
    'accounts',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE - SQLite par défaut (pas Supabase!)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si vous voulez utiliser PostgreSQL local:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'irl_ad'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN URLS
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'core:index'

# AUTH SETTINGS
AUTH_USER_MODEL = 'auth.User'  # Utiliser le User par défaut

# COMMISSION SETTINGS
COMMISSION_STUDENT = 1000  # 1000 DA par élève
```

### 2. config/urls.py

```python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 3. .env

```env
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here

# Database (SQLite - par défaut)
# Ou PostgreSQL:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=irl_ad
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🗄️ Modèles de Données

### core/models.py

```python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import random
import string

class Librairie(models.Model):
    """Modèle pour une librairie partenaire"""
    STATUS_CHOICES = [
        ('non_paye', 'Non payé'),
        ('partiel', 'Partiel'),
        ('paye', 'Payé'),
    ]

    nom = models.CharField(max_length=100)
    code_promo = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)

    # Finance
    total_genere = models.IntegerField(default=0)
    montant_paye = models.IntegerField(default=0)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='non_paye')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Librairie"
        verbose_name_plural = "Librairies"

    def __str__(self):
        return f"{self.nom} ({self.code_promo})"

    def calculate_stats(self):
        """Recalculer les statistiques"""
        # Total généré = nb élèves × 1000
        self.total_genere = self.eleves.count() * settings.COMMISSION_STUDENT

        # Total payé = somme des paiements
        self.montant_paye = sum(p.montant for p in self.paiements.all())

        # Mettre à jour le statut
        montant_restant = self.total_genere - self.montant_paye

        if montant_restant <= 0 and self.total_genere > 0:
            self.statut = 'paye'
        elif self.montant_paye > 0 and montant_restant > 0:
            self.statut = 'partiel'
        else:
            self.statut = 'non_paye'

        self.save()

    @property
    def montant_restant(self):
        """Montant restant à payer"""
        return self.total_genere - self.montant_paye

    @staticmethod
    def generer_code_unique():
        """Générer un code promo unique"""
        while True:
            code = 'LIB-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not Librairie.objects.filter(code_promo=code).exists():
                return code


class Eleve(models.Model):
    """Modèle pour un élève inscrit"""
    nom_complet = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)

    # Foreign Key
    librairie = models.ForeignKey(
        Librairie,
        on_delete=models.CASCADE,
        related_name='eleves'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"

    def __str__(self):
        return f"{self.nom_complet} - {self.librairie.nom}"


class Paiement(models.Model):
    """Modèle pour un paiement"""
    montant = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True)

    # Foreign Key
    librairie = models.ForeignKey(
        Librairie,
        on_delete=models.CASCADE,
        related_name='paiements'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"{self.montant} DA - {self.librairie.nom}"

    def save(self, *args, **kwargs):
        """Mettre à jour les stats de la libraire après paiement"""
        super().save(*args, **kwargs)
        self.librairie.calculate_stats()
```

---

## 🔐 Authentification & Autorisation

### accounts/models.py

```python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    """Profil utilisateur étendu"""
    ROLES = [
        ('admin', 'Administrateur'),
        ('libraire', 'Libraire'),
        ('student', 'Élève'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=ROLES, default='student')

    # Si c'est un libraire
    librairie = models.OneToOneField(
        'core.Librairie',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsable'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
```

### accounts/decorators.py

```python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

def admin_required(view_func):
    """Décorateur: Only for admins"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        if not request.user.is_staff and not (hasattr(request.user, 'profil') and request.user.profil.role == 'admin'):
            return redirect('core:index')

        return view_func(request, *args, **kwargs)

    return wrapper


def libraire_required(view_func):
    """Décorateur: Only for libraires"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        if not (hasattr(request.user, 'profil') and request.user.profil.role == 'libraire'):
            return redirect('core:index')

        return view_func(request, *args, **kwargs)

    return wrapper


def login_required_custom(view_func):
    """Décorateur: Must be logged in"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        return view_func(request, *args, **kwargs)

    return wrapper
```

---

## 📝 Formulaires

### core/forms.py

```python
# -*- coding: utf-8 -*-
from django import forms
from .models import Librairie, Eleve, Paiement

class InscriptionEleveForm(forms.ModelForm):
    """Formulaire d'inscription élève"""
    code_librairie = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: LIB-XXXXX'
        }),
        label='Code Librairie'
    )

    class Meta:
        model = Eleve
        fields = ['nom_complet', 'email', 'telephone']
        widgets = {
            'nom_complet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre@email.com'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+213 XXX XXX XXX'
            }),
        }

    def clean_code_librairie(self):
        code = self.cleaned_data.get('code_librairie')
        if not Librairie.objects.filter(code_promo=code.upper()).exists():
            raise forms.ValidationError('Code librairie invalide')
        return code.upper()


class AjouterLibrairieForm(forms.ModelForm):
    """Formulaire ajouter librairie (admin)"""
    class Meta:
        model = Librairie
        fields = ['nom', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PaiementForm(forms.ModelForm):
    """Formulaire paiement"""
    class Meta:
        model = Paiement
        fields = ['montant', 'reference']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    """Formulaire de contact"""
    nom_complet = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    code_librairie = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
```

### accounts/forms.py

```python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class LoginForm(AuthenticationForm):
    """Formulaire login personnalisé"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )


class SignupForm(UserCreationForm):
    """Formulaire inscription"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
```

---

## 👁️ Vues (Views)

### core/views.py

```python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.contrib import messages
from django.conf import settings

from .models import Librairie, Eleve, Paiement
from .forms import InscriptionEleveForm, AjouterLibrairieForm, PaiementForm, ContactForm
from accounts.decorators import admin_required, libraire_required, login_required_custom

# ============================================================================
# PAGES PUBLIQUES
# ============================================================================

def index(request):
    """Page d'accueil"""
    context = {
        'total_eleves': Eleve.objects.count(),
        'total_libraires': Librairie.objects.count(),
        'total_genere': Eleve.objects.count() * settings.COMMISSION_STUDENT,
        'total_paye': Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0,
    }
    return render(request, 'index.html', context)


def inscrire(request):
    """Inscription élève"""
    if request.method == 'POST':
        form = InscriptionEleveForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code_librairie']
            librairie = Librairie.objects.get(code_promo=code)

            # Créer l'élève
            eleve = form.save(commit=False)
            eleve.librairie = librairie
            eleve.save()

            # Mettre à jour les stats
            librairie.calculate_stats()

            messages.success(request, f'Inscription réussie! Bienvenue {eleve.nom_complet}')
            return redirect('core:confirmation', eleve_id=eleve.id)
    else:
        form = InscriptionEleveForm()

    return render(request, 'inscrire.html', {'form': form})


def confirmation(request, eleve_id):
    """Confirmation d'inscription"""
    eleve = get_object_or_404(Eleve, id=eleve_id)
    return render(request, 'confirmation.html', {'eleve': eleve})


def librairies(request):
    """Liste les librairies"""
    libraires = Librairie.objects.annotate(nb_eleves=Count('eleves'))

    # Recherche
    search = request.GET.get('search', '')
    if search:
        libraires = libraires.filter(nom__icontains=search) | libraires.filter(code_promo__icontains=search)

    context = {
        'libraires': libraires,
        'search': search,
    }
    return render(request, 'librairies.html', context)


def detail_librairie(request, librairie_id):
    """Détail d'une librairie"""
    librairie = get_object_or_404(Librairie, id=librairie_id)
    librairie.calculate_stats()

    context = {
        'librairie': librairie,
        'nb_eleves': librairie.eleves.count(),
    }
    return render(request, 'detail_librairie.html', context)


def contact(request):
    """Page contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Traiter le formulaire (email, db, etc)
            messages.success(request, 'Merci pour votre message!')
            return redirect('core:index')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ============================================================================
# DASHBOARD ADMIN
# ============================================================================

@admin_required
def dashboard_admin(request):
    """Dashboard admin"""
    libraires = Librairie.objects.all()

    context = {
        'libraires': libraires,
        'total_eleves': Eleve.objects.count(),
        'total_genere': Eleve.objects.count() * settings.COMMISSION_STUDENT,
        'total_paye': Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0,
        'paiements_recents': Paiement.objects.select_related('librairie')[:10],
    }
    return render(request, 'admin/dashboard.html', context)


@admin_required
@require_http_methods(["POST"])
def ajouter_librairie(request):
    """Ajouter une librairie"""
    form = AjouterLibrairieForm(request.POST)
    if form.is_valid():
        librairie = form.save(commit=False)
        librairie.code_promo = Librairie.generer_code_unique()
        librairie.save()

        messages.success(request, f'Librairie "{librairie.nom}" créée avec code {librairie.code_promo}')

    return redirect('core:dashboard_admin')


@admin_required
def detail_libraire_admin(request, librairie_id):
    """Détail libraire (admin)"""
    librairie = get_object_or_404(Librairie, id=librairie_id)
    librairie.calculate_stats()

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.librairie = librairie
            paiement.save()

            librairie.calculate_stats()
            messages.success(request, 'Paiement enregistré')
            return redirect('core:detail_libraire_admin', librairie_id=librairie.id)
    else:
        form = PaiementForm(initial={'montant': librairie.montant_restant})

    context = {
        'librairie': librairie,
        'eleves': librairie.eleves.all(),
        'paiements': librairie.paiements.all(),
        'form': form,
    }
    return render(request, 'admin/detail_libraire.html', context)


@admin_required
def modifier_librairie(request, librairie_id):
    """Modifier librairie"""
    librairie = get_object_or_404(Librairie, id=librairie_id)

    if request.method == 'POST':
        form = AjouterLibrairieForm(request.POST, instance=librairie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Librairie modifiée')
            return redirect('core:detail_libraire_admin', librairie_id=librairie.id)
    else:
        form = AjouterLibrairieForm(instance=librairie)

    return render(request, 'admin/modifier_librairie.html', {'form': form, 'librairie': librairie})


@admin_required
@require_http_methods(["POST"])
def supprimer_librairie(request, librairie_id):
    """Supprimer librairie"""
    librairie = get_object_or_404(Librairie, id=librairie_id)
    nom = librairie.nom
    librairie.delete()

    messages.warning(request, f'Librairie "{nom}" supprimée')
    return redirect('core:dashboard_admin')


# ============================================================================
# DASHBOARD LIBRAIRE
# ============================================================================

@libraire_required
def dashboard_libraire(request):
    """Dashboard personnalisé pour libraire"""
    librairie = request.user.profil.librairie
    librairie.calculate_stats()

    context = {
        'librairie': librairie,
        'eleves': librairie.eleves.all(),
        'paiements': librairie.paiements.all(),
    }
    return render(request, 'libraire/dashboard.html', context)


# ============================================================================
# API JSON
# ============================================================================

from django.http import JsonResponse

def api_librairies(request):
    """API: Liste des librairies"""
    libraires = Librairie.objects.all()

    data = [{
        'id': lib.id,
        'nom': lib.nom,
        'code_promo': lib.code_promo,
        'nb_eleves': lib.eleves.count(),
        'total_genere': lib.total_genere,
        'montant_paye': lib.montant_paye,
        'statut': lib.statut,
    } for lib in libraires]

    return JsonResponse(data, safe=False)


def api_stats(request):
    """API: Statistiques globales"""
    data = {
        'total_eleves': Eleve.objects.count(),
        'total_libraires': Librairie.objects.count(),
        'total_genere': Eleve.objects.count() * settings.COMMISSION_STUDENT,
        'total_paye': Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0,
    }
    return JsonResponse(data)
```

### accounts/views.py

```python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import LoginForm, SignupForm
from .models import Profil

class LoginCustomView(LoginView):
    """Vue de login personnalisée"""
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class LogoutCustomView(LogoutView):
    """Vue de logout"""
    next_page = 'core:index'


class SignupView(CreateView):
    """Vue d'inscription"""
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Créer un profil
        Profil.objects.create(
            user=self.object,
            role='student'
        )

        messages.success(self.request, 'Inscription réussie! Connectez-vous.')
        return response


def logout_view(request):
    """Logout"""
    logout(request)
    messages.success(request, 'Vous êtes déconnecté')
    return redirect('core:index')
```

---

## 🎨 Templates

### templates/base.html

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}IRL AD{% endblock %}</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        :root {
            --primary: #2563eb;
            --secondary: #64748b;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .navbar {
            background: linear-gradient(135deg, var(--primary) 0%, #1e40af 100%);
        }

        .card {
            border: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-lg">
            <a class="navbar-brand" href="{% url 'core:index' %}">
                <i class="fas fa-graduation-cap"></i> IRL AD
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbar">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:index' %}">Accueil</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:librairies' %}">Librairies</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:inscrire' %}">S'inscrire</a>
                    </li>

                    {% if user.is_authenticated %}
                        {% if user.is_staff %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:dashboard_admin' %}">Admin</a>
                            </li>
                        {% endif %}
                        {% if user.profil.role == 'libraire' %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:dashboard_libraire' %}">Mon Dashboard</a>
                            </li>
                        {% endif %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:logout' %}">Déconnexion</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:login' %}">Connexion</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
        <div class="container-lg mt-4">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container-lg">
            <p class="text-center mb-0">&copy; 2024 IRL AD - Tous droits réservés</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### templates/index.html

```html
{% extends 'base.html' %}

{% block title %}Accueil - IRL AD{% endblock %}

{% block content %}
    <section class="bg-primary text-white py-5">
        <div class="container-lg text-center">
            <h1>Publicité Scolaire Transparente</h1>
            <p class="lead">Aider les librairies et écoles à se développer ensemble</p>
            <a href="{% url 'core:inscrire' %}" class="btn btn-light btn-lg">S'inscrire</a>
        </div>
    </section>

    <!-- Stats -->
    <section class="py-5">
        <div class="container-lg">
            <div class="row">
                <div class="col-md-3 mb-4">
                    <div class="card text-center p-4">
                        <h3 class="text-primary">{{ total_eleves }}</h3>
                        <p>Élèves inscrits</p>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card text-center p-4">
                        <h3 class="text-primary">{{ total_libraires }}</h3>
                        <p>Librairies partenaires</p>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card text-center p-4">
                        <h3 class="text-primary">{{ total_genere }} DA</h3>
                        <p>Montant généré</p>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="card text-center p-4">
                        <h3 class="text-primary">{{ total_paye }} DA</h3>
                        <p>Montant payé</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
{% endblock %}
```

### templates/accounts/login.html

```html
{% extends 'base.html' %}

{% block title %}Connexion - IRL AD{% endblock %}

{% block content %}
    <div class="container-lg py-5">
        <div class="row">
            <div class="col-lg-6 offset-lg-3">
                <div class="card">
                    <div class="card-body p-5">
                        <h2 class="card-title mb-4">Connexion</h2>

                        <form method="post">
                            {% csrf_token %}

                            <div class="mb-3">
                                {{ form.username.label_tag }}
                                {{ form.username }}
                                {% if form.username.errors %}
                                    <div class="text-danger">{{ form.username.errors }}</div>
                                {% endif %}
                            </div>

                            <div class="mb-3">
                                {{ form.password.label_tag }}
                                {{ form.password }}
                                {% if form.password.errors %}
                                    <div class="text-danger">{{ form.password.errors }}</div>
                                {% endif %}
                            </div>

                            <button type="submit" class="btn btn-primary w-100">Connexion</button>
                        </form>

                        <hr>

                        <p class="text-center">
                            Pas de compte? <a href="{% url 'accounts:signup' %}">S'inscrire</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

---

## 🌐 URLs

### core/urls.py

```python
# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public
    path('', views.index, name='index'),
    path('inscrire/', views.inscrire, name='inscrire'),
    path('confirmation/<int:eleve_id>/', views.confirmation, name='confirmation'),
    path('librairies/', views.librairies, name='librairies'),
    path('librairie/<int:librairie_id>/', views.detail_librairie, name='detail_librairie'),
    path('contact/', views.contact, name='contact'),

    # Admin
    path('admin/dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('admin/librairie/add/', views.ajouter_librairie, name='ajouter_librairie'),
    path('admin/librairie/<int:librairie_id>/', views.detail_libraire_admin, name='detail_libraire_admin'),
    path('admin/librairie/<int:librairie_id>/modifier/', views.modifier_librairie, name='modifier_librairie'),
    path('admin/librairie/<int:librairie_id>/supprimer/', views.supprimer_librairie, name='supprimer_librairie'),

    # Libraire
    path('libraire/dashboard/', views.dashboard_libraire, name='dashboard_libraire'),

    # API
    path('api/librairies/', views.api_librairies, name='api_librairies'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
```

### accounts/urls.py

```python
# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginCustomView.as_view(), name='login'),
    path('logout/', views.LogoutCustomView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
]
```

---

## ⚡ Commandes Django

### Démarrage rapide

```bash
# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Créer superuser (admin)
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Commandes utiles

```bash
# Shell Django (tester le code)
python manage.py shell

# Créer données de test
python manage.py loaddata fixtures.json

# Sauvegarde données
python manage.py dumpdata > backup.json

# Restaurer données
python manage.py loaddata backup.json

# Vider la DB
python manage.py flush

# Voir les migrations
python manage.py showmigrations

# Tests
python manage.py test
```

---

## 🔐 Système d'autorisation (Récapitulatif)

### Accès par rôle

```
Pages              | Public | Étudiant | Libraire | Admin
───────────────────┼────────┼──────────┼──────────┼──────
/                  |   ✓    |    ✓     |    ✓     |  ✓
/inscrire          |   ✓    |    ✓     |    ✓     |  ✓
/librairies        |   ✓    |    ✓     |    ✓     |  ✓
/libraire/<id>     |   ✓    |    ✓     |    ✓     |  ✓
───────────────────┼────────┼──────────┼──────────┼──────
/libraire/dash     |   ✗    |    ✗     |    ✓     |  ✗
───────────────────┼────────┼──────────┼──────────┼──────
/admin/dashboard   |   ✗    |    ✗     |    ✗     |  ✓
/admin/libraire/...|   ✗    |    ✗     |    ✗     |  ✓
```

### Décorateurs d'autorisation

```python
# Admin seulement
@admin_required
def ma_vue(request):
    ...

# Libraire seulement
@libraire_required
def ma_vue(request):
    ...

# Connecté obligatoire
@login_required_custom
def ma_vue(request):
    ...
```

---

## 📊 Migration depuis Flask

### Équivalences

| Flask | Django |
|-------|--------|
| `@app.route()` | `path()` in urls.py |
| `render_template()` | `render()` |
| `SQLAlchemy Model` | `models.Model` |
| `WTForms` | `Django Forms` |
| `Flask-Login` | `Django Auth` |
| `Blueprints` | `Apps` |

---

## 🚀 Avantages Django

✅ Admin panel automatique
✅ Authentification intégrée
✅ Migrations faciles
✅ ORM très puissant
✅ Sécurité CSRF par défaut
✅ Communauté massive
✅ Documentation excellente

---

## 📚 Prochaines étapes

1. Créer le projet Django
2. Implémenter les modèles
3. Créer les vues
4. Faire les templates
5. Tester l'authentification
6. Déployer en production

---

**Bon développement avec Django! 🚀**
