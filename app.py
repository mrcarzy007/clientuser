from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "tasks.db"

# Database Initialization
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Home Route
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to ProjectFour Task API",
        "version": "1.0.0",
        "status": "Running inside Docker & EKS"
    })

# Health Check Route (For Kubernetes/LoadBalancer)
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# 1. GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "title": row[1], "completed": bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return jsonify({"tasks": tasks})

# 2. POST a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (data['title'],))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"message": "Task added", "id": task_id}), 201

# 3. DELETE a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    
    if rows_deleted == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)