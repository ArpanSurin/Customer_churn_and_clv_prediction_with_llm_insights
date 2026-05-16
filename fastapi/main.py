from datetime import datetime
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import uvicorn
from pathlib import Path
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from utils import engineer_features_for_api_batch, engineered_features, get_strategy
from schemas import CustomerInput
from utils import get_ai_strategy
from fastapi import Body

app = FastAPI(title="Churn prediction API")

BASE_DIR = Path(__file__).parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

db_url = os.getenv("DB_URL") 
engine = create_engine(db_url)

@app.get("/")
async def root():
    return {"message": "Server is running successfully"}

try:
    churn_pipe = joblib.load("../models/best_churn_model.pkl")
    clv_pipe = joblib.load("../models/best_clv_model.pkl")
except Exception as e:
    print(f"⚠️ Error loading models: {e}")

@app.post("/predict")
async def predict_customers(request: CustomerInput):
    try:
        raw_data = request.model_dump()

        features_df = engineered_features(raw_data)

        churn_id = int(churn_pipe.predict(features_df)[0])
        churn_prob = float(churn_pipe.predict_proba(features_df).max())

        mapping = {0: "Active", 1: "At-Risk", 2: "Churned"}
        status = mapping.get(churn_id, "Unknown")

        predicted_clv = float(clv_pipe.predict(features_df)[0])

        strategy = get_strategy(churn_id, churn_prob, predicted_clv)
        log_entry = {
            "customer_id": request.customer_id,
            "city": request.city,
            "gender": request.gender,
            "age": request.age,
            "lifetime_spend": request.lifetime_spend,
            "total_orders": request.total_orders,
            "total_returns": request.total_returns,
            "avg_rating": request.avg_rating,
            "customer_tenure_days": features_df['customer_tenure_days'].iloc[0],
            "customer_segment": request.customer_segment,

            "churn_status": status,
            "probability": churn_prob,
            "clv": predicted_clv,
            "strategy": strategy,
            "timestamp": datetime.now()
        }

        results_df = pd.DataFrame([log_entry])
        results_df.to_sql('realtime_logs', engine, if_exists='append', index=False)

        expert_advice = get_ai_strategy(request.dict(), status, round(predicted_clv, 2))

        return {
            "status": "success",
            "prediction": {
                "churn_status": status,
                "churn_probability": f"{churn_prob:.2%}",
                "predicted_lifetime_value": round(predicted_clv, 2),
                "strategy": strategy,
                "expert_advice": expert_advice
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_batch")
async def predict_batch(requests: List[Dict[str, Any]]):
    try:
        input_df = pd.DataFrame(requests)
        
        features_df = engineer_features_for_api_batch(input_df)
        
        churn_ids = churn_pipe.predict(features_df)
        churn_probs = churn_pipe.predict_proba(features_df).max(axis=1)
        clv_preds = clv_pipe.predict(features_df)
        
        mapping = {0: "Active", 1: "At-risk", 2: "Churned"}
        
        results = []
        for i in range(len(input_df)):
            results.append({
                "customer_id": str(input_df.iloc[i].get("customer_id", f"User_{i}")),
                "churn_status": mapping.get(int(churn_ids[i]), "Unknown"),
                "churn_probability": f"{churn_probs[i]:.2%}",
                "predicted_clv": round(float(clv_preds[i]), 2)
            })
            
        return {"status": "success", "results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/customer/{customer_id}")
async def update_customer(customer_id: str, updated_data: dict = Body(...)):
    try:
        # 1. Update the 'final_features' table in PostgreSQL
        # We use a simple SQL update here
        columns = ", ".join([f"{key} = :{key}" for key in updated_data.keys()])
        query = text(f"UPDATE final_features SET {columns} WHERE customer_id = :customer_id")
        
        with engine.connect() as conn:
            conn.execute(query, {**updated_data, "customer_id": customer_id})
            conn.commit()

        # 2. Re-run Prediction Logic
        # We fetch the newly updated row to ensure feature engineering is fresh
        df_updated = pd.read_sql(f"SELECT * FROM final_features WHERE customer_id = '{customer_id}'", engine)
        
        # Process and Predict (Reuse your engineering & model logic)
        features_df = engineered_features(df_updated.to_dict(orient='records')[0])
        new_churn = int(churn_pipe.predict(features_df)[0])
        new_clv = float(clv_pipe.predict(features_df)[0])

        update_pred_query = text("""
            UPDATE customer_predictions 
            SET predicted_churn_id = :churn, predicted_clv = :clv 
            WHERE customer_id = :customer_id
        """)
        with engine.connect() as conn:
            conn.execute(update_pred_query, {"churn": new_churn, "clv": new_clv, "customer_id": customer_id})
            conn.commit()

        return {"status": "success", "message": f"Customer {customer_id} updated and re-predicted."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_expert")
async def ask_expert(customer_data: dict, user_query: str):
    # This combines the customer's data with the user's specific question
    context = f"""
    Customer Context:
    - Status: {customer_data.get('churn_status')}
    - Value: ${customer_data.get('clv')}
    - Behavior: {customer_data.get('total_orders')} orders
    
    Question: {user_query}
    """
    
    # Call your Groq function with the new context
    answer = get_custom_response(context)
    return {"answer": answer}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

