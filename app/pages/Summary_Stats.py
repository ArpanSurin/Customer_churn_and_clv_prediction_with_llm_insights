import os
import pandas as pd
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine



load_dotenv()

db_url = os.getenv("DB_URL")

if not db_url:
    raise ValueError("DB_URL not found in environment variables!")

engine = create_engine(db_url)

df = pd.read_sql("SELECT * FROM realtime_logs", engine)

churn_rate = (df['probability'] == 0).mean()
non_churn_rate = (df['probability'] == 1).mean()

st.title("📊 Summary Dashboard")

st.metric("Churn Rate", f"{churn_rate:.2%}")
st.metric("Non-Churn Rate", f"{non_churn_rate:.2%}")

st.subheader("Churn by Segment")

segment_df = df.groupby("churn_status")['probability'].value_counts(normalize=True).unstack()

st.bar_chart(segment_df)

st.subheader("Top 10 Cities by Churn")

city_df = df[df['churn_status'] == 'At-Risk']['city'].value_counts().head(10)

st.bar_chart(city_df)