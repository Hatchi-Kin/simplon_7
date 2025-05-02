# FastAPI SQLite Sales Analysis Project

Ce projet met en place une application FastAPI qui se connecte à une base de données SQLite pour analyser les données de ventes d'une entreprise. Le tout est conteneurisé avec Docker pour faciliter le déploiement et la gestion des dépendances.

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

## Schéma de la Base de Données
```sh
+----------------------------+     +--------------------+     +---------------------------+
| PRODUITS                   |     | MAGASINS           |     | VENTES                    |
+----------------------------+     +--------------------+     +---------------------------+
| id_reference_produit (PK)  |     | id_magasin (PK)    |     | date (PK)                 |
| nom                        |     | ville              |     | id_reference_produit (FK) |
| prix                       |     | nombre_de_salaries |     | quantite                  |
| stock                      |     +--------------------+     | id_magasin (FK)           |
+----------------------------+                               +----------------------------+
          |                                                        ^
          |                                                        |
          +--------------------------------------------------------+
                        (Clé étrangère)
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
  Accédez aux résultats d'analyse en naviguant vers `http://localhost:8000/execute/analysis` dans votre navigateur.

- **Voir le schéma de la base de données:**
  Pour déboguer ou vérifier la structure de la base de données, visitez `http://localhost:8000/execute/schema`.

- **Exécuter des requêtes SQL personnalisées:**
  Vous pouvez envoyer des requêtes SQL à l'application via une requête POST à l'endpoint `/execute/query`.

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
