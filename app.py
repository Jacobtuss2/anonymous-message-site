import os
from datetime import datetime
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DEFAULT_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me-strong-password")
app.config["ADMIN_PASSWORD_HASH"] = generate_password_hash(
    DEFAULT_ADMIN_PASSWORD,
    method="scrypt",
)

DB_NAME = "messages.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def get_message_count():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) AS total FROM messages").fetchone()["total"]
    conn.close()
    return count


@app.route("/")
def index():
    return render_template("index.html", message_count=get_message_count())


@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message", "").strip()

    if message:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = get_db()
        conn.execute(
            "INSERT INTO messages (text, created_at) VALUES (?, ?)",
            (message, now),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if check_password_hash(app.config["ADMIN_PASSWORD_HASH"], password):
            session["admin"] = True
            return redirect(url_for("admin"))
        return render_template("login.html", error="Incorrect password.")

    return render_template("login.html", error=None)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db()
    messages = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    conn.close()
    return render_template(
        "admin.html",
        messages=messages,
        message_count=len(messages),
    )


@app.route("/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


@app.route("/clear-all", methods=["POST"])
def clear_all_messages():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
