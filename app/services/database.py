import duckdb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DUCKDB_PATH = os.getenv("DUCKDB_PATH")

if not DUCKDB_PATH:
    raise ValueError("Database path is not set. Check your .env file.")

def get_db_connection():
    return duckdb.connect(database=DUCKDB_PATH, read_only=True)
