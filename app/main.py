import sqlite3
import unicodedata

from fastapi import FastAPI

from utils.init_app import initialize_database
from utils.routes import router as sql_router

app = FastAPI()
app.include_router(sql_router)

@app.on_event("startup")
def startup_event():
    initialize_database()


