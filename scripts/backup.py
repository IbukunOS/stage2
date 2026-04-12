import os
import subprocess
import datetime

BACKUP_DIR = "/app/backups"
DB_NAME = "remotehustle"
HOST = "mongodb"

def run_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{BACKUP_DIR}/backup_{timestamp}.gz"
    
    # Ensure backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    print(f"Starting backup of {DB_NAME} to {backup_file}...")
    
    # Use mongodump for backup
    cmd = [
        "mongodump",
        f"--host={HOST}",
        f"--db={DB_NAME}",
        f"--archive={backup_file}",
        "--gzip"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Backup successful: {backup_file}")
        
        # Keep only last 7 backups (optional housekeeping)
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("backup_")])
        if len(backups) > 7:
            for b in backups[:-7]:
                os.remove(os.path.join(BACKUP_DIR, b))
                print(f"Removed old backup: {b}")
                
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    run_backup()
