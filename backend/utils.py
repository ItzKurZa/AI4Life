import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def get_env_var(name: str, default=None):
    """Helper to fetch environment variables, optionally with a default."""
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Environment variable {name} is not set")
    return val

def get_mongo_client():
    """Create and return a MongoClient based on env vars."""
    mongo_uri = get_env_var("MONGO_URI")
    client = MongoClient(mongo_uri)
    return client

def get_mongo_db():
    """Return the MongoDB database object."""
    client = get_mongo_client()
    db_name = get_env_var("MONGO_DB")
    return client[db_name]

def assert_api_key(provided_key: str):
    """Validate the API key, raise if invalid."""
    real = get_env_var("API_KEY")
    if provided_key != real:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Invalid API key")
