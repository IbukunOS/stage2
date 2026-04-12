FROM python:3.11-slim

WORKDIR /app

# Install dependencies and MongoDB Tools directly from repo
# This is lighter than pulling a 700MB mongo:latest image
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    cron \
    && wget -qO- https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg \
    && echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list \
    && apt-get update && apt-get install -y \
    mongodb-database-tools \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Setup a simple backup cron job
RUN echo "0 0 * * * /usr/bin/python3 /app/scripts/backup.py >> /var/log/cron.log 2>&1" > /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron

RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 5000

CMD ["/app/scripts/entrypoint.sh"]
