#!/bin/sh

# This script is configured to exit immediately if any command within it fails.
# The `set -e` command ensures that the script stops execution upon encountering an error,
# which helps prevent unintended behavior or further errors caused by failed commands.
set -e

# This script is used to configure and run an Nginx server for the e-commerce proxy.
# 
# Steps:
# 1. The `envsubst` command substitutes environment variables in the Nginx configuration
#    template file (`/etc/nginx/default.conf.tpl`) and writes the output to the 
#    Nginx configuration directory (`/etc/nginx/conf.d/default.conf`).
# 2. The `nginx` command starts the Nginx server in the foreground with the `daemon off` 
#    directive, ensuring it runs as the main process.
#
# Prerequisites:
# - Ensure that the `/etc/nginx/default.conf.tpl` template file exists and contains 
#   placeholders for environment variables.
# - Verify that the necessary environment variables are set before running this script.
# - Ensure that Nginx is installed and properly configured on the system.
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;' 