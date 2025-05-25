# This Dockerfile is designed to build a Python application image,
# optimized for both development and production environments.
# It leverages a multi-stage approach for efficient dependency management
# and image size reduction, all based on a lightweight Alpine Linux.

# --- Base Image ---
    FROM python:3.13-alpine
    # Uses the python:3.13-alpine base image for a small and efficient footprint.
    
    # --- Metadata ---
    LABEL maintainer="solopdev.com"
    # Sets a metadata label to indicate the maintainer of this Dockerfile.
    
    # --- Environment Variables ---
    ENV PYTHONUNBUFFERED=1
    # Ensures Python's output (stdout/stderr) is unbuffered,
    # making logs appear in real-time, crucial for monitoring and debugging.
    ENV PATH="scripts:/py/bin:$PATH"
    # Modifies the system's PATH.
    # - 'scripts': Allows direct execution of scripts placed in the /scripts directory.
    # - '/py/bin': Includes the Python virtual environment's executables.
    
    # --- Dependency Management & Build Process ---
    # Copy dependency lists early to leverage Docker's layer caching.
    COPY ./requirements.txt /tmp/requirements.txt
    COPY ./requirements.dev.txt /tmp/requirements.dev.txt
    # Copy utility scripts. These are added to PATH.
    COPY ./scripts /scripts
    
    # Build argument to conditionally install development dependencies.
    # Set to 'true' for development builds: docker build --build-arg DEV=true .
    ARG DEV=false
    
    # Multi-stage RUN command for setting up the environment and installing dependencies.
    RUN python -m venv /py && \
        # Create a Python virtual environment at /py to isolate dependencies.
        /py/bin/pip install --upgrade pip && \
        # Upgrade pip within the virtual environment.
    
        # Install essential runtime system dependencies using Alpine's apk.
        # --update: Updates the package lists.
        # --no-cache: Prevents apk from caching package index files.
        # postgresql-client: For interacting with PostgreSQL.
        # jpeg-dev: Development headers for JPEG support (e.g., for Pillow library).
        apk add --update --no-cache postgresql-client jpeg-dev && \
    
        # Install temporary build-time system dependencies.
        # --virtual .tmp-build-deps: Creates a virtual package for easy removal later.
        # build-base: Essential tools for compiling software (e.g., GCC).
        # postgresql-dev: Development headers for PostgreSQL (for database adapters).
        # musl-dev: Development headers for Musl C library (Alpine's libc).
        # zlib, zlib-dev: Libraries and headers for zlib compression.
        # linux-headers: Linux kernel headers, sometimes needed for compilation.
        apk add --update --no-cache --virtual .tmp-build-deps \
            build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    
        # Install core application dependencies into the virtual environment.
        /py/bin/pip install -r /tmp/requirements.txt && \
    
        # Conditionally install development dependencies if DEV build argument is 'true'.
        if [ "$DEV" = "true" ]; \
            then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
            fi && \
    
        # Clean up temporary files to reduce image size.
        rm -rf /tmp && \
    
        # Remove temporary build dependencies to keep the final image lean.
        apk del .tmp-build-deps
    
    # --- Application Code & Working Directory ---
    # Copy the application source code into the image.
    COPY ./app /app
    # Set the working directory for subsequent instructions and container runtime.
    WORKDIR /app
    
    # --- Port Exposure ---
    EXPOSE 8000
    # Informs Docker that the container will listen on port 8000 at runtime.
    # This is informational; use -p to publish the port when running.
    
    # --- User & Permissions Setup ---
    RUN adduser --disabled-password --no-create-home user && \
        # Create a new non-root user named 'user' for enhanced security.
        # No password and no home directory are created.
        mkdir -p /vol/web/media && \
        mkdir -p /vol/web/static && \
        # Create directories for static files and user-uploaded media (e.g., for Django).
        chown -R user:user /vol && \
        # Change ownership of /vol and its contents recursively to the 'user'.
        chmod -R 755 /vol && \
        # Set read/write/execute permissions for owner, read/execute for others on /vol.
        chmod -R +x /scripts
        # Make all files within the /scripts directory executable.
    
    # --- Container Execution ---
    USER user
    # Switch to the non-root 'user'. All subsequent instructions run as this user.
    
    CMD ["run.sh"]
    # Specifies the default command to execute when a container starts.
    # It will run 'run.sh' (which should be in /scripts, now in PATH).