from flask import Flask, jsonify
import sqlite3
from parser import analyze_auth_logs

app = Flask(__name__)
DB_NAME = "security_logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            failure_count INTEGER NOT NULL,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/api/scan', methods=['POST'])
def run_scan():
    threats = analyze_auth_logs('auth_sample.log')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for threat in threats:
        cursor.execute(
            "INSERT INTO security_alerts (ip_address, failure_count) VALUES (?, ?)",
            (threat['ip'], threat['failures'])
        )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"status": "success", "threats_logged": len(threats), "data": threats})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_alerts ORDER BY detected_at DESC;")
    rows = cursor.fetchall()
    alerts = [dict(row) for row in rows]
    cursor.close()
    conn.close()
    
    return jsonify({"alerts": alerts})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)