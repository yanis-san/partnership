# QR Codes - Guide Complet

## Concept Ultra-Simple

Chaque librairie peut afficher un **QR code** dans sa boutique. Quand un élève scanne le code avec son téléphone, il est **automatiquement redirigé vers le formulaire d'inscription avec son code pré-rempli**.

```
Client vient à la librairie
    ↓
Scan le QR code
    ↓
Formulaire s'ouvre automatiquement sur le téléphone
    ↓
Son code est déjà rempli (LIB4F6)
    ↓
Il complète les 5 champs (prénom, nom, email, téléphone, niveau)
    ↓
Il clique "S'inscrire"
    ↓
Terminé! ✓
```

## URLs

### Voir tous les QR codes
```
/register/qrcodes/
```
Affiche les QR codes de toutes les librairies avec:
- Le QR code à scanner
- Le code partenaire
- Un lien direct pour accéder sans scanner

### Générer un QR code spécifique
```
/register/qrcode/LIB4F6/
```
Retourne juste l'image PNG du QR code

### S'inscrire avec code pré-rempli
```
/register/?code=LIB4F6
```
Formulaire d'inscription avec le code pré-rempli

## Deux Méthodes d'Inscription

### Méthode 1: QR Code (Recommandée en Librairie)

**Étapes pour l'élève:**
1. À la librairie, prendre son téléphone
2. Scanner le QR code affiché
3. Remplir 5 champs
4. Cliquer "S'inscrire"
5. Terminé! ✓

**Avantages:**
- Super simple
- Zéro copie du code
- Code pré-rempli automatiquement
- Juste avec le téléphone

**Lien à afficher en librairie:**
```
/register/qrcodes/
```

### Méthode 2: Manuel (Fallback)

**Étapes pour l'élève:**
1. Aller sur /register/
2. Copier le code fourni par la librairie (LIB4F6)
3. Coller le code
4. Remplir les autres champs
5. Cliquer "S'inscrire"
6. Terminé! ✓

**Avantages:**
- Ne nécessite pas de QR code
- Accessible sans scanner
- Peut être fait à la maison

## Pour la Librairie

### Étape 1: Obtenir le QR Code

Accédez à:
```
/register/qrcodes/
```

Vous voyez tous vos codes avec leurs QR codes.

### Étape 2: Télécharger/Imprimer

1. Cliquez sur le QR code
2. Enregistrez l'image (clic droit → "Enregistrer l'image")
3. Imprimez en grande taille (minimum 10cm x 10cm)
4. Plastifiez pour durabilité

### Étape 3: Afficher en Boutique

Mettez un panneau comme:
```
┌─────────────────────────────┐
│  INSCRIVEZ-VOUS À L'ÉCOLE! │
│                             │
│      [ QR CODE ICI ]       │
│                             │
│ Scannez pour vous inscrire  │
│ Commission: 1500 DA/élève  │
└─────────────────────────────┘
```

### Étape 4: Éduquer les Clients

Expliquez aux clients:
"Scannez ce code avec votre téléphone pour vous inscrire à notre école partenaire. Vous recevrez une commission de 1500 DA par élève inscrit!"

## Flux Technique

### Côté Librairie (Admin)

1. Admin crée une librairie → Code auto-généré (LIB4F6)
2. Librairie accède à `/register/qrcodes/`
3. Voit son QR code
4. Télécharge et imprime
5. Affiche en boutique

### Côté Élève

1. Élève arrive à la librairie
2. Scanne le QR code
3. Navigateur mobile ouvre: `http://localhost:8000/register/?code=LIB4F6`
4. Formulaire affiche le code pré-rempli
5. Élève complète prénom, nom, email, téléphone, niveau
6. Clique "S'inscrire"
7. Redirection vers la page de confirmation

### Côté Système

1. QR code contient: `http://localhost:8000/register/?code=LIB4F6`
2. Quand scanné, le paramètre `?code=LIB4F6` est envoyé
3. Vue `StudentRegistrationView.get_initial()` récupère le code
4. Le formulaire est pré-rempli automatiquement
5. Validation et sauvegarde comme normal

## Avantages du Système QR

✓ **Zéro erreur de code** - Pas de copie manuelle
✓ **Ultra rapide** - Juste scanner
✓ **Pas d'authentification** - Direct du téléphone
✓ **Traçabilité** - Chaque QR code est unique
✓ **Imprimable** - Peut être affiché partout
✓ **Économique** - Juste une image
✓ **Viral** - Élèves parlent à d'autres
✓ **Transparent** - Code visible sur le papier

## Pages Web

### Page d'Accueil
```
/
```
Explique le système QR avec lien vers les QR codes

### Page des QR Codes
```
/register/qrcodes/
```
Liste tous les codes avec images QR

### Formulaire d'Inscription
```
/register/?code=LIB4F6
```
Formulaire avec code pré-rempli (depuis QR)

```
/register/
```
Formulaire manuel (sans code pré-rempli)

## Exemple Real-Life

**Librairie du Centre**

1. Admin crée la librairie → Code: LIB4F6
2. Librairie accède à `/register/qrcodes/`
3. Télécharge l'image du QR code
4. Imprime en 20cm x 20cm
5. Plastifie et affiche sur le comptoir
6. Élève arrive, scan le code
7. Son téléphone ouvre: `/register/?code=LIB4F6`
8. Code "LIB4F6" est auto-rempli ✓
9. Élève complète les autres champs
10. Commission de 1500 DA générée ✓

## Techniquement

### Génération du QR Code

```python
url_with_code = "http://localhost:8000/register/?code=LIB4F6"

qr = qrcode.QRCode()
qr.add_data(url_with_code)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode_lib4f6.png")
```

### Récupération du Code

```python
def get_initial(self):
    initial = super().get_initial()
    code = self.request.GET.get('code')  # Récupère ?code=LIB4F6
    if code:
        initial['referral_code'] = code.upper()
    return initial
```

### Affichage dans le Formulaire

```html
{% if code_from_qr %}
    Code pré-rempli depuis le QR code
{% endif %}
```

## URLs Complètes

| Fonction | URL |
|----------|-----|
| Voir tous les QR codes | `/register/qrcodes/` |
| QR code unique (image PNG) | `/register/qrcode/LIB4F6/` |
| Inscription avec code | `/register/?code=LIB4F6` |
| Inscription manuelle | `/register/` |
| Accueil | `/` |
| Admin | `/admin/` |

## Notes Importantes

- Les QR codes pointent vers l'URL complète avec le paramètre `code`
- Le code est toujours en MAJUSCULES
- Le paramètre `?code=` pré-remplit le formulaire
- Pas besoin de modifier les librairies
- Les codes peuvent avoir plusieurs QR codes (code unique par librairie)
- Les QR codes sont statiques (pas d'expiration)

## Implémentation en Production

Pour un domaine réel (exemple: `monecole.dz`):

Changer l'URL du QR code de:
```
http://localhost:8000/register/?code=LIB4F6
```

À:
```
https://monecole.dz/register/?code=LIB4F6
```

Les QR codes se régénérent automatiquement avec la bonne URL!

## Raccourcissement d'URL (Optionnel)

Vous pouvez utiliser un service d'URL courte pour plus de portabilité:

```
Original: http://monecole.dz/register/?code=LIB4F6
Court: https://qr.co/lib4f6
```

Puis générer un QR code du lien court.

## Résumé

**Pour un élève:**
1. Scan QR → Formulaire pré-rempli → Inscription immédiate

**Pour une librairie:**
1. Voir QR codes → Télécharger → Imprimer → Afficher

**Pour l'admin:**
1. Créer librairie → QR codes générés auto → Librairie les utilise

**C'est ça!** 🎉
