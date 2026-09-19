from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "fitness_tracker_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "fitness.db")

# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Activities table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT NOT NULL,
            activity TEXT NOT NULL,
            duration INTEGER NOT NULL,
            steps INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        # Check if username already exists
        existing = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing:
            conn.close()
            return "Username already exists"

        # Add new user
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["username"] = username
            return redirect("/")

        return "Invalid username or password"

    return render_template("login.html")


# ---------------- ADD ACTIVITY ----------------

@app.route("/add_activity", methods=["POST"])
def add_activity():

    if "username" not in session:
        return jsonify({"error": "Please login first"}), 401

    username = session["username"]

    name = request.form.get("name")
    activity = request.form.get("activity")
    duration = request.form.get("duration")
    steps = request.form.get("steps")
    date = request.form.get("date")

    conn = get_db()

    conn.execute(
        """
        INSERT INTO activities
        (username, name, activity, duration, steps, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (username, name, activity, duration, steps, date)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Activity added successfully"})


# ---------------- GET ACTIVITIES ----------------

@app.route("/activities")
def activities():

    if "username" not in session:
        return jsonify([])

    username = session["username"]

    conn = get_db()

    data = conn.execute(
        """
        SELECT * FROM activities
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    create_table()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )