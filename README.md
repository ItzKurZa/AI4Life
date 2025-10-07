# Course Data Management System

A FastAPI-based backend system for processing, storing, and retrieving course information from Excel files. The system processes course data and organizes it by academic year, semester, cohort, and class, storing the results in MongoDB.

## Overview

This project provides a RESTful API that:
- Processes Excel files containing course information
- Extracts and normalizes course data
- Stores structured data in MongoDB
- Provides endpoints for data retrieval

## Architecture

The system consists of three main components:

1. **Backend API** (FastAPI): RESTful API for data processing and retrieval
2. **Data Processor**: Python script that converts Excel files to structured JSON
3. **MongoDB Database**: Document storage for course data

## Project Structure

```
.
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── utils.py              # Database and utility functions
│   ├── Dockerfile            # Backend container configuration
│   └── processor/
│       ├── Dockerfile        # Processor container configuration
│       └── ingest_data/
│           ├── process_course_data.py    # Data processing script
│           ├── raw/          # Input Excel files
│           └── cleaned/      # Output CSV and JSON files
├── docker-compose.yml        # Container orchestration
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- MongoDB 7+

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# MongoDB Configuration
MONGO_URI=your_mongodb_connection_string
MONGO_DB=your_database_name

# API Security
API_KEY=your_secure_api_key
```

## Installation

1. Clone the repository
2. Set up environment variables in `.env`
3. Build and start the containers:

```bash


docker compose up --build
```

This will start:
- MongoDB on port 27017
- Backend API on port 8000

## API Endpoints

### Health Check

```http
GET /
```

Returns a simple status message confirming the backend is running.

**Response:**
```json
{
  "message": "Backend running"
}
```

### Process and Save Course Data

```http
POST /save-data?api_key=YOUR_API_KEY
```

Processes an Excel file containing course information and stores the results in MongoDB.

**Process Flow:**
1. Validates API key
2. Runs the data processor Docker container
3. Converts Excel file to cleaned CSV and structured JSON
4. Stores the processed data in MongoDB

**Response:**
```json
{
  "status": "success",
  "message": "Processed and stored"
}
```

### Retrieve All Courses

```http
GET /courses
```

Returns all stored course data from MongoDB.

**Response:**
```json
{
  "data": [...]
}
```

## Data Processing

### Input Format

The system expects Excel files with course information in the following Vietnamese format:
- Sheet containing course data with headers in row 5
- Columns: Tên học phần, LT, TH, Tổng, Ghi chú, Lớp

### Output Format

The processor generates two outputs:

1. **CSV File**: Cleaned course data with English column names
2. **JSON File**: Structured data organized by:
   - Academic year
   - Semester
   - Cohort
   - Class

### JSON Structure

```json
{
  "academic_year": "2025-2026",
  "semesters": {
    "semester_1": {
      "19": {
        "19SE1": [
          {
            "course_name": "Course Name",
            "theory_credits": 3.0,
            "practical_credits": 1.0,
            "total_credits": 4.0,
            "note": "Optional note"
          }
        ]
      }
    }
  }
}
```

## Running the Data Processor Standalone

You can run the data processor independently:

```bash
docker run --rm \
  -v /path/to/backend:/app \
  -w /app/processor \
  course-data-processor \
  --input ingest_data/raw/input.xlsx \
  --sheet Sheet1 \
  --csv-output ingest_data/cleaned/output.csv \
  --json-output ingest_data/cleaned/output.json
```

## Class Expansion Logic

The system supports automatic class range expansion:

- `19SE1->SE5` expands to: `19SE1, 19SE2, 19SE3, 19SE4, 19SE5`
- `22SE1->2` expands to: `22SE1, 22SE2`

## Dependencies

### Backend
- FastAPI: Web framework
- Uvicorn: ASGI server
- PyMongo: MongoDB driver
- python-dotenv: Environment variable management

### Data Processor
- pandas: Data manipulation
- openpyxl: Excel file reading

## Security Considerations

- API key authentication for data processing endpoint
- MongoDB authentication enabled
- Environment variables for sensitive configuration
- Docker socket mounted with appropriate permissions

## Development

### Building Containers

Build individual containers:

```bash
# Backend API
docker build -t backend -f backend/Dockerfile .

# Data Processor
docker build -t course-data-processor -f backend/processor/Dockerfile .
```

### Running Locally

Start the FastAPI server:

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Processor Fails
- Check input file path is correct
- Verify Excel file format matches expected structure
- Review container logs for detailed error messages

### MongoDB Connection Issues
- Verify MONGO_URI is correct
- Ensure MongoDB container is running
- Check network connectivity between containers

### API Key Issues
- Confirm API_KEY is set in .env
- Verify the key is being passed correctly in requests

## License

This project is provided as-is for educational and internal use.