import pandas as pd

def transform_data(cust, ord):

    # cust, ord = extract_data()
    print("\n--------------------------------------------------")
    print("[TRANSFORM] Begin")
    print("--------------------------------------------------")

    print("--------------------------")
    print("[Transform] customers table")
    print("--------------------------")

    clean_cust = cust.copy()

    print(f"\n Fixing data types in the column: \n {clean_cust.info()}")

    # Fixing data types
    # ---------------------------------------------------------------------------------
    clean_cust['full_name'] = clean_cust['full_name'].astype('string')
    clean_cust['city'] = clean_cust['city'].astype('string')
    clean_cust['gender'] = clean_cust['gender'].astype('string')
    clean_cust['customer_segment'] = clean_cust['customer_segment'].astype('category')
    clean_cust['phone'] = pd.to_numeric(clean_cust['phone'], errors='coerce').astype('Int64')
    clean_cust['age'] = pd.to_numeric(clean_cust['age'], errors='coerce').astype('Int64')
    clean_cust['registration_date'] = pd.to_datetime(clean_cust['registration_date'], errors='coerce')
    clean_cust['gender'] = clean_cust['gender'].str.strip().str.title()
    
    print("Column data type fixed.")
    print(f"[TRANSFORM] column info: \n {clean_cust.info()}")
    # ---------------------------------------------------------------------------------


    # Malinformed Gender column fix
    # ---------------------------------------------------------------------------------
    print(f"[BEFORE TRANSFORM] gender column info: ")
    print(clean_cust['gender'].value_counts())

    gender_map = {
        'M': 'Male', 'F': 'Female',
        'Male ': 'Male', 'Female ': 'Female',
        'N/A': None, 'Na': None
    }
    clean_cust['gender'] = clean_cust['gender'].replace(gender_map)
    clean_cust['gender'] = clean_cust['gender'].fillna('Unknown')
    clean_cust['gender'].value_counts()

    print(f"[AFTER TRANSFORM] gender column info:")
    print(clean_cust['gender'].value_counts())
    # ---------------------------------------------------------------------------------


    # Malinformed Age column fix
    # ---------------------------------------------------------------------------------
    print("")
    clean_cust['age'] = clean_cust['age'].where(clean_cust['age'].between(16, 80), other=pd.NA)
    age_median = clean_cust['age'].median()
    print(f"Median age after calculation is {age_median}")
    clean_cust['age'] = clean_cust['age'].fillna(age_median)
    clean_cust['age']
    # ---------------------------------------------------------------------------------

    # Fixing the remaining columns
    # ---------------------------------------------------------------------------------

    # Phone
    clean_cust['phone_available'] = clean_cust['phone'].where(
        clean_cust['phone'].astype(str).str.match(r'^[6-9]\d{9}$', na=False),
        other=pd.NA
    )
    clean_cust['phone_available'] = clean_cust['phone_available'].notna().astype(int)

    # Email
    valid_email_mask = (
        clean_cust['email'].notna() &
        clean_cust['email'].str.contains('@', na=False) &
        ~clean_cust['email'].str.contains('@@', na=False)
    )
    clean_cust['email'] = clean_cust['email'].where(valid_email_mask, other=pd.NA)
    clean_cust['email_available'] = clean_cust['email'].notna().astype(int)

    # City
    clean_cust['city_available'] = clean_cust['city'].notna().astype(int)
    obj_cols = clean_cust.select_dtypes(include='object').columns
    clean_cust[obj_cols] = clean_cust[obj_cols].astype('string')
    # ---------------------------------------------------------------------------------
    
    # ---------------------------------------------------------------------------------
    print("--------------------------")
    print("[Transform] orders table")
    print("--------------------------")

    clean_ord = ord.copy()

    print("\nFixing data types: ")
    clean_ord['order_timestamp'] = pd.to_datetime(clean_ord['order_timestamp'], errors='coerce')
    clean_ord['delivery_days'] = pd.to_numeric(clean_ord['delivery_days'], errors='coerce').astype('Int64')

    for col in ['category', 'payment_method', 'order_status', 'device_type']:
        clean_ord[col] = clean_ord[col].astype('category')
    
    print(f"\n {clean_ord.info()}")
    
    # Feature Engineering
    clean_ord['total_price'] = clean_ord['quantity'] * clean_ord['unit_price']
    clean_ord['discount_amt'] = clean_ord['total_price'] - clean_ord['final_amount']
    clean_ord['total_revenue'] = clean_ord['final_amount'] + clean_ord['shipping_cost']

    # Handling null values ['payment_method', 'delivery_days', 'rating', 'device_type']
    clean_ord['payment_method'] = clean_ord['payment_method'].cat.add_categories('Unknown')
    clean_ord['payment_method'] = clean_ord['payment_method'].fillna('Unknown')
    clean_ord['device_type'] = clean_ord['device_type'].cat.add_categories('Unknown')
    clean_ord['device_type'] = clean_ord['device_type'].fillna('Unknown')


    return clean_cust, clean_ord
