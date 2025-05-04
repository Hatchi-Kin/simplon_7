import time
from fastapi import FastAPI

from core.database import initialize_tables, get_connection
from gdrive.importers import import_all_data
from routes.api import router as api_router
from routes.web import router as web_router
from services.analysis import run_analysis

app = FastAPI(
    title="Sales Analysis Dashboard",
    description="An application for analyzing and visualizing sales data",
    version="1.0.0",
)

app.include_router(api_router)
app.include_router(web_router)


@app.on_event("startup")
async def startup_event():
    time.sleep(1)
    initialize_tables()

    with get_connection() as conn:
        import_all_data(conn)

    run_analysis()
