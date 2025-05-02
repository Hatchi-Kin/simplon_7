import sqlite3
import unicodedata

import pandas as pd
from fastapi.templating import Jinja2Templates

DATABASE_PATH = "/app/data/sales.db"
templates = Jinja2Templates(directory="templates")


def initialize_database():
    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create tabels
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS produits (
        id_reference_produit TEXT PRIMARY KEY,
        nom TEXT,
        prix REAL,
        stock INTEGER
    )
    """
    )
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS magasins (
        id_magasin INTEGER PRIMARY KEY,
        ville TEXT,
        nombre_de_salaries INTEGER
    )
    """
    )
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS ventes (
        date TEXT,
        id_reference_produit TEXT,
        quantite INTEGER,
        id_magasin INTEGER,
        FOREIGN KEY (id_reference_produit) REFERENCES produits(id_reference_produit),
        FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin)
    )
    """
    )

    # Load data, normalize column names, write to table
    produits_df = pd.read_csv("/app/data/produits.csv")
    magasins_df = pd.read_csv("/app/data/magasins.csv")
    ventes_df = pd.read_csv("/app/data/ventes.csv")

    produits_df = normalize_column_names(produits_df)
    magasins_df = normalize_column_names(magasins_df)
    ventes_df = normalize_column_names(ventes_df)

    produits_df.to_sql("produits", conn, if_exists="replace", index=False)
    magasins_df.to_sql("magasins", conn, if_exists="replace", index=False)
    ventes_df.to_sql("ventes", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()


def normalize_column_names(df):
    df.columns = [
        unicodedata.normalize("NFKD", col)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .replace(" ", "_")
        .lower()
        for col in df.columns
    ]
    return df
