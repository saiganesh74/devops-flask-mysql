from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="password123",
            database="testdb"
        )
        return "Connected to MySQL from Flask!!"
    except:
        return "Failed to connect to MySQL."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

