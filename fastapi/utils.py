from pathlib import Path
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def engineered_features(data: dict):
    df = pd.DataFrame([data])

    today = pd.Timestamp.now()
    reg_date = pd.to_datetime(df['registration_date'])

    df['customer_tenure_days'] = (today - reg_date).dt.days
    months_active = df['customer_tenure_days'] / 30

    df['avg_order_value'] = df['lifetime_spend'] / df['total_orders'].replace(0, 1)
    df['return_rate'] = df['total_returns'] / df['total_orders'].replace(0, 1)
    df['rating_rate'] = df['total_ratings'] / df['total_orders'].replace(0, 1)
    df['orders_per_month'] = df['total_orders'] / months_active.replace(0, 1)

    cols_to_remove = ['registration_date', 'last_order_date', 'churn_status']
    df = df.drop(columns=cols_to_remove, errors='ignore')
    
    return df

def get_strategy(churn_status, prob, clv_value):
    status_map = {0: "Active", 1: "At-risk", 2: "Churn"}
    label = status_map.get(churn_status, "Unknown")

    if clv_value < 10000:
        clv_tier = "LOW"
    elif clv_value < 150000: 
        clv_tier = "MEDIUM"
    else: 
        clv_tier = "HIGH"

    matrix = {
        "Active": {
            "LOW": "🟢 Monitor (Self-Service)",
            "MEDIUM": "🟢 Upsell (Growth)",
            "HIGH": "⭐ VIP (Advocacy & Referral)"
        },
        "At-risk": {
            "LOW": "🟡 Automated Nurture",
            "MEDIUM": "🟠 Incentive (Discount/Offer)",
            "HIGH": "🔴 CRITICAL (Human Outreach)"
        },
        "Churn": {
            "LOW": "⚪ Low Effort Win-back",
            "MEDIUM": "🔵 Strategic Win-back",
            "HIGH": "🚨 EXECUTIVE SAVE (Immediate Call)"
        }
    }
    
    strategy = matrix.get(label, {}).get(clv_tier, "⚪ Unknown")

    if prob > 0.95 and label == "At-risk":
        strategy = "🔥 EMERGENCY: " + strategy
        
    return strategy


def engineer_features_for_api_batch(df: pd.DataFrame):
    today = pd.Timestamp.now()
    df['registration_date'] = pd.to_datetime(df['registration_date'])
    df['customer_tenure_days'] = (today - df['registration_date']).dt.days
    
    df['return_rate'] = df['total_returns'] / df['total_orders'].replace(0, 1)
    
    cols_to_drop = ['registration_date', 'last_order_date', 'customer_id', 'churn_status']
    return df.drop(columns=[c for c in cols_to_drop if c in df.columns])


def get_ai_strategy(customer_data, churn_status, clv):
    prompt = f"""
    You are a Senior Business Consultant. Analyze this customer data:
    - Churn Risk: {churn_status}
    - Predicted Lifetime Value: ${clv}
    - Segment: {customer_data['customer_segment']}
    - Behavior: {customer_data['total_orders']} orders with {customer_data['total_returns']} returns.

    Provide a concise, 3-bullet point strategy:
    1. Risk Assessment (Why they might leave or why they are valuable)
    2. Immediate Action (What to do right now)
    3. Personalized Offer (Specific discount or message)
    
    Keep it under 80 words. Be professional and decisive.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful business growth expert."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile", # High-quality, fast model
        temperature=0.5,
    )

    return chat_completion.choices[0].message.content
