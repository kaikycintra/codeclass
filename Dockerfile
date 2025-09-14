# -----------------------------------------------------------------------------
#                           Base Build Image
# -----------------------------------------------------------------------------

FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Install python dependencies
COPY pyproject.toml uv.lock ./
RUN uv export --format requirements.txt -o requirements.txt
RUN uv pip install --system -r requirements.txt

# -----------------------------------------------------------------------------
#                               Dev Image
# -----------------------------------------------------------------------------

FROM python:3.13-slim AS development

# Set working directory
WORKDIR /app

# Copy installed python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Copy project files
COPY servidor/ .

# Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Expose the port the app runs on
EXPOSE 8000

# Run server with hot reload
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
