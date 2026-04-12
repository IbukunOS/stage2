import os
import subprocess
import sys

BACKUP_DIR = "/app/backups"
DB_NAME = "remotehustle"
HOST = "mongodb"

def run_restore(backup_file):
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} not found.")
        return

    print(f"Restoring {DB_NAME} from {backup_file}...")
    
    # Use mongorestore for restore
    cmd = [
        "mongorestore",
        f"--host={HOST}",
        f"--nsInclude={DB_NAME}.*",
        f"--archive={backup_file}",
        "--gzip",
        "--drop" # Drop existing data before restore
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Restore successful from {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Restore failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python restore.py <path_to_backup_file>")
        # Try to find the latest backup automatically
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("backup_")])
        if backups:
            latest = os.path.join(BACKUP_DIR, backups[-1])
            print(f"No file specified. Using latest: {latest}")
            run_restore(latest)
        else:
            print("No backups found in " + BACKUP_DIR)
    else:
        run_restore(sys.argv[1])
