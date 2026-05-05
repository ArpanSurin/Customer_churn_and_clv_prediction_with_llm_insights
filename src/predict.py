import os
import joblib
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def run_predictions():
    print("="*60)
    print("🚀 STARTING BATCH PREDICTION PIPELINE")
    print("="*60)

    MODEL_DIR = BASE_DIR / "models"
    try:
        churn_model = joblib.load(MODEL_DIR / "best_churn_model.pkl")
        clv_model = joblib.load(MODEL_DIR / "best_clv_model.pkl")

    except FileNotFoundError as e:
        print(f"❌ Error: Model files not found in {MODEL_DIR}. Run model.py first.")
        return
    
    print("📥 Fetching features from PostgreSQL...")
    df = pd.read_sql("SELECT * FROM final_features", engine)
    
    if df.empty:
        print("⚠️ No data found in the database to predict.")
        return

    customer_ids = df['customer_id'] 
    X_churn = df.drop(columns=[
        'customer_id', 'churn_status', 'churn_label', 
        'future_spend', 'days_since_last_order', 
        'lifetime_spend', 'last_order_date', 'registration_date'
    ], errors='ignore')


    X_clv = df.drop(columns=[
        'customer_id', 'future_spend', 'churn_status', 'churn_label', 
        'lifetime_spend', 'avg_order_value', 'spend_per_order', 
        'days_since_last_order', 'last_order_date', 'registration_date'
    ], errors='ignore')

    print("🧠 Generating predictions...")
    
    df['predicted_churn_id'] = churn_model.predict(X_churn)
    df['churn_probability'] = churn_model.predict_proba(X_churn).max(axis=1)

    df['predicted_clv'] = clv_model.predict(X_clv)

    results_df = df[[
        'customer_id', 
        'predicted_churn_id', 
        'churn_probability', 
        'predicted_clv'
    ]].copy()
    
    results_df['prediction_date'] = pd.Timestamp.now()

    print("📤 Saving results to table: 'customer_predictions'...")
    results_df.to_sql('customer_predictions', engine, if_exists='replace', index=False)
    
    print("✅ Success! Database updated.")
    print("="*60)

