import sqlite3

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from .init_app import DATABASE_PATH, templates
from .sql_queries import (
    get_total_revenue,
    get_sales_by_product,
    get_sales_by_region,
    get_revenue_per_employee,
)
from .plot_generator import generate_revenue_per_employee_plot

api_router = APIRouter(prefix="/api", tags=["api"])
web_router = APIRouter(prefix="/web", tags=["web"])

@api_router.get("/schema")
def get_schema():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Get list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}
    for table in tables:
        table_name = table[0]
        # Get column info for this table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema[table_name] = [
            {
                "cid": col[0],
                "name": col[1],
                "type": col[2],
                "notnull": col[3],
                "default": col[4],
                "pk": col[5],
            }
            for col in columns
        ]

    conn.close()

    return schema


@api_router.post("/query")
def execute_query(query: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()

        return {"result": result}

    finally:
        conn.close()


@web_router.get("/dashboard", response_class=HTMLResponse)
def analysis(request: Request):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # 1. Chiffre d'affaires total
        cursor.execute(get_total_revenue())
        total_revenue = cursor.fetchone()[0]

        # 2. Ventes par produit
        cursor.execute(get_sales_by_product())
        product_sales = cursor.fetchall()

        # 3. Ventes par région
        cursor.execute(get_sales_by_region())
        region_sales = cursor.fetchall()

        # 4. Chiffre d'affaires par employé (pour le graphique)
        cursor.execute(get_revenue_per_employee())
        revenue_per_employee_data = cursor.fetchall()
        revenue_per_employee_plot = generate_revenue_per_employee_plot(
            revenue_per_employee_data
        )

    except Exception as e:
        print(f"Error in analysis endpoint: {str(e)}")
        return HTMLResponse(
            content=f"<html><body><h1>Erreur</h1><p>{str(e)}</p></body></html>"
        )
    finally:
        conn.close()

    return templates.TemplateResponse(
        "analysis.html",
        {
            "request": request,
            "total_revenue": total_revenue,
            "product_sales": product_sales,
            "region_sales": region_sales,
            "revenue_per_employee_plot": revenue_per_employee_plot,
        },
    )
