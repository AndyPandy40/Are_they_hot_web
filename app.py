from flask import Flask, render_template_string, request, redirect
import sqlite3
import random

app = Flask(__name__)

DB_PATH = "scores.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    teachers = conn.execute("SELECT * FROM teachers").fetchall()
    conn.close()

    teacher1, teacher2 = random.sample(teachers, 2)
    return render_template_string("""
        <html>
        <head><title>Are They Hot?</title></head>
        <body>
            <h1>🔥 Who's hotter?</h1>
            <form method="POST" action="/vote">
                <input type="hidden" name="t1_id" value="{{ t1['id'] }}">
                <input type="hidden" name="t2_id" value="{{ t2['id'] }}">
                <button type="submit" name="choice" value="t1">{{ t1["name"] }}</button>
                <button type="submit" name="choice" value="t2">{{ t2["name"] }}</button>
            </form>
            <p><a href="/leaderboard">View leaderboard</a></p>
        </body>
        </html>
    """, t1=teacher1, t2=teacher2)

@app.route("/vote", methods=["POST"])
def vote():
    t1_id = int(request.form["t1_id"])
    t2_id = int(request.form["t2_id"])
    choice = request.form["choice"]

    conn = get_db_connection()
    if choice == "t1":
        conn.execute("UPDATE teachers SET score = score + 5 WHERE id = ?", (t1_id,))
        conn.execute("UPDATE teachers SET score = score - 5 WHERE id = ?", (t2_id,))
    else:
        conn.execute("UPDATE teachers SET score = score + 5 WHERE id = ?", (t2_id,))
        conn.execute("UPDATE teachers SET score = score - 5 WHERE id = ?", (t1_id,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection()
    teachers = conn.execute("SELECT * FROM teachers ORDER BY score DESC").fetchall()
    conn.close()

    return render_template_string("""
        <html>
        <head><title>Leaderboard</title></head>
        <body>
            <h1>🏆 Leaderboard</h1>
            <table border="1" cellpadding="10">
                <tr><th>Name</th><th>Score</th></tr>
                {% for teacher in teachers %}
                    <tr>
                        <td>{{ teacher["name"] }}</td>
                        <td>{{ teacher["score"] }}</td>
                    </tr>
                {% endfor %}
            </table>
            <p><a href="/">← Back to voting</a></p>
        </body>
        </html>
    """, teachers=teachers)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
