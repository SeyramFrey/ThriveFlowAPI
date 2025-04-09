# ThriveFlowAPI

API de gestion de projets avec génération automatique de plans de projet via Mistral AI.

## À propos

ThriveFlowAPI est une application backend permettant aux utilisateurs de gérer leurs projets et activités, et d'utiliser l'IA pour générer automatiquement des plans de projet détaillés à partir d'une simple idée textuelle.

Principales fonctionnalités :
- Authentification des utilisateurs (inscription, connexion)
- Génération de projets via l'API Mistral AI
- Gestion des projets et de leurs activités
- Stockage des idées et association avec les projets générés

## Technologies utilisées

- **Backend** : Flask (Python)
- **Base de données** : PostgreSQL
- **ORM** : SQLAlchemy
- **Authentification** : JWT (JSON Web Tokens)
- **IA** : Mistral AI API
- **Documentation** : Markdown

## Prérequis

- Python 3.8+
- PostgreSQL
- Clé API Mistral AI

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/yourusername/ThriveFlowAPI.git
cd ThriveFlowAPI
```

2. Créez et activez un environnement virtuel :
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Créez un fichier `.env` à la racine du projet avec les variables suivantes :
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/thriveflow
JWT_SECRET_KEY=votre_clé_secrète_jwt
MISTRAL_API_KEY=votre_clé_api_mistral
```

5. Initialisez la base de données :
```bash
flask db init
flask db migrate
flask db upgrade
```

6. Lancez l'application :
```bash
flask run
```

L'API sera disponible à l'adresse http://localhost:5000

## Documentation API

La documentation complète de l'API est disponible dans le fichier [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## Flux de travail typique

1. **Inscription/Connexion** : L'utilisateur crée un compte ou se connecte pour obtenir un token JWT
2. **Génération de projet** : L'utilisateur soumet une idée à l'endpoint `/api/generate-project`
3. **Sauvegarde du projet** : Si l'utilisateur est satisfait du projet généré, il le sauvegarde via `/api/save-generated-project`
4. **Gestion du projet** : L'utilisateur peut alors gérer son projet et ses activités via les endpoints appropriés

## Structure du projet

```
ThriveFlowAPI/
├── app/                    # Code de l'application
│   ├── models/             # Modèles SQLAlchemy
│   ├── routes/             # Routes de l'API
│   ├── utils/              # Utilitaires et services
│   └── __init__.py         # Initialisation de l'application
├── migrations/             # Migrations de la base de données
├── .env                    # Variables d'environnement
├── .gitignore              # Fichiers à ignorer par Git
├── API_DOCUMENTATION.md    # Documentation détaillée de l'API
├── README.md               # Ce fichier
├── requirements.txt        # Dépendances Python
└── run.py                  # Point d'entrée de l'application
```

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.