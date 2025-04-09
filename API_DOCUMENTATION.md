# ThriveFlowAPI - Documentation

Ce document décrit en détail comment utiliser l'API ThriveFlow pour gérer des projets, générer automatiquement des plans de projet avec l'IA et gérer les activités associées.

## Table des matières

1. [Authentification](#1-authentification)
   - [Inscription](#inscription)
   - [Connexion](#connexion)
   - [Utilisation des tokens](#utilisation-des-tokens)
2. [Génération de projets avec l'IA](#2-génération-de-projets-avec-lia)
   - [Générer un projet](#générer-un-projet)
   - [Sauvegarder un projet généré](#sauvegarder-un-projet-généré)
3. [Gestion des projets](#3-gestion-des-projets)
   - [Récupérer tous les projets](#récupérer-tous-les-projets)
   - [Récupérer un projet spécifique](#récupérer-un-projet-spécifique)
   - [Créer un projet manuellement](#créer-un-projet-manuellement)
   - [Mettre à jour un projet](#mettre-à-jour-un-projet)
   - [Supprimer un projet](#supprimer-un-projet)
4. [Gestion des activités](#4-gestion-des-activités)
   - [Créer une activité](#créer-une-activité)
   - [Récupérer une activité](#récupérer-une-activité)

## 1. Authentification

### Inscription

Permet de créer un nouveau compte utilisateur.

**Endpoint** : `POST /api/auth/register`

**Corps de la requête** :
```json
{
  "username": "votre_nom_utilisateur",
  "email": "votre_email@exemple.com",
  "password": "votre_mot_de_passe"
}
```

**Réponse en cas de succès** (201 Created) :
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "votre_nom_utilisateur",
    "email": "votre_email@exemple.com",
    "created_at": "2025-04-09T21:14:18.336285",
    "updated_at": "2025-04-09T21:14:18.336290"
  }
}
```

### Connexion

Permet de se connecter et d'obtenir un token d'authentification.

**Endpoint** : `POST /api/auth/login`

**Corps de la requête** :
```json
{
  "username": "votre_nom_utilisateur",
  "password": "votre_mot_de_passe"
}
```

**Réponse en cas de succès** (200 OK) :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "votre_nom_utilisateur",
    "email": "votre_email@exemple.com",
    "created_at": "2025-04-09T21:14:18.336285",
    "updated_at": "2025-04-09T21:14:18.336290"
  }
}
```

### Utilisation des tokens

Pour toutes les requêtes authentifiées, utilisez le token d'accès dans l'en-tête de la requête :

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 2. Génération de projets avec l'IA

### Générer un projet

Génère un plan de projet basé sur une idée fournie en utilisant l'IA de Mistral.

**Endpoint** : `POST /api/generate-project`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "idea": "Je voudrais créer une application mobile de suivi de budget personnel avec des catégories personnalisables et des notifications intelligentes."
}
```

**Réponse en cas de succès** (200 OK) :
```json
{
  "success": true,
  "data": {
    "raw_response": {
      "project": {
        "name": "MyBudgetApp",
        "description": "Une application mobile de suivi de budget personnel avec des catégories personnalisables...",
        "competitiveAdvantage": "Une interface intuitive, des fonctionnalités uniques...",
        "estimatedBudget": 12000,
        "estimatedDuration": "3 mois",
        "keyPoints": ["Suivi de budget personnel", "Catégories personnalisables", "Notifications intelligentes"]
      },
      "activities": [
        {
          "name": "Étude de marché",
          "description": "Analyser les besoins des utilisateurs et la concurrence existante.",
          "startDate": "2023-02-20",
          "endDate": "2023-02-25",
          "estimatedDailyTime": "3h/day",
          "estimatedDuration": "5 days",
          "estimatedCost": 0,
          "status": "not started",
          "priority": "high",
          "dependencies": [],
          "resources": {
            "human": ["Analyste de marché"],
            "material": [],
            "tools": ["Google Forms", "Typeform", "Excel"]
          }
        },
        // Autres activités...
      ],
      "projectSummary": {
        "totalDuration": "3 mois",
        "totalCost": 12000,
        "criticalPoints": ["Validation des hypothèses après l'étude de marché", "Stabilité de l'application lors des tests utilisateurs"]
      }
    },
    "status": "success",
    "timestamp": "2025-04-09T23:34:16.343264"
  },
  "idea_id": 1
}
```

### Sauvegarder un projet généré

Permet de sauvegarder un projet généré par l'IA dans la base de données.

**Endpoint** : `POST /api/save-generated-project`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "mistral_response": {
    "project": { ... },
    "activities": [ ... ],
    "projectSummary": { ... }
  },
  "idea_id": 1
}
```

**Réponse en cas de succès** (201 Created) :
```json
{
  "success": true,
  "message": "Project and activities saved successfully",
  "project": {
    "id": 2,
    "name": "MyBudgetApp",
    "description": "Une application mobile de suivi de budget personnel...",
    "status": "planning",
    "activities_count": 5
  }
}
```

## 3. Gestion des projets

### Récupérer tous les projets

Récupère tous les projets de l'utilisateur authentifié.

**Endpoint** : `GET /api/projects`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
```

**Réponse en cas de succès** (200 OK) :
```json
[
  {
    "id": 1,
    "name": "MyBudgetApp",
    "description": "Une application mobile de suivi de budget personnel...",
    "status": "planning",
    "start_date": "2025-04-09",
    "end_date": "2025-05-09",
    "estimated_budget": 12000,
    "estimated_duration": "3 mois",
    "competitive_advantage": "Une interface intuitive...",
    "key_points": { ... },
    "created_at": "2025-04-09T21:17:26.974418",
    "activities": [ ... ],
    "idea": { ... }
  }
]
```

### Récupérer un projet spécifique

Récupère les détails d'un projet spécifique.

**Endpoint** : `GET /api/projects/{project_id}`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
```

**Réponse en cas de succès** (200 OK) :
```json
{
  "id": 1,
  "name": "MyBudgetApp",
  "description": "Une application mobile de suivi de budget personnel...",
  "status": "planning",
  "start_date": "2025-04-09",
  "end_date": "2025-05-09",
  "estimated_budget": 12000,
  "estimated_duration": "3 mois",
  "competitive_advantage": "Une interface intuitive...",
  "key_points": { ... },
  "created_at": "2025-04-09T21:17:26.974418",
  "updated_at": "2025-04-09T21:17:26.974418",
  "activities": [
    {
      "id": 1,
      "name": "Étude de marché",
      "description": "Analyser les besoins des utilisateurs...",
      "status": "not started",
      "start_date": "2025-04-13",
      "end_date": "2025-04-18",
      "estimated_duration": "5 days",
      "estimated_cost": 0,
      "priority": "high"
    },
    // Autres activités...
  ],
  "idea": {
    "id": 1,
    "title": "Idée: Je voudrais créer une application mobile de suivi de budget...",
    "description": "Je voudrais créer une application mobile de suivi de budget personnel..."
  }
}
```

### Créer un projet manuellement

Crée un nouveau projet manuellement.

**Endpoint** : `POST /api/projects`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "name": "Nom du projet",
  "description": "Description du projet",
  "start_date": "2025-04-10",
  "end_date": "2025-05-10",
  "status": "planning",
  "estimated_budget": 10000,
  "estimated_duration": "1 mois",
  "competitive_advantage": "Avantage compétitif du projet",
  "key_points": {
    "points": ["Point clé 1", "Point clé 2"]
  }
}
```

**Réponse en cas de succès** (201 Created) :
```json
{
  "message": "Project created successfully",
  "project": {
    "id": 3,
    "name": "Nom du projet",
    "description": "Description du projet",
    "status": "planning",
    "created_at": "2025-04-10T10:00:00.000000"
  }
}
```

### Mettre à jour un projet

Met à jour un projet existant.

**Endpoint** : `PUT /api/projects/{project_id}`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "name": "Nouveau nom du projet",
  "description": "Nouvelle description",
  "status": "active"
}
```

**Réponse en cas de succès** (200 OK) :
```json
{
  "message": "Project updated successfully",
  "project": {
    "id": 1,
    "name": "Nouveau nom du projet",
    "description": "Nouvelle description",
    "start_date": "2025-04-09",
    "end_date": "2025-05-09",
    "status": "active"
  }
}
```

### Supprimer un projet

Supprime un projet existant.

**Endpoint** : `DELETE /api/projects/{project_id}`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
```

**Réponse en cas de succès** (200 OK) :
```json
{
  "message": "Project deleted successfully"
}
```

## 4. Gestion des activités

### Créer une activité

Crée une nouvelle activité associée à un projet.

**Endpoint** : `POST /api/activities`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
Content-Type: application/json
```

**Corps de la requête** :
```json
{
  "name": "Nom de l'activité",
  "description": "Description de l'activité",
  "project_id": 1,
  "start_date": "2025-04-10",
  "end_date": "2025-04-15",
  "estimated_daily_time": "2 heures",
  "estimated_duration": "5 jours",
  "estimated_cost": 500,
  "status": "not started",
  "priority": "medium",
  "dependencies": [],
  "resources": {
    "human": ["Développeur"],
    "material": ["Ordinateur"],
    "tools": ["VS Code", "Git"]
  }
}
```

**Réponse en cas de succès** (201 Created) :
```json
{
  "message": "Activity created successfully",
  "activity": {
    "id": 6,
    "name": "Nom de l'activité",
    "description": "Description de l'activité",
    "project_id": 1,
    "status": "not started",
    "created_at": "2025-04-10T10:00:00.000000"
  }
}
```

### Récupérer une activité

Récupère les détails d'une activité spécifique.

**Endpoint** : `GET /api/activities/{activity_id}`

**En-têtes requis** :
```
Authorization: Bearer votre_token_access
```

**Réponse en cas de succès** (200 OK) :
```json
{
  "id": 1,
  "name": "Étude de marché",
  "description": "Analyser les besoins des utilisateurs...",
  "project_id": 1,
  "start_date": "2025-04-13",
  "end_date": "2025-04-18",
  "estimated_daily_time": "3h/day",
  "estimated_duration": "5 days",
  "estimated_cost": 0,
  "status": "not started",
  "priority": "high",
  "dependencies": [],
  "resources": {
    "human": ["Analyste de marché"],
    "material": [],
    "tools": ["Google Forms", "Typeform", "Excel"]
  },
  "created_at": "2025-04-09T21:20:16.446377",
  "updated_at": "2025-04-09T21:20:16.446377"
}
```

## Format des données

### Projet

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique du projet |
| user_id | Integer | ID de l'utilisateur propriétaire |
| name | String | Nom du projet |
| description | String | Description détaillée |
| start_date | Date | Date de début (YYYY-MM-DD) |
| end_date | Date | Date de fin prévue (YYYY-MM-DD) |
| status | String | État du projet (planning, active, completed, on_hold) |
| estimated_budget | Float | Budget estimé |
| estimated_duration | String | Durée estimée |
| competitive_advantage | String | Avantage compétitif |
| key_points | JSON | Points clés du projet |
| created_at | DateTime | Date de création |
| updated_at | DateTime | Date de dernière mise à jour |

### Activité

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique de l'activité |
| user_id | Integer | ID de l'utilisateur propriétaire |
| project_id | Integer | ID du projet associé |
| name | String | Nom de l'activité |
| description | String | Description détaillée |
| start_date | Date | Date de début (YYYY-MM-DD) |
| end_date | Date | Date de fin prévue (YYYY-MM-DD) |
| estimated_daily_time | String | Temps quotidien estimé |
| estimated_duration | String | Durée estimée |
| estimated_cost | Float | Coût estimé |
| status | String | État (not started, in progress, completed, delayed) |
| priority | String | Priorité (low, medium, high) |
| dependencies | JSON | Dépendances avec d'autres activités |
| resources | JSON | Ressources nécessaires (humaines, matérielles, outils) |
| created_at | DateTime | Date de création |
| updated_at | DateTime | Date de dernière mise à jour | 