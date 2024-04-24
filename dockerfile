# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set non-interactive installation mode
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies for Tkinter, Firefox, Xvfb
RUN apt-get update && apt-get install -y \
    tk \
    python3-tk \
    wget \
    firefox-esr \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Download and install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.30.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.30.0-linux64.tar.gz

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Configure the DISPLAY environment variable for Xvfb
ENV DISPLAY=:99

# Start Xvfb, then run the application
CMD Xvfb :99 -screen 0 1280x720x24 & python app.py

