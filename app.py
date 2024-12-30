from flask import Flask, jsonify, render_template, request
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',      # Replace with your DB host
    'database': 'testdb',     # Replace with your database name
    'user': 'testuser',       # Replace with your username
    'password': 'password'    # Replace with your password
}

# Connect to PostgreSQL Database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    return conn

# API Endpoint to Get Users
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM users')
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users)
    elif request.method == 'POST':
        new_user = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name) VALUES (%s) RETURNING id, name', (new_user['name'],))
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(user)

# HTML Page to Display Users
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
