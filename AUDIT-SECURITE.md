# Audit sécurité (OWASP) : MamiePull

> Branche : `audit-cyber-rgpd`
> Périmètre : API Django REST Framework (apps users, products, categories, favorites, news), configuration (`config/settings.py`), authentification JWT.
> Méthode : audit statique selon OWASP API Security Top 10 (2023) et OWASP Top 10 web. Aucune modification de code. Chaque finding est vérifié dans le code et assorti d'un scénario d'exploitation.

## Verdict

**Écarts à corriger avant prod.** Un finding bloquant confirmé (escalade de privilèges `is_staff` via `PUT /api/auth/me/`, vérifié en lecture du code) et plusieurs écarts majeurs de configuration et d'authentification.

Récapitulatif : **1 bloquant, 4 majeurs, 3 mineurs.**

---

## Findings

### [bloquant] Escalade de privilèges : `is_staff` modifiable par l'utilisateur via PUT /api/auth/me/ (OWASP API3/API6 — Broken Object Property Level Authorization)

- **Fichier** : `backend/users/serializers.py:11-12` ; `backend/users/api_views.py:23-28`
- **Faille** : `UserSerializer` liste `is_staff` dans `fields` et ne met en `read_only_fields` que `["id"]` (confirmé : `fields = ["id","username","email","first_name","last_name","is_staff"]`, `read_only_fields = ["id"]`). `CurrentUserAPIView.put()` fait `UserSerializer(request.user, data=request.data, partial=True)` puis `save()`. Le champ de rôle `is_staff` est donc accepté en écriture par le endpoint self-service.
- **Scénario d'exploitation** : un utilisateur authentifié standard envoie `PUT /api/auth/me/` avec `{"is_staff": true}` et devient staff. `is_staff=True` ouvre l'admin Django (`admin/` dans `config/urls.py`) et débloque toutes les écritures produits/catégories (dont la garde repose sur `request.user.is_staff`). Impact : compromission complète du back-office et accès à toutes les données personnelles de tous les comptes.
- **Correction attendue** : retirer `is_staff` de `fields` du `UserSerializer` ou le passer en `read_only_fields`. Un champ de rôle ne doit jamais être modifiable en self-service. Idéalement, séparer un serializer de lecture d'un serializer d'update self-service restreint à `username/first_name/last_name`.

### [majeur] DEBUG=True par défaut, activable en prod par simple absence de variable (OWASP API8 — Security Misconfiguration)

- **Fichier** : `backend/config/settings.py:15`
- **Faille** : `DEBUG = config("DEBUG", default=True, cast=bool)`. Le défaut est `True`. Si la variable d'environnement `DEBUG` n'est pas positionnée (ou mal typée) sur le serveur, Django tourne en mode debug. Le `.env.example` ne fournit pas de ligne `DEBUG`, donc un déploiement calqué dessus démarre en debug.
- **Scénario d'exploitation** : un attaquant provoque une exception non gérée (ex : POST produit avec un body non JSON, voir finding parsing). Django renvoie la page de debug complète : traceback, extraits de code, variables locales, et la liste des settings avec `SECRET_KEY`, identifiants DB (`DB_PASSWORD`), CORS. Avec `SECRET_KEY` divulguée il peut forger des tokens et pivoter en compromission totale.
- **Correction attendue** : `default=False`. Positionner explicitement `DEBUG=False` en prod et documenter la variable dans `.env.example`.

### [majeur] Aucun throttling : brute force du login et énumération de comptes possibles (OWASP API2 — Broken Authentication)

- **Fichier** : `backend/config/settings.py:138-149` (REST_FRAMEWORK sans `DEFAULT_THROTTLE_CLASSES`/`RATES`) ; `backend/config/urls.py:15` ; `backend/users/api_urls.py:8-11`
- **Faille** : `REST_FRAMEWORK` ne définit ni `DEFAULT_THROTTLE_CLASSES` ni `DEFAULT_THROTTLE_RATES`. Aucune vue (login `TokenObtainPairView`, register, refresh) n'applique de throttle. SimpleJWT ne limite pas le débit nativement.
- **Scénario d'exploitation** : un attaquant lance un bruteforce automatisé sur `POST /api/token/` ou `/api/auth/login/` avec l'email de la créatrice (connu/deviné, cf finding suivant) et une liste de mots de passe, sans jamais être ralenti. Corollaire d'énumération : `POST /api/auth/register/` renvoie une erreur distincte quand l'email est déjà pris (contrainte `unique=True`), ce qui confirme l'existence d'un compte. Impact : prise de contrôle du compte staff ou cartographie des comptes.
- **Correction attendue** : activer `AnonRateThrottle`/`ScopedRateThrottle` avec un `throttle_scope` dédié sur les endpoints d'authentification (ex 5/min sur login et register), messages d'erreur register génériques.

### [majeur] Email de la créatrice exposé dans les réponses produits publiques (OWASP API3 — Excessive Data Exposure)

- **Fichier** : `backend/products/serializers.py:10,24` ; `backend/products/views.py:15` (`@permission_classes([AllowAny])` sur GET) ; `backend/favorites/serializers.py:8` (serializer dupliqué)
- **Faille** : `ProductSerializer` expose `created_by_name = CharField(source="created_by.email")`. Le GET produits est public (`AllowAny`). Chaque produit renvoie donc l'email du staff qui l'a créé.
- **Scénario d'exploitation** : un visiteur anonyme appelle `GET /api/products/` et récupère dans chaque objet `created_by_name` l'adresse email personnelle de la créatrice. Impact : fuite de donnée personnelle (recoupe l'audit RGPD), collecte pour phishing/spam, et aide au bruteforce du login (l'email est le `USERNAME_FIELD`).
- **Correction attendue** : retirer `created_by_name` (email) du serializer public, ou exposer un nom d'affichage non sensible. Ne jamais exposer l'email via un endpoint `AllowAny`.

### [majeur] Swagger/OpenAPI et ReDoc exposés sans authentification (OWASP API8 — Security Misconfiguration)

- **Fichier** : `backend/config/urls.py:26-38` ; `backend/config/settings.py:155` (`SERVE_INCLUDE_SCHEMA: False`)
- **Faille** : `/api/schema/`, `/api/schema/swagger-ui/` et `/api/schema/redoc/` sont montés sans `permission_classes` restrictif. Les vues drf-spectacular sont servies publiquement par défaut. Le hook `exclude_non_api_paths` masque seulement admin/token/auth du schéma, il ne restreint pas l'accès.
- **Scénario d'exploitation** : un attaquant ouvre `/api/schema/swagger-ui/` et obtient la cartographie complète des endpoints produits, catégories, favorites (chemins, méthodes, formes de payload), ce qui accélère toute autre attaque. À confirmer selon la config runtime, mais par défaut ces vues sont accessibles anonymement.
- **Correction attendue** : restreindre l'accès à la doc (auth requise ou `SERVE_PERMISSIONS` staff-only) en prod, ou ne pas exposer Swagger en production.

### [mineur] Contrôle d'accès catégories : `is_staff` testé sans vérifier `is_authenticated` (OWASP API5 — Broken Function Level Authorization)

- **Fichier** : `backend/categories/views.py:15,24,29,34`
- **Faille** : la vue est `@permission_classes([AllowAny])`. Pour POST/PUT/DELETE elle teste seulement `if not request.user.is_staff`. Un anonyme a `request.user = AnonymousUser` dont `is_staff` vaut `False`, donc l'accès est refusé (403) : comportement final correct, mais logique fragile et différente de `products/views.py` (qui teste `is_authenticated` puis `is_staff`). Un futur refactor casse facilement cette barrière implicite.
- **Scénario d'exploitation** : pas d'exploitation directe aujourd'hui. Risque de régression si la condition est modifiée. Défaut de robustesse.
- **Correction attendue** : uniformiser avec `permission_classes([IsAdminUser])` ou `IsAuthenticated` + test explicite, plutôt que `AllowAny` + garde manuelle.

### [mineur] `json.loads(request.body)` non protégé : 500 sur body malformé (OWASP API8 — robustesse)

- **Fichier** : `backend/products/views.py:33,37` ; `backend/categories/views.py:60,70`
- **Faille** : `body = json.loads(request.body)` sans try/except. Un corps non JSON lève `json.JSONDecodeError` non capturée → 500. Couplé à DEBUG=True, expose un traceback.
- **Scénario d'exploitation** : un staff (ou l'attaquant après compromission) envoie `POST /api/products/` avec un body non JSON. En debug, la stack complète s'affiche. Sans debug, déni de robustesse mineur. Impact limité car ces endpoints exigent staff.
- **Correction attendue** : encadrer le parsing par un try/except renvoyant 400, ou utiliser les serializers DRF pour valider l'entrée.

### [mineur] Logout non révocateur : blacklist JWT inopérante (OWASP API2 — Broken Authentication)

- **Fichier** : `backend/users/api_views.py:31-36` ; `backend/config/settings.py:161-167`
- **Faille** : `LogoutAPIView` renvoie seulement un message, sans blacklister le refresh token. `SIMPLE_JWT` active `ROTATE_REFRESH_TOKENS` et `BLACKLIST_AFTER_ROTATION`, mais `rest_framework_simplejwt.token_blacklist` n'est pas dans `INSTALLED_APPS` : la blacklist est inopérante (tables absentes).
- **Scénario d'exploitation** : un token volé (XSS front, fuite de logs, poste partagé) reste valide jusqu'à expiration naturelle malgré le logout (access 60 min, refresh 1 jour renouvelable). L'utilisateur croit à tort s'être déconnecté.
- **Correction attendue** : ajouter `rest_framework_simplejwt.token_blacklist` aux INSTALLED_APPS, migrer, et blacklister le refresh token dans `LogoutAPIView`.

---

## Surface d'attaque (endpoints audités)

| Route | Méthodes | Rôle/scope attendu | Statut protection |
|---|---|---|---|
| `POST /api/token/`, `/api/auth/login/` | POST | public (auth) | OK fonctionnel, SANS throttle (majeur) |
| `POST /api/token/refresh/`, `/api/auth/token/refresh/` | POST | token valide | OK, sans throttle |
| `POST /api/auth/register/` | POST | public | Ouvert (normal) ; énumération d'email possible (majeur) |
| `GET/PUT /api/auth/me/` | GET/PUT | user authentifié, ses données | **BLOQUANT** : `is_staff` modifiable (escalade) |
| `POST /api/auth/logout/` | POST | authentifié | OK mais ne révoque rien (mineur) |
| `GET /api/products/` (+ `/id/`, `/category/id/`) | GET | public | OK public ; expose email créatrice (majeur) |
| `POST/PUT/DELETE /api/products/...` | écriture | staff | OK : `is_authenticated` + `is_staff` vérifiés |
| `GET /api/categories/` (+ `/id/`) | GET | public | OK public |
| `POST/PUT/DELETE /api/categories/...` | écriture | staff | Fonctionnellement OK, logique fragile (mineur) |
| `GET/POST/DELETE /api/favorites/` (+ `/product_id/`) | GET/POST/DELETE | user, SES favoris | OK : cloisonné par `user=request.user`, pas de BOLA |
| `/admin/` | toutes | superuser | Django admin standard |
| `/api/schema/`, `/swagger-ui/`, `/redoc/` | GET | devrait être privé | Exposé publiquement par défaut (majeur) |
| news | aucune | — | Pas d'urls ni de vues : aucune surface API |

---

## Points sûrs notables (à ne pas régresser)

- **Cloisonnement des favoris correct** : `get_favorites`, `add_favorite`, `remove_favorite` filtrent tous sur `user=request.user`. Aucun IDOR/BOLA. `unique_together` empêche les doublons.
- **Permission par défaut DRF saine** : `DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]` (settings.py:139). Les endpoints publics sont explicitement ouverts, pas ouverts par défaut.
- **Pas de mass assignment via `__all__`** : `ProductSerializer` et `UserSerializer` listent des `fields` explicites. `created_by` et `id` en `read_only_fields`. `UserSerializer` n'expose pas `password`. (Le trou est le champ `is_staff`, traité en bloquant ci-dessus.)
- **Politique de mot de passe robuste** : min 9 + majuscule + minuscule + chiffre + caractère spécial (settings.py:102-121, validators.py).
- **Pas de SQL brut** : aucune occurrence de `.raw()`, `.extra()`, `cursor()`, f-string SQL. ORM Django uniquement, pas d'injection SQL.
- **`SECRET_KEY` chargée depuis l'environnement sans défaut** (settings.py:13) : pas de clé « django-insecure » commitée.
- **`.env` non versionné** : seuls `.env.example` (backend et frontend) sont suivis par git, sans secret réel (confirmé `git ls-files`). Attention : aucun `.gitignore` n'existe (voir audit RGPD), donc un `git add .` commiterait un vrai `.env`.
- **CORS restreint** : `CORS_ALLOWED_ORIGINS` limité à localhost:3000, pas de `CORS_ALLOW_ALL_ORIGINS=True`. `CSRF_TRUSTED_ORIGINS` défini. `ALLOWED_HOSTS` explicite.
- **App news sans surface** : modèle présent mais ni vue ni URL exposées.

---

## Non vérifiable statiquement (à traiter en DAST / pentest / revue infra)

- Valeur réelle de `SECRET_KEY`, `DEBUG`, `DB_PASSWORD` en environnement de prod (dépend du `.env` non fourni).
- Accès effectif à Swagger/Redoc sans auth (dépend de la version drf-spectacular et de la config runtime).
- Validation des uploads d'images (`Product.image`, `upload_to="products/"`) : type, taille, contenu réel, chemin. Non contrôlée dans le code (risque path traversal/upload malveillant faible car écriture réservée au staff).
- En-têtes de sécurité HTTP / HTTPS : `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, HSTS absents de settings.py, à ajouter pour la prod.

---

## Top 3 à traiter en priorité

1. **[bloquant] Escalade `is_staff` via `PUT /api/auth/me/`** (API3/API6) — un user standard devient admin.
2. **DEBUG=True par défaut** (API8) — expose `SECRET_KEY` et identifiants DB via traceback.
3. **Aucun throttling** (API2) — bruteforce et énumération de comptes libres sur login/register.

Flux le plus exposé : l'authentification / `PUT /api/auth/me/`, dont la compromission ou l'abus débloque tout le back-office.
