from flask import Flask, render_template, request, redirect
import csv
import random

app = Flask(__name__)

CSV_FILE = 'teacher_stats.csv'
IMAGE_FOLDER = 'static/teacher_photos'


def load_stats():
    with open(CSV_FILE, newline='') as csvfile:
        return list(csv.DictReader(csvfile))


def save_stats(stats):
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=stats[0].keys())
        writer.writeheader()
        writer.writerows(stats)


@app.route("/", methods=["GET", "POST"])
def index():
    stats = load_stats()

    if request.method == "POST":
        choice = request.form["choice"]
        id1 = int(request.form["id1"])
        id2 = int(request.form["id2"])

        if choice == "1":
            stats[id1]["Score"] = str(int(stats[id1]["Score"]) + 5)
            stats[id2]["Score"] = str(int(stats[id2]["Score"]) - 5)
        else:
            stats[id2]["Score"] = str(int(stats[id2]["Score"]) + 5)
            stats[id1]["Score"] = str(int(stats[id1]["Score"]) - 5)

        save_stats(stats)
        return redirect("/")

    num1, num2 = random.sample(range(len(stats)), 2)
    teacher1 = stats[num1]
    teacher2 = stats[num2]

    return render_template("index.html",
                           teacher1=teacher1,
                           teacher2=teacher2,
                           id1=num1,
                           id2=num2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

