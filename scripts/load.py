from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def load_to_db(clean_cust, clean_ord):

    # Loading the cleaned data to PostgreSQL database
    # ---------------------------------------------------------------------------------
    
    db_url = os.getenv("DB_URL")
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=60
    )

    print("\n---------------------------------------------------------------------------")
    print("[LOAD] Begin")
    print("---------------------------------------------------------------------------")

    tables = {
        "customers": clean_cust,
        "orders": clean_ord
    }

    for table_name, df in tables.items():
        print(f"[Loading] {table_name} - {len(df):,} rows...")

        try:
            with engine.begin() as conn:
                df.to_sql(
                    name = table_name,
                    con = engine,
                    if_exists = 'replace',
                    index = False,
                    method = 'multi',
                    chunksize = 10_000
                )
            print(f"[LOAD] {table_name} loaded successfully\n")

        except Exception as e:
            print(f"[LOAD] failed on {table_name}: {e}")
            print(f"[LOAD] skipping {table_name} and continuing....")

    print("---------------------------------------------------------------------------")

    # ---------------------------------------------------------------------------------
