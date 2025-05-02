## Structure de la base de données

1. **Table `produits`**
   - `nom`: Nom du produit (TEXT)
   - `id_reference_produit`: Identifiant unique du produit (TEXT)
   - `prix`: Prix unitaire du produit (REAL)
   - `stock`: Quantité en stock (INTEGER)

2. **Table `magasins`**
   - `id_magasin`: Identifiant unique du magasin (INTEGER)
   - `ville`: Localisation du magasin (TEXT)
   - `nombre_de_salaries`: Nombre d'employés dans le magasin (INTEGER)

3. **Table `ventes`**
   - `date`: Date de la vente (TEXT)
   - `id_reference_produit`: Référence du produit vendu (TEXT)
   - `quantite`: Quantité vendue (INTEGER)
   - `id_magasin`: Identifiant du magasin où la vente a été réalisée (INTEGER)

## Requêtes d'analyse et interprétation des résultats

### 1. Chiffre d'affaires total
Le résultat obtenu représente la performance globale de l'entreprise sur la période analysée (30 jours).

```sql
SELECT SUM(ventes.quantite * produits.prix) AS chiffre_affaires_total
FROM ventes
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
```

- Cette requête calcule le chiffre d'affaires total en multipliant la quantité vendue par le prix unitaire pour chaque vente.
- La jointure avec la table `produits` est nécessaire pour obtenir le prix de chaque produit.
- La fonction d'agrégation `SUM()` additionne toutes les valeurs pour donner le chiffre d'affaires total.


### 2. Ventes par produit
Cette analyse permet d'identifier les produits les plus rentables et les plus populaires.

```sql
SELECT 
    produits.nom AS produit,
    SUM(ventes.quantite) AS quantite_totale,
    SUM(ventes.quantite * produits.prix) AS chiffre_affaires
FROM ventes
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
GROUP BY produits.nom
ORDER BY chiffre_affaires DESC
```

- Cette requête agrège les ventes par produit.
- Pour chaque produit, elle calcule la quantité totale vendue et le chiffre d'affaires généré.
- Les résultats sont regroupés par nom de produit (`GROUP BY produits.nom`).
- Le tri est effectué par ordre décroissant de chiffre d'affaires (`ORDER BY chiffre_affaires DESC`).


### 3. Ventes par région
Cette analyse révèle la performance relative de chaque région/ville.

```sql
SELECT 
    magasins.ville AS region,
    SUM(ventes.quantite) AS quantite_totale,
    SUM(ventes.quantite * produits.prix) AS chiffre_affaires
FROM ventes
JOIN magasins ON ventes.id_magasin = magasins.id_magasin
JOIN produits ON ventes.id_reference_produit = produits.id_reference_produit
GROUP BY magasins.ville
ORDER BY chiffre_affaires DESC
```

- Cette requête analyse les performances de vente par région (ville).
- Elle nécessite deux jointures: une avec la table `magasins` pour obtenir la localisation et une avec la table `produits` pour calculer le chiffre d'affaires.
- Les résultats sont regroupés par ville (`GROUP BY magasins.ville`).
- Le tri est effectué par ordre décroissant de chiffre d'affaires (`ORDER BY chiffre_affaires DESC`).


### 4. Chiffre d'affaires par employé
Cette métrique est un indicateur clé de l'efficacité opérationnelle des magasins.

```sql
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
```

- Cette requête calcule l'efficacité des magasins en termes de chiffre d'affaires généré par employé.
- Elle divise le chiffre d'affaires total de chaque magasin par son nombre d'employés.
- Les résultats sont groupés par ville et nombre d'employés.
- Le tri est effectué par ordre décroissant de chiffre d'affaires par employé.
