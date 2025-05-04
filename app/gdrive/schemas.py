# Schema definitions for data sources
DATA_SCHEMAS = {
    "produits": {
        "mapping": {
            "ID Référence produit": "id_reference_produit", 
            "id_rafarence_produit": "id_reference_produit",
            "Nom": "nom",
            "Prix": "prix",
            "Stock": "stock"
        },
        "required_columns": ["id_reference_produit", "nom", "prix", "stock"]
    },
    "magasins": {
        "mapping": {
            "ID Magasin": "id_magasin",
            "Ville": "ville",
            "Nombre de salariés": "nombre_de_salaries",
            "nombre_de_salarias": "nombre_de_salaries" 
        },
        "required_columns": ["id_magasin", "ville", "nombre_de_salaries"]
    },
    "ventes": {
        "mapping": {
            "Date": "date",
            "ID Référence produit": "id_reference_produit",
            "Quantité": "quantite",
            "ID Magasin": "id_magasin"
        },
        "required_columns": ["date", "id_reference_produit", "quantite", "id_magasin"],
        "composite_key": ["date", "id_reference_produit", "id_magasin"]
    }
}