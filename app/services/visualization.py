import base64
from io import BytesIO

import matplotlib.pyplot as plt


def generate_employee_performance_chart(data):
    """Generate a bar chart showing revenue per employee by store"""
    if not data:
        return None

    stores = [row[0] for row in data]  # Store names
    revenue_per_employee = [row[3] for row in data]  # Revenue per employee

    plt.figure(figsize=(10, 6))
    plt.bar(stores, revenue_per_employee, color="#4CAF50")
    plt.xlabel("Store")
    plt.ylabel("Revenue per Employee (€)")
    plt.title("Store Efficiency - Revenue per Employee")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save to BytesIO object and encode as base64
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    buf.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return image_base64
