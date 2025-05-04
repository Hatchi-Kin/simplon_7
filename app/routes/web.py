from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from core.config import TEMPLATES_DIR
from core.database import execute_query
from models.tables import REVENUE_PER_EMPLOYEE_QUERY
from services.analysis import get_latest_analysis
from services.visualization import generate_employee_performance_chart

router = APIRouter(prefix="/web", tags=["web"])
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """Render the sales dashboard"""
    total_revenue, product_sales, region_sales = get_latest_analysis()

    if not total_revenue:
        return HTMLResponse(
            content="<html><body><h1>Error</h1><p>No analysis data available</p></body></html>"
        )

    # Generate employee performance chart
    try:
        employee_data = execute_query(REVENUE_PER_EMPLOYEE_QUERY)
        employee_chart = generate_employee_performance_chart(employee_data)
    except Exception as e:
        print(f"Error generating employee chart: {str(e)}")
        return HTMLResponse(
            content=f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"
        )

    return templates.TemplateResponse(
        "analysis.html",
        {
            "request": request,
            "total_revenue": total_revenue,
            "product_sales": product_sales,
            "region_sales": region_sales,
            "employee_chart": employee_chart,
        },
    )
