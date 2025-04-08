# ThriveFlow API

ThriveFlow est une API complète de gestion de projets et de productivité personnelle, intégrant l'IA pour la génération automatique de projets à partir d'idées.

## Fonctionnalités

- **Gestion de Projets** : Création, suivi et gestion de projets
- **Gestion des Tâches** : Organisation des tâches avec catégories et tags
- **Gestion Financière** : Suivi des dépenses et budgets
- **Gestion des Idées** : Stockage et organisation des idées
- **Génération IA de Projets** : Utilisation de Mixtral-8x7B pour transformer des idées en projets structurés
- **Suivi de la Motivation** : Citations inspirantes et objectifs personnels
- **Gestion des Ressources** : Suivi du temps et des niveaux d'énergie
- **Collaboration** : Gestion d'équipe et partage de fichiers

## Prérequis

- Python 3.11 ou supérieur
- PostgreSQL
- Carte graphique NVIDIA avec au moins 16 Go de VRAM (pour l'IA)
- Git

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/ThriveFlowAPI.git
cd ThriveFlowAPI
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement :
```bash
cp .env.example .env
```
Modifiez le fichier `.env` avec vos configurations :
```
DATABASE_URL=postgresql://username:password@localhost:5432/thriveflow
SECRET_KEY=votre_secret_key
JWT_SECRET_KEY=votre_jwt_secret_key
```

5. Initialisez la base de données :
```bash
flask db upgrade
```

## Utilisation de l'API

### Authentification

1. **Inscription**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "votre_nom",
    "email": "votre@email.com",
    "password": "votre_mot_de_passe"
  }'
```

2. **Connexion**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "votre@email.com",
    "password": "votre_mot_de_passe"
  }'
```

### Génération de Projets avec IA

Utilisez l'IA pour générer un projet structuré à partir d'une idée :

```bash
curl -X POST http://localhost:5000/api/generate-project \
  -H "Authorization: Bearer <votre_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "Créer une application mobile de suivi de fitness",
    "context": {
      "objectifs": ["Améliorer la santé des utilisateurs", "Créer une communauté active"],
      "contraintes": ["Budget limité", "Délai de 6 mois"]
    }
  }'
```

### Gestion des Projets

1. **Créer un projet manuellement**
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Authorization: Bearer <votre_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mon Projet",
    "description": "Description du projet",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }'
```

2. **Lister les projets**
```bash
curl -X GET http://localhost:5000/api/projects \
  -H "Authorization: Bearer <votre_token_jwt>"
```

### Gestion des Tâches

1. **Créer une tâche**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Authorization: Bearer <votre_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "title": "Ma Tâche",
    "description": "Description de la tâche",
    "due_date": "2024-02-01",
    "priority": 2
  }'
```

### Gestion Financière

1. **Ajouter une dépense**
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Authorization: Bearer <votre_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.50,
    "description": "Achat de matériel",
    "category": "Équipement",
    "date": "2024-01-15"
  }'
```

### Gestion des Idées

1. **Créer une idée**
```bash
curl -X POST http://localhost:5000/api/ideas \
  -H "Authorization: Bearer <votre_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mon Idée",
    "description": "Description détaillée de l'idée",
    "visibility": "private"
  }'
```

## Structure de la Base de Données

L'application utilise les tables suivantes :
- `users` : Utilisateurs
- `projects` : Projets
- `tasks` : Tâches
- `categories` : Catégories
- `tags` : Étiquettes
- `comments` : Commentaires
- `expenses` : Dépenses
- `budgets` : Budgets
- `ideas` : Idées
- `inspirational_quotes` : Citations inspirantes
- `daily_motivation` : Motivation quotidienne
- `user_goals` : Objectifs personnels
- `time_tracking` : Suivi du temps
- `energy_levels` : Niveaux d'énergie
- `team_members` : Membres d'équipe
- `shared_files` : Fichiers partagés
- `notifications` : Notifications

## Développement

Pour contribuer au projet :

1. Créez une branche pour votre fonctionnalité :
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

2. Committez vos changements :
```bash
git commit -m "Ajout de ma nouvelle fonctionnalité"
```

3. Poussez vers la branche :
```bash
git push origin feature/ma-nouvelle-fonctionnalite
```

4. Créez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.