from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_to_db
from scripts.views import create_views, get_data_from_views
from src.feature import feature_engineering
from src.model import train_model
from src.predict import run_predictions

from pathlib import Path
import os
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
db_url = os.getenv("DB_URL")

engine = create_engine(db_url)
path = Path(__file__).parent/"sql"/"07.views.sql"

if __name__ == "__main__":

    # cust, ord = extract_data()
    # clean_cust, clean_ord = transform_data(cust, ord)
    # load_to_db(
    #     clean_cust,
    #     clean_ord
    # )
    # create_views(engine=engine, file_path=path)
    df_cust, df_ord = get_data_from_views(engine)
    
    df_final = feature_engineering(df_cust, df_ord)
    df = train_model(df_final)
    run_predictions()