# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Run the data ingestion script to build the vector store
RUN python ingestion_scripts/ingest_news.py

# Copy the startup script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Expose the ports for the backend and frontend
EXPOSE 8000
EXPOSE 8501

# Set the startup script as the command to run
CMD ["./start.sh"]