# Use Python 3.12 Alpine as base image for smaller size
FROM python:3.12-alpine

# Add metadata
LABEL maintainer="solopdev.com"
LABEL description="Development and testing environment for Python applications"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/py/bin:$PATH" \
    PYTHONPATH="/app"

# Install system dependencies and cleanup in one layer
RUN apk add --update --no-cache \
    postgresql-client \
    curl \
    git \
    && rm -rf /var/cache/apk/*

# Install build dependencies and cleanup in one layer
RUN apk add --update --no-cache --virtual .build-deps \
    build-base \
    postgresql-dev \
    musl-dev \
    python3-dev \
    && rm -rf /var/cache/apk/*

# Create and activate virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel

# Copy requirements files
COPY requirements.txt requirements.dev.txt /tmp/

# Install Python dependencies
RUN /py/bin/pip install -r /tmp/requirements.txt && \
    /py/bin/pip install -r /tmp/requirements.dev.txt && \
    rm -rf /tmp/*

# Create non-root user
RUN adduser --disabled-password --no-create-home --gecos "" user && \
    chown -R user:user /py

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=user:user ./app /app

# Switch to non-root user
USER user

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command (can be overridden)
CMD ["python", "-u", "gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]