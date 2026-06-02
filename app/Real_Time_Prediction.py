import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import create_engine
import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000/predict"

BASE_DIR = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(BASE_DIR)

db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

st.set_page_config(page_title="Customer Insights Pro", layout="wide")

with st.sidebar:    
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Team Members")
    st.markdown("**RA2211026050004 - Arpan Surin**")
    st.markdown("""
    **Computer Science & Technology with spec. in Artificial Intelligence and Machine Learning (AI & ML) A Section**
""")
    st.markdown("**SRM Institute of Science & Technology Tiruchirappalli**")
    st.markdown("---")



st.title("🚀 Real-Time Customer Churn & CLV Predictor")

st.markdown("This app predicts customer churn risk and estimated CLV based on input features. It also logs predictions for historical analysis and provides a customer 360° profile view.")

st.divider()

tab1, tab2, tab3 = st.tabs(["🎯 New Prediction", "📜 Prediction History", "🔍 Customer Deep-Dive"])

with tab1:
    # ... [Paste your existing Prediction Form logic here] ...
    st.subheader("Run New Analysis")
        
    st.markdown("Enter customer details below to generate a risk profile.")

    st.subheader("📋 Customer Details")
    with st.form("main_form"):
        
        customer_id = st.text_input("🆔 Customer ID", value="CUST0050001")

        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col3:
            city = st.text_input("City", value="Mumbai")

        col4, col5, col6 = st.columns(3)
        with col4:
            segment = st.selectbox("Customer Segment", ["New", "Regular", "Premium", "VIP", "Inactive"])
        with col5:
            total_orders = st.number_input("Total Orders", min_value=1, value=5)
        with col6:
            total_returns = st.number_input("Total Returns", min_value=0, value=0)
        
        col7, col8, col9 = st.columns(3)
        with col7:
            lifetime_spend = st.number_input("Lifetime Spend", min_value=0.0, value=1000.0)
        with col8:
            avg_discount_pct = st.number_input("Avg Discount %", min_value=0.0, value=10.5)
        with col9:
            avg_rating = st.number_input("Avg Rating", min_value=0.0, max_value=5.0, value=4.0)

        col10, col11, col12 = st.columns(3)
        with col10:
            reg_date = st.date_input("Registration Date", value=date(2023, 1, 1))
        with col11:
            last_date = st.date_input("Last Order Date", value=date.today())
        with col12:
            avg_delivery_days = st.number_input("Avg Delivery Days", min_value=0, value=3)

        st.markdown("<br>", unsafe_allow_html=True)

        submit = st.form_submit_button("Generate Prediction", width='stretch')

    if submit:
        payload = {
            "customer_id": customer_id,
            "age": age,
            "gender": gender,
            "city": city,
            "customer_segment": segment,
            "total_orders": total_orders,
            "lifetime_spend": lifetime_spend,
            "total_returns": total_returns,
            "avg_rating": avg_rating,
            "registration_date": str(reg_date),
            "last_order_date": str(last_date),
            "avg_discount_pct": avg_discount_pct,
            "avg_delivery_days": avg_delivery_days
        }

        try:
            # Call FastAPI
            with st.spinner("Analyzing customer behavior..."):
                response = requests.post(API_URL, json=payload)
                res_data = response.json()

            if response.status_code == 200:
                pred = res_data["prediction"]
                
                st.subheader(f"Analysis for: {customer_id}")
                strategy = pred["strategy"]
                
                col1, col2, col3 = st.columns(3)

                color_map = {
                    "Critical": "#FF0000",   # Pure Red
                    "Emergency": "#8B0000",  # Dark Red
                    "Save": "#FF4B4B",       # Streamlit Red
                    "Incentive": "#FFA500",  # Orange
                    "Nurture": "#FFD700",    # Gold/Yellow
                    "VIP": "#1E90FF",        # Dodger Blue
                    "Upsell": "#00FF7F",     # Spring Green
                    "Monitor": "#808080"     # Gray
                }

                # 2. Pick the color based on keywords in the strategy string
                theme_color = next((v for k, v in color_map.items() if k.lower() in strategy.lower()), "#7F8C8D")

                # 3. Enhanced HTML/CSS
                st.markdown(f"""
                    <div style="
                        padding: 25px; 
                        border-radius: 12px; 
                        background-color: #111; 
                        border-left: 8px solid {theme_color};
                        box-shadow: 2px 4px 10px rgba(0,0,0,0.3);
                        margin: 10px 0;
                    ">
                        <h5 style="margin:0; color: {theme_color}; text-transform: uppercase; letter-spacing: 1px;">
                            Target Strategy
                        </h5>
                        <h2 style="margin: 5px 0 15px 0; color: white; font-size: 24px;">
                            {strategy}
                        </h2>
                        <div style="display: flex; gap: 20px; border-top: 1px solid #333; padding-top: 15px;">
                            <div>
                                <p style="margin:0; font-size: 12px; color: #888;">CHURN STATUS</p>
                                <p style="margin:0; color: white; font-weight: bold;">{pred['churn_status']}</p>
                            </div>
                            <div>
                                <p style="margin:0; font-size: 12px; color: #888;">ESTIMATED CLV</p>
                                <p style="margin:0; color: white; font-weight: bold;">${pred['predicted_lifetime_value']:,.2f}</p>
                            </div>
                            <div>
                                <p style="margin:0; font-size: 12px; color: #888;">CHURN PROBABILITY</p>
                                <p style="margin:0; color: white; font-weight: bold;">{pred['churn_probability']}%</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("### 🤖 AI Business Consultant")
                st.info(pred["expert_advice"])

                with col1:
                    st.metric("Churn Risk", pred["churn_status"])
                with col2:
                    st.metric("Confidence", pred["churn_probability"])
                with col3:
                    st.metric("Predicted CLV", f"${pred['predicted_lifetime_value']:.2f}")
                
            else:
                st.error(f"Error: {res_data.get('detail', 'Unknown error')}")

        except Exception as e:
            st.error(f"Could not connect to Backend: {e}")
            print(e)


with tab2:
    st.header("Recent Predictions")
    if st.button("🔄 Refresh History"):
        try:
            # Query the log table
            history_df = pd.read_sql(
                "SELECT * FROM realtime_logs ORDER BY timestamp DESC LIMIT 10", con=engine)
            
            if not history_df.empty:
                # Display as a clean table
                st.dataframe(
                    history_df, 
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn("Date & Time"),
                        "clv": st.column_config.NumberColumn("Predicted CLV ($)"),
                        "strategy": "Action Plan"
                    },
                    width='stretch',
                    hide_index=True
                )
                
                # Option to download full history
                csv = history_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Full Logs", csv, "history.csv", "text/csv")
            else:
                st.info("No past predictions found in the database.")
        except Exception as e:
            st.error(f"Error fetching history: {e}")    

with tab3:
    st.header("Customer 360° Profile")
    search_id = st.text_input("Enter Customer ID to fetch full profile", placeholder="e.g. CUST0000001")

    if search_id:
        try:
            # Fetch joined data from your database
            query = f"SELECT * FROM realtime_logs WHERE customer_id = '{search_id}'"
            customer_data = pd.read_sql(query, engine)

            if not customer_data.empty:
                row = customer_data.iloc[0]
                
                row['avg_order_value'] = row['lifetime_spend'] / row['total_orders'] if row['total_orders'] > 0 else 0
                row['return_rate'] = row['total_returns'] / row['total_orders'] if row['total_orders'] > 0 else 0
                row['days_since_last_order'] = (pd.Timestamp.now() - pd.to_datetime(row['last_order_date'])).days if 'last_order_date' in row else None
                row['customer_tenure_days'] = row['customer_tenure_days'] if 'customer_tenure_days' in row else None

                # Layout for Profile
                col_left, col_right = st.columns([1, 2])
                
                with col_left:
                    st.metric("CustomerID", row['customer_id'])
                    
                with col_right:
                    # Demographics & Details
                    st.markdown(f"### **Customer Stats**")
                    st.write(f"**Location:** {row['city']} | **Gender:** {row['gender']} | **Age:** {row['age']}")
                    st.write(f"**Avg Order Value:** ${row['avg_order_value']:,.2f}$ | **Avg Rating:** {row['avg_rating']:.2f}" )
                    st.write(f"**Return Rate:** {row['return_rate']:.2%} | **Tenure Days:** {row['customer_tenure_days']} days | **Days Since Last Order:** {row['days_since_last_order']} days ")
                    
                    st.divider()
                    
                    # Prediction Data
                    st.markdown("### **AI Insights**")
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**Churn Prob:** {row['probability']:.2%}")
                    c2.write(f"**CLV Est:** ${row['clv']:,.2f}")
                    
                    # Mapping the ID to text
                    status_map = {0: "Active", 1: "At-risk", 2: "Churned"}
                    # c3.write(f"**Status:** {status_map.get(row['predicted_churn_id'], 'Unknown')}")
                    c3.write(f"**Status:** {status_map.get(row['churn_status'], 'Unknown')}")
                
            else:
                st.warning("No record found for that Customer ID.")
        except Exception as e:
            st.error(f"Search failed: {e}")
            st.divider()


    st.markdown("---")
    st.subheader("All Predicted Customers")
    all_data = pd.read_sql("SELECT * FROM realtime_logs LIMIT 100", index_col='customer_id', con=engine)
    st.dataframe(all_data, width='stretch')

st.markdown("---")

