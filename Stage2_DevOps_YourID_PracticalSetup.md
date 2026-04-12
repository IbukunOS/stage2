# Remote Hustle – Stage 2 Task: DevOps & Infrastructure

**Student ID:** DevOps_Infrastructure_Setup
**Project Name:** Remote Hustle Live Infrastructure
**URL:** `https://<YOUR_EC2_IP>`

---

## 1. Hosting & Deployment Setup

### Hosting Environment
*   **Provider:** AWS EC2
*   **Instance Type:** t2.micro (Ubuntu 22.04 LTS)
*   **Infrastructure:** Dockerized environment (Nginx + Flask + MongoDB)

### Deployment Method: GitHub Actions (Auto-Deploy)
We implemented a CI/CD pipeline using GitHub Actions that automatically deploys code to the EC2 instance upon pushing to the `main` branch.

**Deployment Steps:**
1.  **Code Push:** Developer pushes to `main`.
2.  **SSH Connection:** GitHub Action connects to EC2 via SSH using secrets (`EC2_SSH_KEY`).
3.  **Pull & Rebuild:** The script pulls the latest code and runs `docker compose up -d --build`.
4.  **Health Check:** Nginx restarts and routes traffic to the updated Flask application.

**How to Setup Deployment:**
1.  Fork the repository.
2.  Add `EC2_HOST`, `EC2_USERNAME`, and `EC2_SSH_KEY` to GitHub Secrets.
3.  The workflow in `.github/workflows/deploy.yml` handles the rest.

---

## 2. Backup Implementation

### Backup Configuration
*   **Type:** Daily Automated Database Backups (MongoDB).
*   **Mechanism:** A Cron job runs inside the `app` container every midnight.
*   **Script:** `scripts/backup.py` uses `mongodump` with Gzip compression.
*   **Storage:** Backups are stored in a private directory `/app/backups`, which is mounted to a host volume `./backups` for persistence.

### Recovery & Testing
The system includes a manual restore feature to verify backup integrity.
*   **Restore Script:** `scripts/restore.py` uses `mongorestore` with the `--drop` flag to ensure a clean state.
*   **Verification:**
    1.  Generate random data in the UI.
    2.  Trigger a "Manual Backup".
    3.  Delete data or modify it.
    4.  Click "Restore" on the backup list.
    5.  Refresh data to confirm recovery.

### Screenshot Deliverables (How to obtain)
1.  **Backup Config:** Show `docker-compose.yml` volumes and `Dockerfile` cron lines.
2.  **Backup List:** Screenshot the "Backup & Recovery" section of the live website.
3.  **Restore Success:** Screenshot the "Successfully restored" alert message in the browser.

---

## 3. Security Implementation

### SSL Certificate
*   **Method:** Self-signed SSL Certificate (configured for `sslip.io` or direct IP).
*   **Encryption:** 2048-bit RSA key.
*   **Nginx Config:** Nginx is configured to redirect all HTTP traffic (Port 80) to HTTPS (Port 443).

### Access Control & User Roles
*   **Authentication:** Basic Auth implemented at the application level.
*   **Roles:**
    *   `admin`: Full access (Generate Data, Manual Backup, Restore, Download).
    *   `staff`: Read-only access (View Data only).
*   **Password Security:** Passwords are salted and hashed using `pbkdf2:sha256` via `werkzeug.security`.

### Firewall & Network Security
*   **AWS Security Group:** Only ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) are open.
*   **Database Isolation:** MongoDB is NOT exposed to the internet. It only communicates with the Flask app within the internal Docker `app-network`.

---

## 4. Usage Instructions

1.  **Access:** Open `http://<EC2_IP>`. You will be redirected to HTTPS.
2.  **Login:** Enter `admin` / `admin123` to manage the system.
3.  **Generate:** Click "Generate 10 Random Items" to populate the database.
4.  **Backup:** Click "Run Manual Backup" to create a timestamped snapshot.
5.  **Restore:** Select a backup from the list and click "Restore" to revert to that state.
6.  **Download:** Click "Download" to save the backup `.gz` file locally for off-site storage.

---

## 5. Branching Strategy (Bonus)
We implemented a **Staging vs Production** workflow:
*   `main` branch: Deploys to the Production EC2.
*   `staging` branch: Deploys to a Staging EC2/Environment for testing before merging to production.
