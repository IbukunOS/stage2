FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    mongodb-clients \
    cron \
    && rm -rf /var/lib/apt/lists/*

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
