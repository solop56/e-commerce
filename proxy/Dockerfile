# Use the specified Nginx base image
FROM nginxinc/nginx-unprivileged:1.25.2-alpine

# Set the maintainer label for clarity
LABEL maintainer="solopdev.com"

# Copy Nginx configuration templates and uwsgi_params
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params

# Copy the run.sh script to the root directory
COPY ./run.sh /run.sh

# Define environment variables for Nginx and application ports/hosts
ENV LISTEN_PORT=8000
ENV LISTEN_HOST=app
ENV APP_PORT=9000

# Switch to root user for system-level operations
USER root

# Create static volume directory, set permissions, and ownership
# Ensure default.conf exists and has correct permissions/ownership
# Make run.sh executable
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# Declare /vol/static as a volume for persistent storage
VOLUME /vol/static

# Switch back to the non-privileged nginx user for security
USER nginx

# Set the command to execute when the container starts
CMD ["/run.sh"]
