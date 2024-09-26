FROM python:3.12-slim

# Update the package list and install netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Clean up APT cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /home/python/

# Copy project files
COPY --chown=1000:1000 ./client /home/python/client
COPY --chown=1000:1000 ./init-polaris.py /home/python/
COPY --chown=1000:1000 ./init.sh /home/python/init.sh
RUN chmod +x /home/python/init.sh

# Install poetry and set up the environment
RUN pip install poetry==1.5.0 psycopg2-binary && \
    cd client/python && \
    python3 -m poetry install && \
    pip install -e .

ENTRYPOINT [ "./init.sh" ]