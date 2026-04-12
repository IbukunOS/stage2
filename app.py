import os
import random
import string
import datetime
import subprocess
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, send_from_directory
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

# MongoDB Configuration
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', "mongodb://mongodb:27017/remotehustle")
mongo = PyMongo(app)

# Simple User Role management
USERS = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "role": "admin"
    },
    "staff": {
        "password": generate_password_hash("staff123"),
        "role": "staff"
    }
}

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth = request.authorization
            if not auth or not USERS.get(auth.username) or not check_password_hash(USERS[auth.username]['password'], auth.password):
                return jsonify({"message": "Authentication required"}), 401
            
            if role and USERS[auth.username]['role'] != role:
                return jsonify({"message": "Forbidden: insufficient permissions"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
@login_required()
def get_data():
    try:
        data = list(mongo.db.items.find({}, {'_id': 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate', methods=['POST'])
@login_required('admin')
def generate_data():
    try:
        count = int(request.args.get('count', 10))
        new_items = []
        for _ in range(count):
            item = {
                "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                "name": f"Item_{random.randint(1000, 9999)}",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": random.choice(["active", "pending", "completed"]),
                "value": round(random.uniform(10.0, 500.0), 2)
            }
            new_items.append(item)
        
        if new_items:
            mongo.db.items.insert_many(new_items)
        
        return jsonify({"message": f"Generated {count} items", "count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/backup/status', methods=['GET'])
@login_required('admin')
def backup_status():
    backup_dir = "/app/backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backups = [f for f in os.listdir(backup_dir) if f.endswith(".gz")]
    return jsonify({"backup_count": len(backups), "backups": sorted(backups, reverse=True)})

@app.route('/api/backup/download/<filename>', methods=['GET'])
@login_required('admin')
def download_backup(filename):
    backup_dir = "/app/backups"
    return send_from_directory(backup_dir, filename, as_attachment=True)

@app.route('/api/backup/restore/<filename>', methods=['POST'])
@login_required('admin')
def restore_backup(filename):
    backup_path = os.path.join("/app/backups", filename)
    if not os.path.exists(backup_path):
        return jsonify({"error": "Backup file not found"}), 404
    
    try:
        cmd = ["python", "scripts/restore.py", backup_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": f"Successfully restored from {filename}", "output": result.stdout})
        else:
            return jsonify({"error": "Restore failed", "details": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/backup/run', methods=['POST'])
@login_required('admin')
def run_backup_now():
    try:
        cmd = ["python", "scripts/backup.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return jsonify({"message": "Manual backup triggered", "output": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
