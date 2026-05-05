import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent / ".env"
load_dotenv(BASE_DIR)

db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

def feature_engineering(df_cust, df_ord):

    df = df_cust.merge(df_ord, on='customer_id', how='inner')
    print("\n" + "="*60)
    print("FEATURE ENGINEERING STARTED")
    print("="*60)

    print(f"Rows after merge: {len(df)}")

    print("\nFixing datatypes...")

    df['order_timestamp'] = pd.to_datetime(df['order_timestamp'], errors='coerce')
    df['last_order_date'] = pd.to_datetime(df['last_order_date'], errors='coerce')
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')

    cat_cols = ['category', 'gender', 'payment_method', 'customer_segment', 'order_status']
    for col in cat_cols:
        df[col] = df[col].astype('category')

    print("\nMissing Values Summary:")
    missing = df.isna().sum()
    print(missing[missing > 0].sort_values(ascending=False))

    # Fill
    df['city'] = df['city'].fillna('Unknown')
    df['delivery_days'] = df['delivery_days'].fillna(-1)
    df['rating'] = df['rating'].fillna(-1)

    # Flags
    df['has_rating'] = (df['rating'] != -1).astype(int)

    print("\nCreating customer-level features...")

    agg = df.groupby('customer_id').agg(
        total_orders=('order_id', 'count'),
        lifetime_spend=('final_amount', 'sum'),
        avg_order_value=('final_amount', 'mean'),
        total_returns=('is_returned', 'sum'),
        avg_discount_pct=('discount_pct', 'mean'),
        avg_delivery_days=('delivery_days', 'mean'),
        avg_rating=('rating', lambda x: x[x != -1].mean()),
        total_ratings=('has_rating', 'sum'),
        last_order_date=('order_timestamp', 'max')
    ).reset_index()

    print("Creating derived features...")

    snapshot_date = df['order_timestamp'].max()

    agg['days_since_last_order'] = (snapshot_date - agg['last_order_date']).dt.days

    agg['return_rate'] = np.where(
        agg['total_orders'] > 0,
        agg['total_returns'] / agg['total_orders'],
        0
    )

    agg['rating_rate'] = np.where(
        agg['total_orders'] > 0,
        agg['total_ratings'] / agg['total_orders'],
        0
    )

    agg['spend_per_order'] = np.where(
        agg['total_orders'] > 0,
        agg['lifetime_spend'] / agg['total_orders'],
        0
    )

    print("Merging customer info...")

    customer_cols = [
        'customer_id', 'age', 'gender', 'city',
        'customer_segment', 'email_available', 'phone_available',
        'registration_date', 'churn_status'
    ]

    df_customers = df[customer_cols].drop_duplicates()

    df_final = agg.merge(df_customers, on='customer_id', how='left')

    print("Creating tenure features...")

    df_final['customer_tenure_days'] = (
        snapshot_date - df_final['registration_date']
    ).dt.days

    df_final['orders_per_month'] = np.where(
        df_final['customer_tenure_days'] > 0,
        df_final['total_orders'] / (df_final['customer_tenure_days'] / 30),
        0
    )

    print("\nFinal cleanup...")

    df_final = df_final.replace([np.inf, -np.inf], 0)

    df_final = df_final.fillna(0)

    # Run this once at the end of feature_engineering.py
    df_final.to_sql('final_features', engine, if_exists='replace', index=False)

    print("\nFinal Dataset Shape:", df_final.shape)

    print("[FEATURE ENGINEERING] Completed")

    return df_final
