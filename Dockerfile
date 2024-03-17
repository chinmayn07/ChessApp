# Use the official Python image as a base image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements file into the container at /app
COPY chess_moves.py /app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 6000

# Run the Python script
CMD ["python", "chess_moves.py"]
