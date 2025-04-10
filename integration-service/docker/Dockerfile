# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements
COPY src/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

# Copy application code
COPY src/ .

# Expose port
EXPOSE 5002

# Run the app
CMD ["python", "app.py"]
