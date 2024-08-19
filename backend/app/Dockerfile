# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory
WORKDIR /app


# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 7861

# Define the command to run the application
CMD ["python", "app.py"]
