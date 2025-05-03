from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()


from pathlib import Path

# Force load the .env file manually from current directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
# ✅ DEBUG - Confirm environment variable loading
print("[DEBUG] ASTRA_ENDPOINT =", os.getenv("ASTRA_ENDPOINT"))
print("[DEBUG] ASTRA_DB_TOKEN =", os.getenv("ASTRA_DB_TOKEN")[:8], "...")  # Safe preview
# Debug print (temporarily)
print("ENV DEBUG -> ASTRA_ENDPOINT =", os.getenv("ASTRA_ENDPOINT"))

ENDPOINT = os.getenv("ASTRA_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_TOKEN")

if not ENDPOINT or not TOKEN:
    raise ValueError("Environment variables ASTRA_ENDPOINT or ASTRA_DB_TOKEN are not set.")
@st.cache_resource
def get_db():
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db

db = get_db()
collection_names = ["personal_data", "notes"]

for collection in collection_names:
    try:
        db.create_collection(collection)
    except:
        pass
    
personal_data_collection = db.get_collection("personal_data")
notes_collection = db.get_collection("notes")