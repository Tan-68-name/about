from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Railway MySQL connection (use env variables in Render)
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    cursor = db.cursor()

    query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    db.commit()

    cursor.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))