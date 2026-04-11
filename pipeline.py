from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_to_db

if __name__ == "__main__":

    cust, ord = extract_data()
    clean_cust, clean_ord = transform_data(cust, ord)
    load_to_db(
        clean_cust,
        clean_ord
    )
