FROM python:3.11-slim
WORKDIR /app
COPY dns_stress.py .
COPY domains.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        libc-dev \
        musl-dev \
    && pip install aiodns \
    && apt-get remove -y gcc libc-dev musl-dev \
    && apt-get autoremove -y \
    && apt-get clean

CMD ["python", "dns_stress.py"]
