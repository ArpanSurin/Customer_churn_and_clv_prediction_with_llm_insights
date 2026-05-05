import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/predict_batch"

st.set_page_config(page_title="Batch Predictions for customers", layout="wide")

st.write("Upload a CSV file containing customer data to predict in bulk.")

template = pd.DataFrame([{
    "customer_id": "CUST0050001",
    "age": 30,
    "gender": "Male",
    "city": "Delhi",
    "customer_segment": "Regular",
    "total_orders": 5,
    "lifetime_spend": 2000,
    "total_returns": 0,
    "avg_rating": 4.0,
    "registration_date": "2023-01-01",
    "last_order_date": "2024-01-01",
    "total_ratings": 20,
    "avg_discount_pct": 5.0,
    "avg_order_value": 400.0,
    "avg_delivery_days": 3.0,
    "phone_available": 1,
    "email_available": 1,
    "rating_rate": 0.8,
    "spend_per_order": 400.0,
    "orders_per_month": 1.7
}])

st.download_button("📥 Download CSV Template", template.to_csv(index=False), "template.csv")

st.title("📦 Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("Preview:", df.head())

    if st.button("Run Batch Prediction"):
        response = requests.post(
            API_URL,
            json=df.to_dict(orient="records")
        )

        if response.status_code == 200:
            result = response.json()
            results = result.get("results", [])

            if not results:
                st.error("No predictions returned from the API.")
            else:
                result_df = pd.DataFrame(results)
                st.success("Batch prediction completed!")
                st.dataframe(result_df)
                st.download_button(
                    "Download Results",
                    result_df.to_csv(index=False),
                    "batch_predictions.csv"
                )
        else:
            error_message = response.json().get("detail", response.text)
            st.error(f"Batch prediction failed: {error_message}")
