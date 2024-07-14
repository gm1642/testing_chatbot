FROM ollama/ollama:latest

# Update package lists and install Python3-pip
RUN apt-get update && apt-get install -y python3-pip

# Install Flask
RUN pip3 install Flask

# Copy the Flask app
COPY app.py /app/app.py

# Set the working directory
WORKDIR /app

# Expose the necessary port
EXPOSE 11434

# Run the Flask app
CMD ["python3", "app.py"]
