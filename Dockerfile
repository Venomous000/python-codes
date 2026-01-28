# Use official Python image as base
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into container
COPY . /app

# Install dependencies (if you have any, for now skip if none)
# RUN pip install --no-cache-dir -r requirements.txt

# Default command when container starts
CMD ["bash"]
