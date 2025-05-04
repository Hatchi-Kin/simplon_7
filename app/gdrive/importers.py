import requests
from io import StringIO

import pandas as pd

from core.config import DATA_SOURCES
from gdrive.schemas import DATA_SCHEMAS

def fetch_data_from_url(url):
    """Fetch CSV data from a URL and return as DataFrame"""
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"
    data = StringIO(response.text)
    return pd.read_csv(data)

def create_composite_key(df, key_columns):
    """Create a composite key from multiple columns"""
    return df[key_columns].astype(str).agg('_'.join, axis=1)

def import_table_data(conn, table_name):
    """Import data for a specific table using schema configuration"""
    if table_name not in DATA_SCHEMAS or table_name not in DATA_SOURCES:
        raise ValueError(f"Unknown table: {table_name}")
    
    schema = DATA_SCHEMAS[table_name]
    url = DATA_SOURCES[table_name]["url"]
    
    try:
        # Fetch the data
        df = fetch_data_from_url(url)
        
        # Rename columns using the mapping
        df = df.rename(columns=schema["mapping"], errors="ignore")
        
        # Select only required columns
        df_to_import = df[schema["required_columns"]]
        
        # Handle special case for ventes - check for duplicates
        if table_name == "ventes" and "composite_key" in schema:
            # Check if we have existing data
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            existing_count = cursor.fetchone()[0]
            
            if existing_count > 0:
                # Create composite key for new and existing data
                existing_data = pd.read_sql(
                    f"SELECT {', '.join(schema['composite_key'])} FROM {table_name}", 
                    conn
                )
                
                df_to_import["composite_key"] = create_composite_key(df_to_import, schema["composite_key"])
                existing_data["composite_key"] = create_composite_key(existing_data, schema["composite_key"])
                
                # Filter to only new records
                new_data = df_to_import[~df_to_import["composite_key"].isin(existing_data["composite_key"])]
                new_data = new_data.drop(columns=["composite_key"])
                
                if len(new_data) > 0:
                    new_data.to_sql(table_name, conn, if_exists="append", index=False)
                return len(new_data)
        
        # Standard import for new or replaced tables
        df_to_import.to_sql(table_name, conn, if_exists="replace", index=False)
        return len(df_to_import)
        
    except Exception as e:
        print(f"Error importing {table_name}: {e}")
        return 0

def import_all_data(conn):
    """Import all configured data tables"""
    tables_imported = []
    for table_name in ["produits", "magasins", "ventes"]:
        rows_imported = import_table_data(conn, table_name)
        tables_imported.append(f"{table_name}: {rows_imported} rows")
    
    return tables_imported