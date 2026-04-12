# Remote Hustle – Stage 2 Task: DevOps & Infrastructure

**Student ID:** DevOps_Infrastructure_Setup
**Project Name:** Remote Hustle Live Infrastructure
**URL:** `https://<YOUR_EC2_IP>`

---

## 1. Hosting & Deployment Setup

### Hosting Environment
*   **Provider:** AWS EC2
*   **Instance Type:** t2.micro (Ubuntu 22.04 LTS)
*   **Infrastructure:** Dockerized environment (Nginx + Flask + MongoDB 4.4)
*   **Optimization:** Added 2GB Swap space for t2.micro build stability.

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
*   **Type:** Daily Automated & Manual Database Backups (MongoDB).
*   **Mechanism:** A Cron job runs inside the `app` container every midnight.
*   **Script:** `scripts/backup.py` uses `mongodump` with Gzip compression.
*   **Storage:** Backups are stored in a private directory `/app/backups`, which is mounted to a host volume `./backups` for persistence.

### Recovery & Testing
The system includes a manual restore feature to verify backup integrity.
*   **Restore Script:** `scripts/restore.py` uses `mongorestore` with the `--drop` flag to ensure a clean state.
*   **UI Features:**
    1.  **Manual Backup:** Trigger a snapshot instantly from the UI.
    2.  **Download:** Save `.gz` backups locally for off-site storage.
    3.  **Restore:** Select a backup and click "Restore" to overwrite the current database.

### Screenshot Deliverables (How to obtain)
1.  **Backup Config:** Show `docker-compose.yml` volumes and the cron job in `Dockerfile`.
2.  **Backup List:** Screenshot the "Backup & Recovery" table in the live UI.
3.  **Restore Success:** Screenshot the "Successfully restored" alert message after clicking Restore.

---

## 3. Security Implementation

### SSL Certificate
*   **Method:** Self-signed SSL Certificate (configured for `sslip.io` or direct IP).
*   **Encryption:** 2048-bit RSA key.
*   **Nginx Config:** Nginx is configured to redirect all HTTP traffic (Port 80) to HTTPS (Port 443).

### Access Control & User Roles (RBAC)
*   **Authentication:** Session-based Basic Auth via UI login box.
*   **Roles:**
    *   `admin`: Full access (Generate Data, Manual Backup, Restore, Download).
    *   `staff`: Read-only access (View Data only).
*   **Security:** Unauthorized actions (e.g., Guest trying to Backup) are rejected with a 401/403 status.

### Firewall & Network Security
*   **AWS Security Group:** Only ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) are open.
*   **Database Isolation:** MongoDB is NOT exposed to the internet. It only communicates with the Flask app within the internal Docker `app-network`.

---

## 4. Usage Instructions

1.  **Access:** Open `http://<EC2_IP>`. You will be redirected to HTTPS.
2.  **Login:** Enter `admin` / `admin123` in the Session Authentication box and click "Set Session Role".
3.  **Generate:** Click "Generate 10 Random Items" to populate the database.
4.  **Backup:** Click "Run Manual Backup" to create a timestamped snapshot.
5.  **Download:** Click "Download" to save a backup `.gz` file locally.
6.  **Restore:** Select a backup from the list and click "Restore" to revert to that state.

---

## 5. Branching Strategy (Bonus)
We implemented a **Staging vs Production** workflow:
*   `main` branch: Deploys to the Production EC2.
*   `staging` branch: Deploys to a Staging EC2/Environment for testing before merging to production.
