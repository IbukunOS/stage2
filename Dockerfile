FROM mongo:latest AS mongo-tools

FROM python:3.11-slim

WORKDIR /app

# Install cron and dependencies for mongo-tools (shared libraries)
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy mongodump and mongorestore from the mongo-tools stage
COPY --from=mongo-tools /usr/bin/mongodump /usr/bin/mongorestore /usr/bin/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/backups

# Setup a simple backup cron job
RUN echo "0 0 * * * /usr/bin/python3 /app/scripts/backup.py >> /var/log/cron.log 2>&1" > /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron

RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 5000

CMD ["/app/scripts/entrypoint.sh"]
