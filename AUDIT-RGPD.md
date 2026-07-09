# Audit RGPD : MamiePull

> Branche : `audit-cyber-rgpd`
> Périmètre : modèles de données (`backend/*/models.py`), serializers, vues, configuration (`config/settings.py`), points de log, sous-traitants.
> Rôle du projet : la créatrice exploitante est **responsable de traitement** ; la développeuse fournit les **moyens techniques** (projet RNCP individuel). L'audit vérifie que les moyens techniques des obligations existent dans le code. Aucune modification de code.
> Ce document est un audit technique de conformité, **pas un avis juridique**. Les décisions marquées « responsable / DPO » relèvent de la responsable de traitement.

## Verdict

**Écarts à corriger avant prod (dont deux points bloquants de sécurité, art. 32).**

Récapitulatif : **2 bloquants, 4 majeurs, 4 mineurs.**

---

## Findings

### [bloquant] Escalade de privilèges via PUT /api/auth/me/ (is_staff modifiable par l'utilisateur)

- **Fichier** : `backend/users/serializers.py:11-12` ; `backend/users/api_views.py:23-28`
- **Risque** : `UserSerializer` liste `is_staff` dans `fields` et ne met en `read_only_fields` que `["id"]`. `CurrentUserAPIView.put()` fait `UserSerializer(request.user, data=request.data, partial=True)` puis `save()`. Un utilisateur authentifié standard peut envoyer `{"is_staff": true}` sur `/api/auth/me/` et devenir administrateur. `is_staff=True` ouvre l'admin Django (`admin/` dans `config/urls.py`) et donc l'accès en lecture/écriture à TOUTES les données personnelles de tous les comptes (email, nom, prénom, favoris). Défaut de sécurité du traitement, **art. 32** (confidentialité et contrôle d'accès), avec exposition potentielle de toute la base. Vérifié dans le code.
- **Qui agit** : sous-traitant (moyens techniques / développeuse).
- **Correction attendue** : retirer `is_staff` de `fields` du `UserSerializer` (ou le passer en `read_only_fields`). Un champ de rôle ne doit jamais être modifiable en self-service.

### [bloquant] Absence de .gitignore : risque de commit du fichier .env (secrets)

- **Fichier** : racine du repo (aucun `.gitignore`, confirmé) ; `.env.example:9` ; `docker-compose.yml:4-9,21-26`
- **Risque** : le dépôt ne contient aucun `.gitignore` (ni racine, ni backend). `SECRET_KEY`, `DB_PASSWORD`, `DB_USER`, `DB_NAME` sont lus depuis un `.env` non versionné (`config()` dans settings.py, `env_file: .env` dans docker-compose). Actuellement aucun `.env` réel n'est tracké (seuls `.env.example` et `frontend/.env.example` le sont, avec placeholders), donc pas de fuite constatée. Mais sans `.gitignore`, un `git add .` commitera le `.env` réel (SECRET_KEY servant à signer les JWT, mot de passe PostgreSQL). Un `SECRET_KEY` exposé permet de forger des tokens et d'accéder aux comptes, **art. 32**.
- **Qui agit** : sous-traitant (développeuse).
- **Correction attendue** : ajouter un `.gitignore` excluant `.env`, `*/.env`, `.env.*` (sauf `.env.example`) à la racine, et vérifier l'historique (`git log --all -- .env`) pour s'assurer qu'aucun secret n'a déjà été commité.

### [majeur] DEBUG=True par défaut : pages d'erreur exposant des données

- **Fichier** : `backend/config/settings.py:15`
- **Risque** : `DEBUG = config("DEBUG", default=True, cast=bool)`. Le défaut est `True`. Si la variable `DEBUG` n'est pas explicitement passée à `False` en production, Django affiche les pages d'erreur détaillées (traceback, variables locales dont valeurs de champs email/nom, extraits de requêtes SQL, config). Exposition de données personnelles et de configuration, **art. 32**. `docker-compose.yml` passe `DEBUG=${DEBUG}` sans valeur imposée.
- **Qui agit** : sous-traitant (développeuse) + responsable (validation de la config de prod).
- **Correction attendue** : forcer `DEBUG=False` en production, et changer le défaut du code à `False`.

### [majeur] Email de l'administratrice exposé publiquement dans l'API produits

- **Fichier** : `backend/products/serializers.py:10,14-25` ; `backend/products/views.py:15,24-31,47-67` ; `backend/favorites/serializers.py:8` (dupliqué)
- **Risque** : `ProductSerializer` expose `created_by_name = created_by.email` et `created_by` (id). L'endpoint `products_api` est en `@permission_classes([AllowAny])` pour les GET. Tout visiteur anonyme récupère l'adresse email de la créatrice/administratrice dans chaque réponse produit. Donnée personnelle de la responsable diffusée sans nécessité côté vitrine publique, contraire à la minimisation (**art. 5-1-c**) et exposant l'email à la collecte automatisée (spam, phishing).
- **Qui agit** : sous-traitant (développeuse) ; arbitrage finalité par le responsable.
- **Correction attendue** : retirer `created_by_name`/`created_by.email` des réponses publiques, ou ne l'exposer qu'aux utilisateurs staff.

### [majeur] Aucun moyen technique d'effacement/anonymisation ni de purge (art. 17, 5-1-e)

- **Fichier** : `backend/users/api_views.py` (pas de méthode DELETE sur `CurrentUserAPIView`) ; `backend/users/api_urls.py:12` ; absence de commande de purge
- **Risque** : aucun endpoint ne permet à un utilisateur de supprimer son compte (`CurrentUserAPIView` ne gère que GET et PUT). Aucune commande de purge des comptes inactifs, aucune durée de conservation implémentée. Le droit à l'effacement (**art. 17**) et la limitation de conservation (**art. 5-1-e**) ne sont couverts que par l'admin Django (suppression manuelle par la responsable), moyen partiel côté responsable mais pas un mécanisme technique dédié. Bon point : `Favorite` a `on_delete=CASCADE` sur user (la suppression d'un compte efface ses favoris). Vérifié dans le code.
- **Qui agit** : responsable (définir durées de conservation et politique d'effacement) ; sous-traitant (implémenter endpoint de suppression de compte + éventuelle commande de purge).
- **Correction attendue** : ajouter un endpoint DELETE self-service sur `/me/` ou documenter la procédure d'effacement via l'admin ; définir avec la responsable une durée de conservation des comptes/favoris inactifs.

### [majeur] Aucun throttling sur l'authentification : risque de sécurité des accès (art. 32)

- **Fichier** : `backend/config/settings.py:138-149` (REST_FRAMEWORK sans throttle) ; `backend/users/api_urls.py:8-11`
- **Risque** : aucun `DEFAULT_THROTTLE_CLASSES`/`RATES`, aucun throttle sur login/register/refresh. Le bruteforce du compte admin et l'énumération de comptes (l'email étant unique) sont possibles sans limite. Comme `is_staff` donne accès à toutes les données personnelles, un accès non autorisé au compte staff est un défaut de sécurité du traitement (**art. 32**). Recoupe l'audit sécurité.
- **Qui agit** : sous-traitant (développeuse).
- **Correction attendue** : activer un throttling DRF (ex 5/min) sur les endpoints d'authentification et rendre les erreurs de register génériques.

### [mineur] Aucun endpoint de portabilité / export des données (art. 20)

- **Fichier** : `backend/users/api_views.py` ; `backend/favorites/views.py`
- **Risque** : pas de moyen technique d'export structuré des données d'un utilisateur (identité + favoris) au sens de la portabilité (**art. 20**). `GET /me/` renvoie l'identité et `GET /api/favorites/` renvoie les favoris scopés au user, mais il n'y a pas d'export consolidé. Volume faible, gravité mineure ; la réponse peut passer par l'admin/responsable.
- **Qui agit** : responsable (procédure) ; sous-traitant (option d'export si demandé).
- **Correction attendue** : prévoir une procédure d'export (même manuelle) à documenter dans le registre.

### [mineur] JWT d'accès de 60 min, refresh 1 jour, logout non invalidant

- **Fichier** : `backend/config/settings.py:161-167` ; `backend/users/api_views.py:31-36`
- **Risque** : `LogoutAPIView` renvoie seulement un message, sans blacklister le refresh token (l'app `token_blacklist` de SimpleJWT n'est pas dans INSTALLED_APPS, donc la blacklist configurée n'est pas effective). Un token volé reste valable jusqu'à expiration malgré le logout. Impact sécurité modéré (**art. 32**), pas de fuite directe.
- **Qui agit** : sous-traitant (développeuse).
- **Correction attendue** : ajouter `rest_framework_simplejwt.token_blacklist` à INSTALLED_APPS et blacklister le refresh au logout, ou assumer explicitement le choix (durées courtes).

### [mineur] Champ « message de contact » non implémenté : point de vigilance futur

- **Fichier** : `frontend/src/pages/ProductDetail.vue:126-134` (bouton `disabled`) ; `README.md:27,87`
- **Risque** : le bouton « Nous contacter pour ce modèle » est actuellement `disabled` et non branché ; aucun formulaire de contact, aucun modèle de message, aucun envoi d'email (grep `mail`/`send_mail` : aucun résultat). AUCUNE donnée de contact n'est collectée à ce jour, et aucun mailer sous-traitant n'existe. Point de vigilance : dès qu'un champ libre de message sera ajouté, il pourra capter des données non prévues, voire des données de mineurs (produits pour bébés/jeunes enfants) ou sensibles.
- **Qui agit** : responsable (base légale, mention d'information) ; sous-traitant (minimisation du futur formulaire).
- **Correction attendue** : lors de l'ajout du formulaire, prévoir base légale (intérêt légitime ou consentement), mention d'information, champ message non obligatoire avec avertissement de ne pas y saisir de données sensibles/d'enfant, et choix d'un mailer UE.

### [mineur] Seed de données avec mots de passe faibles en clair dans le code

- **Fichier** : `backend/users/management/commands/seed_data.py:13-33`
- **Risque** : comptes de démo (`alice@example.com`… `password123`) avec mots de passe en clair dans le code versionné. Adresses fictives `@example.com` (pas de vraie donnée personnelle), donc pas de fuite RGPD réelle, mais `password123` ne respecte pas `AUTH_PASSWORD_VALIDATORS` et ces comptes ne doivent jamais exister en prod.
- **Qui agit** : sous-traitant (développeuse).
- **Correction attendue** : réserver le seed au dev/test, ne jamais l'exécuter en prod.

---

## Points conformes vérifiés (à conserver)

- Mots de passe : `AbstractUser` + `create_user()` = hachage Django par défaut (PBKDF2), pas de stockage en clair. `RegisterSerializer` a `password` en `write_only`. `AUTH_PASSWORD_VALIDATORS` renforcés. Conforme **art. 32**.
- Cloisonnement des favoris : `get_favorites` filtre `Favorite.objects.filter(user=request.user)` ; add/remove scopés à `request.user`. Un utilisateur ne voit que ses favoris. Conforme.
- `UserSerializer` n'expose pas le mot de passe (absent des `fields`). Pas de `fields='__all__'` sur les données users.
- Aucun `print()`/`logging` de données personnelles ou de secrets trouvé dans le backend (grep vide).
- Swagger : `spectacular_hooks.exclude_non_api_paths` exclut `/admin/`, `/api/token/`, `/api/auth/` de la doc, donc les endpoints users (register, me) ne sont pas listés publiquement (l'accès à la doc elle-même reste à restreindre, cf audit sécurité).
- Secrets en variables d'environnement (`SECRET_KEY`, DB via `config()`), pas de valeur en dur dans settings.py.
- CORS en allowlist (`CORS_ALLOWED_ORIGINS` limité à localhost:3000), pas de `CORS_ALLOW_ALL_ORIGINS`.
- Schéma minimisé : Product, Category, News ne stockent pas de donnée personnelle de visiteur ; User ne contient que identité + email (pas de champ « au cas où »).

---

## Cartographie des données personnelles touchées

| Donnée | Finalité | Base de conservation (à définir par le responsable) | Destinataire |
|---|---|---|---|
| Email (User) | Identifiant de connexion, contact compte | Durée du compte ; purge inactifs à définir | Responsable (admin). **Exposée à tort en public** via ProductSerializer pour l'admin créatrice |
| Username / prénom / nom (User) | Identification de l'utilisateur | Durée du compte | Responsable (admin) |
| Mot de passe haché (User) | Authentification | Durée du compte | Personne (haché, non lisible) |
| date_joined / updated_at (User) | Traçabilité technique | Durée du compte | Responsable (admin) |
| Favoris (Favorite : user + product + date) | Préférences produits de l'utilisateur | Durée du compte (CASCADE à la suppression) | L'utilisateur lui-même (scoping OK) |
| is_staff (User) | Rôle admin | Durée du compte | Responsable ; **actuellement modifiable par l'utilisateur (bug bloquant)** |
| Message de contact | (non collecté à ce jour) | à définir avant activation | à définir (mailer futur) |

Sous-traitants ultérieurs (**art. 28**) : hébergeur à déterminer (déploiement Docker, localisation UE à confirmer) ; base PostgreSQL ; aucun mailer actuellement (formulaire de contact non actif). À contractualiser dès qu'un hébergeur/mailer est choisi.

---

## À porter au registre / à la doc du responsable

- **Finalités** : présenter les créations (vitrine), gérer les comptes visiteurs et leurs favoris, à terme gérer les contacts.
- **Catégories de personnes** : visiteurs/clients particuliers, la créatrice (admin).
- **Catégories de données** : identité (username, prénom, nom), email, mot de passe haché, favoris, horodatages.
- **Base légale** : comptes/favoris = à qualifier (exécution d'un service / intérêt légitime) ; futur formulaire de contact = consentement ou intérêt légitime.
- **Durées de conservation** : à définir (comptes actifs, purge des comptes inactifs, favoris) — actuellement aucune.
- **Droits des personnes** : accès/rectification via `/me/` (GET/PUT) ; effacement et portabilité à formaliser (aujourd'hui via admin uniquement).
- **Sécurité** : hachage mots de passe OK ; corriger l'escalade `is_staff`, forcer `DEBUG=False`, ajouter `.gitignore`, activer le throttling, invalider le JWT au logout.
- **Sous-traitants** : hébergeur (localisation UE), futur mailer — établir les contrats **art. 28** et vérifier l'absence de transfert hors UE (**art. 44+**).
- **Mineurs** : produits ciblant bébés/enfants ; aucune donnée d'enfant collectée aujourd'hui, à surveiller à l'activation du formulaire de contact.

---

## Top 3 à traiter en priorité

1. **[bloquant] Escalade `is_staff` via `PUT /me/`** donnant accès admin à toutes les données perso.
2. **[bloquant] Absence de `.gitignore`** exposant au commit du `.env` (SECRET_KEY, mot de passe DB).
3. **DEBUG=True par défaut** exposant des données via les pages d'erreur.

Donnée la plus à risque : **l'email de l'administratrice**, diffusé publiquement à tout visiteur anonyme dans chaque réponse de l'API produits.
