from flask import Flask, jsonify, render_template, request
import psycopg2
import os
import requests

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

# Function to get weather based on zipcode
def get_weather(zipcode):
    api_key = 'f87c58e4e2464211810191201243012'  # Replace with your weather API key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={zipcode}'
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data['current']['condition']['text']
    return 'Weather data not available'

# API Endpoint to Get Users
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, COALESCE(zipcode, \'84092\') FROM users')
        users = cur.fetchall()
        cur.close()
        conn.close()
        users_with_weather = [
            [user[0], user[1], user[2], get_weather(user[2])] for user in users
        ]
        return jsonify(users_with_weather)
    elif request.method == 'POST':
        new_user = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, zipcode) VALUES (%s, %s) RETURNING id, name, COALESCE(zipcode, \'84092\')', (new_user['name'], new_user.get('zipcode', '84092')))
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        user_with_weather = [user[0], user[1], user[2], get_weather(user[2])]
        return jsonify(user_with_weather)

# HTML Page to Display Users
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
