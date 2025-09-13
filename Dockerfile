# Stage 1: Base build stage (for now)
FROM python:3.12.11-slim

# Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Set working dir
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app to app folder
COPY  servidor/ .

# Expose the Django port
EXPOSE 8000

# Run Development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]