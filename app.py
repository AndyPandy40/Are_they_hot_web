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
      <head><title>Vote</title></head>
      <body>
        <h1>Who is hotter?</h1>
        <form method="POST" action="/vote">
          <input type="hidden" name="t1_id" value="{{ t1['id'] }}">
          <input type="hidden" name="t2_id" value="{{ t2['id'] }}">

          <button type="submit" name="choice" value="t1" style="border:none; background:none;">
            <img src="{{ url_for('static', filename='teacher_photos/' + t1['photo']) }}" alt="Teacher 1" style="max-height:300px;">
          </button>

          <button type="submit" name="choice" value="t2" style="border:none; background:none;">
            <img src="{{ url_for('static', filename='teacher_photos/' + t2['photo']) }}" alt="Teacher 2" style="max-height:300px;">
          </button>
        </form>
      </body>
    </html>
    """, t1=teacher1, t2=teacher2)

@app.route("/vote", methods=["POST"])
def vote():
    # (Your vote processing logic here)

    # After updating the database, print all teachers and scores
    conn = get_db_connection()
    teachers = conn.execute("SELECT name, score FROM teachers").fetchall()
    conn.close()

    print("Current scores:")
    for t in teachers:
        print(f"{t['name']}: {t['score']}")

    return redirect("/")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
