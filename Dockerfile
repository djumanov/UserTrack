# Use the official Python image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Make sure the init.sh script is executable
RUN chmod +x scripts/init.sh

# Expose the port on which Django will run
EXPOSE 8000

# Run the initialization script
ENTRYPOINT ["scripts/init.sh"]
