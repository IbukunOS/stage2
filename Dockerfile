FROM python:3.11-slim

WORKDIR /app

# Install dependencies and MongoDB Tools directly via .deb package
# This bypasses the repository signature issues in newer Debian versions
RUN apt-get update && apt-get install -y \
    wget \
    cron \
    && wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian12-x86_64-100.9.4.deb \
    && apt-get install -y ./mongodb-database-tools-debian12-x86_64-100.9.4.deb \
    && rm mongodb-database-tools-debian12-x86_64-100.9.4.deb \
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
