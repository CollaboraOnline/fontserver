# Copyright the Collabora Online contributors.
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Use a lightweight Python base image
FROM python:3.9-slim

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3-dev build-essential curl && \
    pip install -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy the application script
COPY fontserver.py .

# Copy  SSL certificate
COPY server.crt .
COPY server.key .

# Expose the HTTP port
EXPOSE 5000

# Command to run the application
CMD ["python3", "fontserver.py"]

