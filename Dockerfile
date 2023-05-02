FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app
# Set timezone
ENV TZ=Europe/Kyiv
# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# Install application dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application code
COPY app.py app.py

# Expose port
EXPOSE 8085

# Run the application
CMD ["python", "app.py"]
