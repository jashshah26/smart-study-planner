from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("study_planner.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    subjects = conn.execute("SELECT * FROM subjects ORDER BY exam_date ASC").fetchall()
    conn.close()
    return render_template("index.html", subjects=subjects)

@app.route("/add", methods=["POST"])
def add_subject():
    name = request.form["name"]
    exam_date = request.form["exam_date"]
    difficulty = int(request.form["difficulty"])
    hours_per_day = float(request.form["hours_per_day"])

    conn = get_db()
    conn.execute("INSERT INTO subjects (name, exam_date, difficulty, hours_per_day) VALUES (?, ?, ?, ?)",
                 (name, exam_date, difficulty, hours_per_day))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/generate")
def generate_plan():
    conn = get_db()
    subjects = conn.execute("SELECT * FROM subjects").fetchall()
    conn.execute("DELETE FROM sessions")
    today = datetime.today().date()

    for subject in subjects:
        sid = subject["id"]
        exam = datetime.strptime(subject["exam_date"], "%Y-%m-%d").date()
        days_left = (exam - today).days
        if days_left <= 0:
            continue
        for i in range(days_left):
            study_date = today + timedelta(days=i)
            hours = subject["hours_per_day"] * (1 + (subject["difficulty"] - 1) * 0.2)
            conn.execute("INSERT INTO sessions (subject_id, date, hours) VALUES (?, ?, ?)",
                         (sid, str(study_date), round(hours, 1)))

    conn.commit()
    conn.close()
    return redirect(url_for("plan"))

@app.route("/plan")
def plan():
    conn = get_db()
    rows = conn.execute('''SELECT sessions.id, sessions.date, subjects.name, 
                           sessions.hours, sessions.completed
                           FROM sessions JOIN subjects ON sessions.subject_id = subjects.id
                           ORDER BY sessions.date ASC LIMIT 30''').fetchall()
    conn.close()
    return render_template("plan.html", rows=rows)

@app.route("/done/<int:session_id>")
def mark_done(session_id):
    conn = get_db()
    conn.execute("UPDATE sessions SET completed = 1 WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("plan"))

if __name__ == "__main__":
    app.run(debug=True)