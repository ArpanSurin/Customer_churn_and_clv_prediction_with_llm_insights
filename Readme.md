# End-to-End Customer Churn Prediction & CLV Estimation with LLM insights

An end-to-end e-commerce data pipeline built in Python. This project covers raw data ingestion, data cleaning, feature engineering, machine learning for churn and CLV, a REST API backend, and a Streamlit-powered customer insights experience.

---

## 🚀 Project Summary

This Prediction ingests raw e-commerce customer and order data, cleans and transforms both tables, loads them into PostgreSQL, generates analytics-ready views, trains churn and customer lifetime value models, and exposes real-time prediction services through FastAPI and Streamlit.

---

## 📁 What’s Included

- `pipeline.py` — orchestration entry point for view generation, feature engineering, model training, and prediction
- `scripts/extract.py` — loads raw CSV files and validates dataset shape
- `scripts/transform.py` — cleans customers and orders, normalizes types, fixes malformed values, and adds engineered features
- `scripts/load.py` — loads cleaned tables into PostgreSQL using SQLAlchemy
- `scripts/views.py` — applies SQL view definitions and reads model-ready views
- `sql/` — A folder containing a set of sql queries answering business questions such as Revenue by category, contact coverage, conversion rate, segmentation, etc.
and a `views.sql` file that defines analytical SQL views for orders and customers
- `src/feature.py` — merges customer and order data, creates customer-level aggregates, and persists `final_features`
- `src/model.py` — trains churn and CLV models, evaluates candidates, and saves the best assemblies
- `src/predict.py` — batch prediction pipeline that writes results to `customer_predictions`
- `fastapi/main.py` — FastAPI application exposing a health check and a real-time prediction endpoint
- `fastapi/schemas.py` — request schema for POST prediction payloads
- `fastapi/utils.py` — runtime feature engineering for incoming API data
- `app/Real_Time_Prediction.py` — Streamlit live prediction UI
- `app/pages/Summary_Stats.py` — Streamlit summary analytics dashboard
- `app/pages/Batch_Prediction.py` — Streamlit batch prediction upload interface
- `models/` — saved model artifacts and encoder files
- `data/raw/` — source CSVs for customers and orders

---

## 📊 Dataset
The dataset is available on Kaggle:\
https://www.kaggle.com/datasets/arpanboassurin/shopflow-data


## 🧩 Architecture Overview

1. Raw data loads from `data/raw/customers.csv` and `data/raw/orders.csv`
2. Data is cleaned and validated in `scripts/extract.py` and `scripts/transform.py`
3. Cleaned tables are loaded into PostgreSQL by `scripts/load.py`
4. SQL views are created via `sql/07.views.sql` and `scripts/views.py`
5. Customer-level features are built in `src/feature.py`
6. Churn and CLV models are trained in `src/model.py`
7. Predictions are generated in `src/predict.py` and stored in the database
8. FastAPI serves real-time scoring through `/predict`
9. Streamlit delivers an interactive UI for business users
10. Groq LLM model integration  providing AI driven insights and action plan

---

## 📌 Detailed Components

### Data Ingestion & ETL

- `scripts/extract.py`
  - reads raw customer and order CSV files
  - prints row counts, data columns, and null summaries
- `scripts/transform.py`
  - standardizes customer demographics and order fields
  - converts types, fixes malformed gender and phone values, fills missing ages, and creates availability flags
  - computes order-level features such as `total_price`, `discount_amt`, and `total_revenue`
- `scripts/load.py`
  - loads cleaned `customers` and `orders` tables into PostgreSQL
  - uses chunked inserts with `method='multi'`

### SQL Analytics & Views

- `sql/07.views.sql`
  - defines `fact_orders` for order-level analytics
  - defines `dim_customers` for customer-level segmentation and churn labeling
- `scripts/views.py`
  - applies SQL view definitions to the database
  - reads the materialized views for downstream modeling

### Feature Engineering

- `src/feature.py`
  - merges customer and order data into a modeling dataset
  - creates aggregates like `total_orders`, `lifetime_spend`, `avg_order_value`, `return_rate`, and `orders_per_month`
  - computes tenure and recency features
  - saves the final dataset to PostgreSQL table `final_features`

### Machine Learning

- `src/model.py`
  - trains churn classifiers using Logistic Regression, Random Forest, Gradient Boosting, and XGBoost
  - trains CLV regressors using Linear Regression, Random Forest, and Gradient Boosting
  - selects the best churn model by F1 score and the best CLV model by RMSE
  - saves the chosen models and label encoder to `models/`
- `src/predict.py`
  - loads `final_features` from PostgreSQL
  - generates churn and CLV predictions for the customer dataset
  - persists predictions to `customer_predictions`

### API & Interface

- `fastapi/main.py`
  - serves a health check at `/`
  - serves customer prediction at `/predict`
- `fastapi/schemas.py`
  - validates incoming JSON payloads for real-time scoring
- `fastapi/utils.py`
  - builds runtime model features from API requests
- `app/Real_Time_Prediction.py`
  - Streamlit UI for entering customer details and receiving churn/CLV output
- `app/pages/Summary_Stats.py`
  - Streamlit dashboard summarizing churn statistics and segment behavior
- `app/pages/Batch_Prediction.py`
  - Streamlit concept for bulk CSV prediction upload

---

## ⚙️ Setup Instructions

### 1. Activate your environment

Windows:

```powershell
myenv\Scripts\activate
```

macOS / Linux:

```bash
source myenv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with your PostgreSQL connection string:

```env
DB_URL=postgresql://username:password@localhost:5432/customer_chrun_prediction
```

### 4. Run the pipeline

```bash
python pipeline.py
```

> Note: `pipeline.py` currently orchestrates view loading, feature engineering, model training, and prediction. To activate the raw extract/transform/load steps, uncomment those calls inside `pipeline.py`.

### 5. Start the FastAPI backend

```bash
python fastapi/main.py
```

### 6. Run the Streamlit app

```bash
streamlit run app/Real_Time_Prediction.py
```

---

## 🔧 Folder Structure

```
app/
├── Real_Time_Prediction.py
├── pages/
│   ├── Batch_Prediction.py
│   └── Summary_Stats.py

data/
└── raw/
    ├── customers.csv
    └── orders.csv

fastapi/
├── main.py
├── schemas.py
└── utils.py

models/

scripts/
├── extract.py
├── load.py
├── transform.py
└── views.py

sql/
├── 01.revenue_by_category.sql
├── 02.contact_coverage.sql
├── 03.customer_conversion_rate.sql
├── 04.customer_churn_risk.sql
├── 05.customer_segmentation.sql
├── 06.payment_method.sql
└── 07.views.sql

src/
├── feature.py
├── model.py
└── predict.py

notebooks/

pipeline.py
requirements.txt
Readme.md
```

---

## ✅ Notes

- `sql/07.views.sql` is the central SQL layer used to generate analytics-ready views from cleaned tables.
- The FastAPI app currently supports real-time scoring through `/predict`.
- Streamlit UI provides live prediction UX and summary analytics.
- `models/` contains trained pipeline artifacts for production scoring.

---

## 🎯 Built For

- ETL and data cleansing practice
- SQL analytics and business view creation
- Customer churn and CLV machine learning
- API model serving with FastAPI
- Interactive UX with Streamlit

## 🛠️ Tech Stack
Python · Pandas · PostgreSQL · SQLAlchemy · psycopg2 · Power BI · Scikit-Learn · Streamlit · FastAPI · Groq LLM
