from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection (Railway)
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Message saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True)