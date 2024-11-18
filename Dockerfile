FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    gcc \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
