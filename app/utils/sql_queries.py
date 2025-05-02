def get_total_revenue():
    return """
    SELECT SUM(ventes.quantite * produits.prix) AS chiffre_affaires_total
    FROM ventes
    JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
    """


def get_sales_by_product():
    return """
    SELECT 
        produits.nom AS produit,
        SUM(ventes.quantite) AS quantite_totale,
        SUM(ventes.quantite * produits.prix) AS chiffre_affaires
    FROM ventes
    JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
    GROUP BY produits.nom
    ORDER BY chiffre_affaires DESC
    """


def get_sales_by_region():
    return """
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


def get_revenue_per_employee():
    """
    Requête pour obtenir le chiffre d'affaires par employé pour chaque magasin
    """
    return """
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
