import pandas as pd
import os

def extract_data():

    print("---------------------------------------------------------------------------------")
    print("[EXTRACT] BEGIN.")
    print("---------------------------------------------------------------------------------")
    
    print("Loading the data into python. \n")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(__file__)
    
    cust_path = os.path.join(BASE_DIR, "data", "raw", "customers.csv")
    ord_path  = os.path.join(BASE_DIR, "data", "raw", "orders.csv")

    cust = pd.read_csv(cust_path)
    ord  = pd.read_csv(ord_path)    
    
    print("--------------------------")
    print("[Extract] customers data")
    print("--------------------------")

    # 1. Basic shape check - customers table
    print(f"[EXTRACT] Rows loaded: {len(cust):,}\n")
    print(f"[EXTRACT] Columns loaded: {cust.columns.tolist()}\n")
    print(f"[EXTRACT] Null counts per column:")
    print(cust.isnull().sum().to_string(), "\n")
    print(cust.describe())

    print("--------------------------")
    print("[Extract] orders data")
    print("--------------------------")

    # 1. Basic shape check - orders table
    print(f"[EXTRACT] Rows: {len(ord):,}\n")
    print(f"[EXTRACT] Columns loaded: {ord.columns.to_list()}\n")
    print(f"[EXTRACT] Null counts per column:")
    print(ord.isna().sum().to_string(), "\n")
    print(ord.describe())

    print(f"[EXTRACT] Completed successfully\n")

    return cust, ord
    # ---------------------------------------------------------------------------------


