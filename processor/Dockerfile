FROM python:3.11-slim

WORKDIR /processor

# Copy requirements from project root
COPY requirements.txt /processor/requirements.txt
RUN pip install --no-cache-dir -r /processor/requirements.txt

# Copy the processor code
COPY processor/ingest_data /processor/ingest_data

# Default command
ENTRYPOINT ["python", "ingest_data/process_course_data.py"]