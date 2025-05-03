import matplotlib.pyplot as plt
import base64
from io import BytesIO


def generate_revenue_per_employee_plot(data):
    stores = [row[0] for row in data]  # Noms des magasins
    revenue_per_employee = [row[3] for row in data]  # CA par employé

    plt.figure(figsize=(10, 6))
    plt.bar(stores, revenue_per_employee, color="#4CAF50")

    plt.xlabel("Magasin")
    plt.ylabel("Chiffre d'Affaires par Employé (€)")
    plt.title("Efficacité des Magasins - CA par Employé")

    plt.xticks(rotation=45, ha="right")

    for i, v in enumerate(revenue_per_employee):
        plt.text(i, v + 5, f"{v:.2f}€", ha="center", fontweight="bold")

    plt.tight_layout()

    # Sauvegarder dans un objet BytesIO, puis encoder en base64
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return image_base64
