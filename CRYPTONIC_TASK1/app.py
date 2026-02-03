from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "securekey123"

def get_db():
    return sqlite3.connect("users.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return "Invalid input"

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect("/dashboard")
        return "Login Failed"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(debug=True)