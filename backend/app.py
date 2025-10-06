import os
import subprocess
from fastapi import FastAPI, HTTPException
from utils import get_mongo_db, assert_api_key

app = FastAPI()

db = get_mongo_db()

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/process-data")
def process_data(api_key: str):
    # Validate key
    assert_api_key(api_key)

    # Path to input file, relative to project root mount inside container
    input_file = "processor/ingest_data/raw/input.xlsx"

    command = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/project",
        "-w", "/project/processor",
        "course-data-processor",
        "--input", input_file
    ]

    try:
        subprocess.run(command, check=True)
        return {"status": "success", "message": "Processed and stored"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

@app.get("/courses")
def get_courses():
    courses = list(db.courses.find({}, {"_id": 0}))
    return {"data": courses}
