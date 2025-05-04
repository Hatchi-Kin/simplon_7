# Core business tables
CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS produits (
    id_reference_produit TEXT PRIMARY KEY,
    nom TEXT,
    prix REAL,
    stock INTEGER
)
"""

CREATE_STORES_TABLE = """
CREATE TABLE IF NOT EXISTS magasins (
    id_magasin INTEGER PRIMARY KEY,
    ville TEXT,
    nombre_de_salaries INTEGER
)
"""

CREATE_SALES_TABLE = """
CREATE TABLE IF NOT EXISTS ventes (
    date TEXT,
    id_reference_produit TEXT,
    quantite INTEGER,
    id_magasin INTEGER,
    FOREIGN KEY (id_reference_produit) REFERENCES produits(id_reference_produit),
    FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin)
)
"""

# Analysis results tables
CREATE_REVENUE_TABLE = """
CREATE TABLE IF NOT EXISTS chiffre_affaires_total (
    date_analyse TEXT PRIMARY KEY,
    montant_total REAL
)
"""

CREATE_PRODUCT_SALES_TABLE = """
CREATE TABLE IF NOT EXISTS ventes_par_produit (
    date_analyse TEXT,
    nom_produit TEXT,
    quantite_totale INTEGER,
    chiffre_affaires REAL,
    PRIMARY KEY (date_analyse, nom_produit) 
)
"""

CREATE_REGION_SALES_TABLE = """
CREATE TABLE IF NOT EXISTS ventes_par_region (
    date_analyse TEXT,
    region TEXT,
    quantite_totale INTEGER,
    chiffre_affaires REAL,
    PRIMARY KEY (date_analyse, region)
)
"""

# Analysis queries
TOTAL_REVENUE_QUERY = """
SELECT SUM(ventes.quantite * produits.prix) AS chiffre_affaires_total
FROM ventes
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
"""

SALES_BY_PRODUCT_QUERY = """
SELECT 
    produits.nom AS produit,
    SUM(ventes.quantite) AS quantite_totale,
    SUM(ventes.quantite * produits.prix) AS chiffre_affaires
FROM ventes
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
GROUP BY produits.nom
ORDER BY chiffre_affaires DESC
"""

SALES_BY_REGION_QUERY = """
SELECT 
    magasins.ville AS region,
    SUM(ventes.quantite) AS quantite_totale,
    SUM(ventes.quantite * produits.prix) AS chiffre_affaires
FROM ventes
JOIN magasins ON ventes.id_magasin = magasins.id_magasin
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
GROUP BY magasins.ville
ORDER BY chiffre_affaires DESC
"""

REVENUE_PER_EMPLOYEE_QUERY = """
SELECT 
    magasins.ville AS magasin,
    magasins.nombre_de_salaries AS nombre_employes,
    SUM(ventes.quantite * produits.prix) AS chiffre_affaires_total,
    SUM(ventes.quantite * produits.prix) / magasins.nombre_de_salaries AS chiffre_affaires_par_employe
FROM ventes
JOIN magasins ON ventes.id_magasin = magasins.id_magasin
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
GROUP BY magasins.ville, magasins.nombre_de_salaries
ORDER BY chiffre_affaires_par_employe DESC
"""

# Insert queries
INSERT_TOTAL_REVENUE = "INSERT INTO chiffre_affaires_total (date_analyse, montant_total) VALUES (?, ?)"

INSERT_PRODUCT_SALES = """
INSERT INTO ventes_par_produit 
(date_analyse, nom_produit, quantite_totale, chiffre_affaires) 
VALUES (?, ?, ?, ?)
"""

INSERT_REGION_SALES = """
INSERT INTO ventes_par_region 
(date_analyse, region, quantite_totale, chiffre_affaires) 
VALUES (?, ?, ?, ?)
"""

# Retrieval queries
LATEST_ANALYSIS_DATE_QUERY = "SELECT MAX(date_analyse) FROM chiffre_affaires_total"
TOTAL_REVENUE_BY_DATE_QUERY = "SELECT montant_total FROM chiffre_affaires_total WHERE date_analyse = ?"
PRODUCT_SALES_BY_DATE_QUERY = "SELECT nom_produit, quantite_totale, chiffre_affaires FROM ventes_par_produit WHERE date_analyse = ?"
REGION_SALES_BY_DATE_QUERY = "SELECT region, quantite_totale, chiffre_affaires FROM ventes_par_region WHERE date_analyse = ?"