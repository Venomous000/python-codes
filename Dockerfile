FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip git curl && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set workdir
WORKDIR /app

# Copy your project
COPY . .
# Create virtual environment
RUN python3 -m venv /opt/venv

# Use the virtual environment's pip
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install uv

# Optionally set PATH so the virtualenv python is default
ENV PATH="/opt/venv/bin:$PATH"

# Default shell
CMD ["bash"]
