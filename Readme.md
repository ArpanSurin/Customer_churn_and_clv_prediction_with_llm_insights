# ShopFlow Pipeline
An end-to-end ETL pipeline that extracts raw e-commerce data, cleans and transforms it using Python, and loads it into PostgreSQL for SQL-based business analysis and a Power BI dashboard.

## 📊 Dataset

The dataset is available on Kaggle:
https://www.kaggle.com/datasets/arpanboassurin/shopflow-data

---

## 💹 Dashboard

![Page 1]()\
![Page 2]()\
![Page 3]()


---

## Tech Stack
Python · Pandas · PostgreSQL · SQLAlchemy · psycopg2 · Power BI

---

## What It Does

```
Raw CSV Files  →  Python (Extract & Transform)  →  PostgreSQL  →  SQL Analysis  →  Power BI Dashboard
```

- Extracts raw data from CSV files and validates schema and shape
- Transforms and cleans 50,000 customer records and 1.5M orders — handling nulls, malformed values, outliers, type inconsistencies, and engineers new features
- Loads cleaned data into PostgreSQL in chunks using SQLAlchemy
- Answers business questions via SQL: customer churn risk, revenue by category, payment behaviour, contact data coverage, and regional segmentation
- Visualises findings in a Power BI dashboard across 5 pages: Business Overview, Customer Health, Geographic Intelligence, Revenue Quality, and Contact Coverage

---

## Why I Built This

Built to simulate how data moves in a production ETL environment — from messy raw sources through a modular cleaning pipeline into a structured, queryable database. The goal was to understand not just the tooling, but the decisions behind each step: when to impute vs flag nulls, how to engineer features that answer real business questions, and how Python and SQL complement each other in a real pipeline.

---

## Folder Structure

```
shopflow-pipeline/
│
├── pipeline.py              ← entry point
├── requirements.txt
├── .env.example           
├── .gitignore
│
├── scripts/
│   ├── __init__.py
│   ├── extract.py           ← loads CSVs, validates schema
│   ├── transform.py         ← cleaning and feature 
│   └── load.py              ← writes to PostgreSQL in chunks
│
├── sql/
│   ├── 01_revenue_by_category.sql
│   ├── 02_contact_coverage.sql
│   ├── 03_customer_conversion_rate.sql
│   ├── 04_customer_churn_risk.sql
│   ├── 05_customer_segmentation.sql
│   └── 06_payment_behaviour.sql
│
├── notebooks/
│   ├── customers.ipynb
│   └── orders.ipynb
│
├── dashboard/
│   ├── dashboard.pbix
│   ├── Page_1.png
│   ├── Page_2.png
│   └── Page_3.png
│
└── data/
    └── raw/
        ├── customers.csv
        └── orders.csv
```

---

## How to Run

**1. Clone the repo and set up the environment**
```bash
git clone https://github.com/ArpanSurin/Shopflow-pipeline.git
cd shopflow-pipeline

# Windows
myenv\Scripts\activate

# Mac/Linux
source myenv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure database credentials**
```bash
cp .env.example .env
# Open .env and fill in your PostgreSQL connection string
```

**4. Run the pipeline**
```bash
python pipeline.py
```

---

## Status
- [x] Data generation
- [x] Extract, Transform, Load pipeline
- [x] PostgreSQL loading
- [x] SQL business analysis
- [x] Power BI dashboard
