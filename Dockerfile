FROM python:3.12-alpine

# Install needed packages (DNS lookups + pip building)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    py3-pip \
    bind-tools

# Set working directory
WORKDIR /app

RUN pip install aiodns


# Copy your script into the container
COPY ./ ./

# Install any Python dependencies if needed (example: dnspython if used)
# RUN pip install dnspython

# Command to run your script
CMD ["python", "/app/dns_stress.py"]
