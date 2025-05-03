from fastapi import FastAPI

from utils.init_app import initialize_database
from utils.routes import api_router, web_router

app = FastAPI(title="Analyses des Ventes")
app.include_router(api_router)
app.include_router(web_router)

@app.on_event("startup")
def startup_event():
    initialize_database()


