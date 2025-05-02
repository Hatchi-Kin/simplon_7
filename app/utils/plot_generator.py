import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_revenue_per_employee_plot(data):
    """
    Génère un graphique en barres montrant le chiffre d'affaires par employé pour chaque magasin
    """
    # Extraire les données
    stores = [row[0] for row in data]  # Noms des magasins
    revenue_per_employee = [row[3] for row in data]  # CA par employé
    
    # Créer la figure et l'axe
    plt.figure(figsize=(10, 6))
    
    # Créer le graphique en barres
    plt.bar(stores, revenue_per_employee, color='#4CAF50')
    
    # Ajouter les étiquettes et le titre
    plt.xlabel('Magasin')
    plt.ylabel('Chiffre d\'Affaires par Employé (€)')
    plt.title('Efficacité des Magasins - CA par Employé')
    
    # Rotation des étiquettes pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Ajouter les valeurs au-dessus des barres
    for i, v in enumerate(revenue_per_employee):
        plt.text(i, v + 5, f'{v:.2f}€', ha='center', fontweight='bold')
    
    # Ajuster la mise en page
    plt.tight_layout()
    
    # Sauvegarder dans un objet BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    
    # Encoder en base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64