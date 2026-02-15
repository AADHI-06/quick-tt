FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY timetable_system/ ./timetable_system/
COPY api/ ./api/

# Create empty timetable.db for init (will be lost on restart in Cloud Run but needed for startup)
# In production, use Cloud SQL.
ENV TT_DB_PASSWORD=placeholder

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
