import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# --- Explicitly load the .env file from the project's root directory ---
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Connection Details from Environment Variables ---
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# --- Database Connection ---
# Check if all variables are loaded before attempting to connect
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("❌ Error: Missing one or more database connection environment variables.")
    print("Please check your .env file in the project root.")
else:
    try:
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        # --- Data Loading ---
        data_dir = 'data'
        files_to_load = {
            'claims': 'claims_data.csv',
            'policies': 'customer_policy_data.csv',
            'identity_protection': 'identity_protection_data.csv',
            'trips': 'telematics_driving_data.csv'
        }

        for table_name, file_name in files_to_load.items():
            file_path = os.path.join(data_dir, file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                print(f"  - Read {len(df)} rows from {file_name}.")
                print(f"🔄 Loading {file_name} to 'raw.{table_name}' table...")
                # This will now load directly into your manually created 'raw' schema
                df.to_sql(table_name, engine, if_exists='replace', index=False, schema='raw')
                print(f"✅ Successfully loaded {file_name}!")
            else:
                print(f"⚠️ Warning: {file_name} not found in {data_dir}")

        print("\nAll data loaded successfully! 🎉")

    except Exception as e:
        print(f"❌ An error occurred: {e}")