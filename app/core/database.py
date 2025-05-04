import os
import sqlite3
import contextlib

from core.config import DATABASE_PATH

@contextlib.contextmanager
def get_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, timeout=30)
    # Set pragmas for better performance and reliability
    conn.execute('PRAGMA journal_mode = WAL;')
    conn.execute('PRAGMA synchronous = NORMAL;')
    
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=None, fetch=True):
    """Execute a SQL query and return results if requested"""
    with get_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.rowcount

def initialize_tables():
    from models.tables import (
        CREATE_PRODUCTS_TABLE,
        CREATE_STORES_TABLE,
        CREATE_SALES_TABLE,
        CREATE_REVENUE_TABLE,
        CREATE_PRODUCT_SALES_TABLE,
        CREATE_REGION_SALES_TABLE
    )
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Create main tables
        cursor.execute(CREATE_PRODUCTS_TABLE)
        cursor.execute(CREATE_STORES_TABLE)
        cursor.execute(CREATE_SALES_TABLE)
        
        # Create analysis tables
        cursor.execute(CREATE_REVENUE_TABLE)
        cursor.execute(CREATE_PRODUCT_SALES_TABLE)
        cursor.execute(CREATE_REGION_SALES_TABLE)
        
        conn.commit()