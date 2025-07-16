import csv
import sqlite3

# Step 1: Connect to SQLite (creates file if it doesn't exist)
conn = sqlite3.connect("scores.db")
cursor = conn.cursor()

# Step 2: Create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL,
        photo TEXT
    )
""")

# Step 3: Read your CSV and insert the data
with open("teacher_stats.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        photo = row["Photo"]
        score = int(row["Score"])
        name = photo  # Use photo filename as name placeholder
        cursor.execute("INSERT INTO teachers (name, score, photo) VALUES (?, ?, ?)", (name, score, photo))

# Step 4: Commit and close
conn.commit()
conn.close()

print("✅ Database created and populated successfully!")
