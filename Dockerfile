# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
ENV PYTHONPATH=/app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install pip-tools for dependency management
RUN pip install --upgrade pip

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose port 8000
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
