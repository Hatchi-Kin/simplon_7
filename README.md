# FastAPI SQLite Sales Analysis Project

Ce projet met en place une application FastAPI qui analyse les données de ventes d'une entreprise en utilisant SQLite. L'ensemble est conteneurisé avec Docker pour simplifier le déploiement.

## Architecture de l'Application

L'architecture repose sur deux conteneurs orchestrés par Docker Compose:
- Un conteneur **SQLite** qui fournit la base de données persistante
- Un conteneur **FastAPI** qui héberge l'application web et la logique métier

Le conteneur FastAPI attend que la base de données soit prête (via healthcheck) avant de démarrer. Lors de son initialisation, il charge automatiquement les données CSV dans la base SQLite. L'interface utilisateur est servie via des templates HTML rendus par FastAPI.

```sh
              +---------------------+
              |  Docker Compose     |
              +----------+----------+
                         |
              +----------v----------+
              |                     |
   +----------v---------+  +--------v-----------+
   |  SQLite Container  |  |  FastAPI Container |
   |  (Database)        |  |  (Web Server)      |
   +--------------------+  +--------------------+
            ^                        |
            |                        |
            |                +-------v---------+
            |                | Python Utilities |
            +----------------+ - Data Loading   |
                             | - SQL Queries    |
                             | - Plotting       |
                             +-----------------+
                                      |
                             +--------v--------+
                             | HTML Templates   |
                             +-----------------+
```
## Structure du Projet

```sh
simplon_7
|
├── docker-compose.yaml        # Configuration Docker Compose
├── README.md                  # Documentation du projet
|
├── app
│   ├── main.py                # Point d'entrée de l'application FastAPI
│   ├── requirements.txt       # Dépendances Python
│   ├── Dockerfile             # Configuration Docker pour l'application
│   │
│   ├── templates
│   │   └── analysis.html      # Template HTML pour l'affichage des résultats
│   │
│   └── utils
│       ├── data_loader.py     # Chargement des données CSV
│       ├── init_app.py        # Initialisation de la base de données
│       ├── plot_generator.py  # Génération de graphiques pour l'analyse
│       ├── routes.py          # Définition des routes API
│       └── sql_queries.py     # Requêtes SQL pour l'analyse des ventes
│
└── data
    ├── magasins.csv           # Données des magasins
    ├── produits.csv           # Données des produits
    ├── sales.db               # Base de données SQLite
    └── ventes.csv             # Données des ventes

```

# Diagramme Entité-Relation (ERD)
```sh
erDiagram
    ## "||" represents "one" and "o{" represents "many"
    ## So "||--o{" means "one-to-many" relationship
    PRODUITS ||--o{ VENTES : "sells (one product can be in many sales)"
    MAGASINS ||--o{ VENTES : "records (one store can have many sales)"
    
    PRODUITS {
        string id_reference_produit PK
        string nom
        float prix
        int stock
    }
    
    MAGASINS {
        int id_magasin PK
        string ville
        int nombre_de_salaries
    }
    
    VENTES {
        date date PK
        string id_reference_produit FK
        int id_magasin FK
        int quantite
    }
```

## Diagramme de la Base de Données
```sh
+----------------------------+          +--------------------+
| PRODUITS                   |          | MAGASINS           |
+----------------------------+          +--------------------+
| id_reference_produit (PK)  |          | id_magasin (PK)    |
| nom                        |          | ville              |
| prix                       |          | nombre_de_salaries |
| stock                      |          +--------------------+
+----------------------------+                 |
           |                                   |
           |                                   |
           | one-to-many                       | one-to-many
           | (one product can be               | (one store can have
           | in many sales)                    | many sales)
           |                                   |
           ↓                                   ↓
+---------------------------------------------------+
| VENTES                                            |
+---------------------------------------------------+
| date (PK)                                         |
| id_reference_produit (FK) -----> PRODUITS         |
| id_magasin (FK) -----> MAGASINS                   |
| quantite                                          |
+---------------------------------------------------+
```
## Instructions d'Installation

1. **Cloner le dépôt:**
   ```
   git clone https://github.com/Hatchi-Kin/simplon_7.git
   cd simplon_7
   ```

2. **Construire et lancer l'application avec Docker Compose:**
   ```
   docker compose build
   docker compose up -d
   ```

3. **Accéder à la documentation interative FastAPI:**
   Ouvrez votre navigateur et naviguez vers `http://localhost:8000/docs`.

## Utilisation

- **Page d'analyse des ventes:**
  Accédez aux résultats d'analyse en naviguant vers `http://localhost:8000/web/dashboard` dans votre navigateur.

- **Voir le schéma de la base de données:**
  Pour déboguer ou vérifier la structure de la base de données, effectuer une requête GET à `http://localhost:8000/api/schema`.

- **Exécuter des requêtes SQL personnalisées:**
  Vous pouvez envoyer des requêtes SQL à l'application via une requête POST à `http://localhost:8000/api/query`.

## Fonctionnalités d'Analyse

L'application fournit trois analyses principales demandées par la direction:

1. **Chiffre d'affaires total de l'entreprise**
   - Calcule la somme totale des ventes en multipliant les quantités vendues par les prix unitaires.

2. **Analyse des ventes par produit**
   - Affiche pour chaque produit les quantités vendues et le chiffre d'affaires généré.
   - Les produits sont classés par chiffre d'affaires décroissant.

3. **Analyse des ventes par région**
   - Présente les performances de chaque magasin regroupées par ville.
   - Inclut les quantités vendues et le chiffre d'affaires généré.

4. **Performance par employé**
   - Visualisation graphique du ratio chiffre d'affaires/nombre d'employés pour chaque magasin.
   - Permet d'identifier les magasins les plus efficaces en termes de productivité par employé.

## Screenshot

![Analyse des Ventes](./Analyse_des_Ventes.png)
