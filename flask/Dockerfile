# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=postgres
ENV POSTGRES_HOST=db-service
ENV POSTGRES_PORT=5432

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
