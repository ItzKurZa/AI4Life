import json
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
    client = MongoClient(mongo_uri, tls=True)
    return client

def get_mongo_db():
    """Return the MongoDB database object."""
    client = get_mongo_client()
    db_name = get_env_var("MONGO_DB")
    return client[db_name]

def insert_courses(json_path):
    """Insert or update structured course data (JSON tree) into MongoDB."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    db = get_mongo_db()

    if isinstance(data, dict):
        academic_year = data.get("academic_year", "unknown")
        result = db.course_trees.replace_one(
            {"academic_year": academic_year},
            data,
            upsert=True
        )
        print(f"🌳 Upserted course tree for academic year {academic_year}")
        return [result.upserted_id or academic_year]
    elif isinstance(data, list):
        result = db.courses.insert_many(data)
        print(f"✅ Inserted {len(result.inserted_ids)} flat course records")
        return result.inserted_ids
    else:
        raise ValueError("JSON must be a list or dictionary")

def assert_api_key(provided_key: str):
    """Validate the API key, raise if invalid."""
    real = get_env_var("API_KEY")
    if provided_key != real:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Invalid API key")

def get_host_mount_path():
    """
    Returns the correct host path for mounting depending on where the code runs.
    """
    if os.path.exists("/.dockerenv"):
        return os.environ.get("HOST_PROJECT_PATH", "/workspaces/codespaces-blank/backend")
    else:
        return os.path.join(os.getcwd(), "backend")