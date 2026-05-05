from pathlib import Path
from dotenv import load_dotenv
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, mean_squared_error
from tabulate import tabulate

# Pathing
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def train_model(df_final):
    print("\nTraining models...\n")

    df = df_final.copy()

    target_mapping = {'Active': 0, 'At-risk': 1, 'Churned': 2}
    df['churn_label'] = df['churn_status'].map(target_mapping)
    df['future_spend'] = df['lifetime_spend']

    df = df.drop(columns=['customer_id', 'last_order_date', 'registration_date', 'churn_status'], errors='ignore')

    le = LabelEncoder()

    y_churn = df['churn_label']
    X_churn = df.drop(columns=['churn_label', 'future_spend', 'days_since_last_order', 'lifetime_spend'], errors='ignore')

    clean_mask_churn = y_churn.notna()
    X_churn = X_churn[clean_mask_churn]
    y_churn = y_churn[clean_mask_churn]
    
    y_churn = le.fit_transform(y_churn) 
    
    y_clv = df['future_spend']
    X_clv = df.drop(columns=['future_spend', 'churn_label', 'lifetime_spend', 'avg_order_value', 'spend_per_order', 'days_since_last_order'], errors='ignore')
    
    clean_mask_clv = y_clv.notna()
    X_clv = X_clv[clean_mask_clv]
    y_clv = y_clv[clean_mask_clv]
    
    categorical_cols_churn = X_churn.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols_churn = X_churn.select_dtypes(include=['int64', 'float64']).columns.tolist()

    categorical_cols_clv = X_clv.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols_clv = X_clv.select_dtypes(include=['int64', 'float64']).columns.tolist()

    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor_churn = ColumnTransformer([
        ('num', numeric_transformer, numeric_cols_churn),
        ('cat', categorical_transformer, categorical_cols_churn)
    ])

    preprocessor_clv = ColumnTransformer([
        ('num', numeric_transformer, numeric_cols_clv),
        ('cat', categorical_transformer, categorical_cols_clv)
    ])


    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_churn, y_churn, test_size=0.2, stratify=y_churn, random_state=42
    )

    Xr_train, Xr_test, yr_train, yr_test = train_test_split(
        X_clv, y_clv, test_size=0.2, random_state=42
    )

    churn_models = {
        "Logistic": LogisticRegression(max_iter=1000),
        "RF": RandomForestClassifier(class_weight='balanced'),
        "GB": GradientBoostingClassifier(),
        "XGBoost": XGBClassifier(eval_metric='mlogloss')
    }

    results = []
    best_churn = None
    best_f1 = 0

    print("="*60)
    print("🚀 TRAINING CHURN MODELS")
    print("="*60)

    for name, model in churn_models.items():
        pipe = Pipeline([
            ('prep', preprocessor_churn),
            ('model', model)
        ])

        pipe.fit(Xc_train, yc_train)
        preds = pipe.predict(Xc_test)
        f1 = f1_score(yc_test, preds, average='macro')
        
        results.append({"Model": name, "F1-Score": f1})

        if f1 > best_f1:
            best_f1 = f1
            best_churn = pipe

    results_df = pd.DataFrame(results).sort_values(by="F1-Score", ascending=False)
    print(tabulate(results_df, headers='keys', tablefmt='psql', showindex=False))
    print(f"\n🏆 WINNER CHURN: {best_churn.named_steps['model'].__class__.__name__} (F1: {best_f1:.4f})")

    clv_models = {
        "Linear": LinearRegression(),
        "RF": RandomForestRegressor(),
        "GB": GradientBoostingRegressor()
    }

    clv_results = []
    best_clv = None
    best_rmse = float('inf')

    print("\n" + "="*60)
    print("💰 TRAINING CLV REGRESSION MODELS")
    print("="*60)

    for name, model in clv_models.items():
        pipe = Pipeline([
            ('prep', preprocessor_clv),
            ('model', model)
        ])

        pipe.fit(Xr_train, yr_train)
        preds = pipe.predict(Xr_test)
        rmse = np.sqrt(mean_squared_error(yr_test, preds))
        
        clv_results.append({"Model": name, "RMSE": rmse})

        if rmse < best_rmse:
            best_rmse = rmse
            best_clv = pipe

    clv_df = pd.DataFrame(clv_results).sort_values(by="RMSE", ascending=True)
    print(tabulate(clv_df, headers='keys', tablefmt='psql', showindex=False))
    print(f"\n🏆 WINNER CLV: {best_clv.named_steps['model'].__class__.__name__} (RMSE: {best_rmse:.2f})")

    MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
    MODEL_DIR.mkdir(exist_ok=True)

    joblib.dump(best_churn, MODEL_DIR / "best_churn_model.pkl")
    joblib.dump(best_clv, MODEL_DIR / "best_clv_model.pkl")
    joblib.dump(le, MODEL_DIR / "label_encoder.joblib")
    
    print(f"\n✅ All models saved successfully in: {MODEL_DIR}")

