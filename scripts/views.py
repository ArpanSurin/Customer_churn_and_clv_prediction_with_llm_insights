import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if not load_dotenv(ENV_PATH):
    print(f"⚠️ Warning: Could not find .env file at {ENV_PATH}")

db_url = os.getenv("DB_URL")

if db_url is None:
    raise ValueError("❌ DB_URL not found in .env file. Check your key spelling!")

def create_views(engine, file_path):
    with open(file_path, 'r') as f:
        query = text(f.read())
    
    with engine.begin() as conn:
        conn.execute(query)
    print("Views updated successfully!")

def get_data_from_views(engine):
    
    df_cust = pd.read_sql("SELECT * FROM dim_customers", engine)
    df_ord = pd.read_sql("SELECT * FROM fact_orders", engine)
    
    print(f"Data loaded: {len(df_cust)} customers and {len(df_ord)} orders.")
    return df_cust, df_ord