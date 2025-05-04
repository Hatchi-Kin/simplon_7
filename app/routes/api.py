from fastapi import APIRouter

from core.database import get_connection, execute_query
from services.analysis import run_analysis

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/schema")
def get_database_schema():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        schema = {}
        for table in tables:
            table_name = table[0]
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

        return schema


@router.post("/query")
def execute_custom_query(query: str):
    """Execute a custom SQL query"""
    try:
        result = execute_query(query)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@router.post("/run-analysis")
def trigger_analysis():
    """Trigger a fresh data analysis"""
    try:
        success = run_analysis()
        if success:
            return {"status": "success", "message": "Analysis completed successfully"}
        return {"status": "error", "message": "Analysis failed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
