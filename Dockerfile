FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Create pdfs directory
RUN mkdir -p /app/pdfs

# Environment variables
ENV PDF_FOLDER_PATH=/app/pdfs
ENV API_PORT=8000
ENV API_HOST=0.0.0.0

# Expose port
EXPOSE 8000

# Run the application
CMD sh -c "uvicorn main:app --host ${API_HOST} --port ${API_PORT}"
