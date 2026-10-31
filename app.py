from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

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


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/admin")
def admin():
    conn = get_db()
    messages = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", messages=messages)


@app.route("/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
