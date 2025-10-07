import os
import subprocess
from fastapi import FastAPI, HTTPException
from utils import get_mongo_db, assert_api_key, insert_courses

app = FastAPI()

db = get_mongo_db()

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/save-data")
def save_data(api_key: str):
    """Run the processor in Docker, then save resulting JSON to MongoDB."""
    # 1️⃣ Validate API key
    assert_api_key(api_key)

    # 2️⃣ Define input/output paths (relative to your project root)
    input_file = "processor/ingest_data/raw/input.xlsx"
    output_file = "processor/ingest_data/output/processed.json"

    # 3️⃣ Run the Docker container
    command = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/project",  # Mount current workspace
        "-w", "/project/processor",       # Work inside /processor
        "course-data-processor",
        "--input", input_file,
        "--output", output_file           # Make sure your processor supports this flag
    ]

    try:
        print("🚀 Running data processor...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        print("✅ Processor finished successfully.")
        print("🔍 stdout:", result.stdout)

        # 4️⃣ Verify that the JSON file exists
        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="Output JSON file not found after processing")

        # 5️⃣ Save processed data to MongoDB
        insert_courses(output_file)
        return {"status": "success", "message": "Processed and stored"}

    except subprocess.CalledProcessError as e:
        # Log stderr for debugging
        print("❌ Processor failed:", e.stderr)
        raise HTTPException(status_code=500, detail=f"Processing failed: {e.stderr}")

    except Exception as e:
        print("❌ Unexpected error:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses")
def get_courses():
    courses = list(db.courses.find({}, {"_id": 0}))
    return {"data": courses}
