from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# CREATE DATABASE AND TABLE
def userdb():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dob TEXT,
        phone TEXT,
        occupation TEXT,
        address TEXT,
        relationship TEXT,
        email TEXT,
        denomination TEXT
    )
    """)

    conn.commit()
    conn.close()


# RUN DATABASE FUNCTION
userdb()


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# FORM SUBMISSION
@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    dob = request.form.get("dob")
    phone = request.form.get("phone")
    occupation = request.form.get("occupation")
    address = request.form.get("address")
    relationship = request.form.get("relationship")
    email = request.form.get("email")
    denomination = request.form.get("denomination")

    # CONNECT TO DATABASE
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # INSERT DATA INTO TABLE
    cursor.execute("""
    INSERT INTO users (
        name,
        dob,
        phone,
        occupation,
        address,
        relationship,
        email,
        denomination
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        dob,
        phone,
        occupation,
        address,
        relationship,
        email,
        denomination
    ))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        name=name,
        dob=dob,
        phone=phone,
        occupation=occupation,
        address=address,
        relationship=relationship,
        email=email,
        denomination=denomination
    )


# DISPLAY ALL USERS
@app.route("/users")
def users():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # GET ALL USERS
    cursor.execute("SELECT * FROM users")

    all_users = cursor.fetchall()

    conn.close()

    return render_template(
        "users.html",
        users=all_users
    )


# RUN APP
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))