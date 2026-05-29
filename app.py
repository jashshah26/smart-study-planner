import sqlite3
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

def init_db():
    conn = sqlite3.connect("study_planner.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    exam_date TEXT NOT NULL,
                    difficulty INTEGER NOT NULL,
                    hours_per_day REAL NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id INTEGER,
                    date TEXT,
                    hours REAL,
                    completed INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def add_subject():
    console.print("\n[bold magenta]Add a New Subject[/bold magenta]")
    name = input("Subject name: ")
    exam_date = input("Exam date (YYYY-MM-DD): ")
    difficulty = int(input("Difficulty (1=Easy, 2=Medium, 3=Hard): "))
    hours_per_day = float(input("How many hours/day can you study this? "))

    conn = sqlite3.connect("study_planner.db")
    c = conn.cursor()
    c.execute("INSERT INTO subjects (name, exam_date, difficulty, hours_per_day) VALUES (?, ?, ?, ?)",
              (name, exam_date, difficulty, hours_per_day))
    conn.commit()
    conn.close()
    rprint(f"[bright_green]{name} added successfully![/bright_green]")

def generate_plan():
    conn = sqlite3.connect("study_planner.db")
    c = conn.cursor()
    c.execute("SELECT * FROM subjects ORDER BY exam_date ASC")
    subjects = c.fetchall()

    if not subjects:
        rprint("[bold red]No subjects found. Add a subject first![/bold red]")
        conn.close()
        return

    c.execute("DELETE FROM sessions")
    today = datetime.today().date()

    for subject in subjects:
        sid, name, exam_date, difficulty, hours_per_day = subject
        exam = datetime.strptime(exam_date, "%Y-%m-%d").date()
        days_left = (exam - today).days

        if days_left <= 0:
            rprint(f"[bold red]Warning: {name} exam date has passed![/bold red]")
            continue

        for i in range(days_left):
            study_date = today + timedelta(days=i)
            hours = hours_per_day * (1 + (difficulty - 1) * 0.2)
            c.execute("INSERT INTO sessions (subject_id, date, hours) VALUES (?, ?, ?)",
                      (sid, str(study_date), round(hours, 1)))

    conn.commit()
    conn.close()
    rprint("[bright_green]Study plan generated successfully![/bright_green]")

def view_plan():
    conn = sqlite3.connect("study_planner.db")
    c = conn.cursor()
    c.execute('''SELECT sessions.date, subjects.name, sessions.hours, sessions.completed
                 FROM sessions JOIN subjects ON sessions.subject_id = subjects.id
                 ORDER BY sessions.date ASC LIMIT 30''')
    rows = c.fetchall()
    conn.close()

    if not rows:
        rprint("[bold red]No plan found. Generate a plan first![/bold red]")
        return

    table = Table(title="Your Study Plan (Next 30 Days)",
                  title_style="bold magenta",
                  header_style="bold purple4")
    table.add_column("Date", style="magenta")
    table.add_column("Subject", style="purple4")
    table.add_column("Hours", style="bright_magenta")
    table.add_column("Status", style="bright_green")

    for row in rows:
        status = "Done" if row[3] else "Pending"
        table.add_row(row[0], row[1], str(row[2]), status)

    console.print(table)

def mark_done():
    view_plan()
    conn = sqlite3.connect("study_planner.db")
    c = conn.cursor()
    date = input("\nEnter date to mark as done (YYYY-MM-DD): ")
    subject = input("Enter subject name: ")
    c.execute('''UPDATE sessions SET completed = 1
                 WHERE date = ? AND subject_id = (SELECT id FROM subjects WHERE name = ?)''',
              (date, subject))
    conn.commit()
    conn.close()
    rprint("[bright_green]Marked as done![/bright_green]")

def main():
    init_db()
    while True:
        console.print("\n[bold purple4]Smart Study Planner[/bold purple4]")
        console.print("[magenta][1][/magenta] Add Subject")
        console.print("[magenta][2][/magenta] Generate Study Plan")
        console.print("[magenta][3][/magenta] View Study Plan")
        console.print("[magenta][4][/magenta] Mark Session as Done")
        console.print("[magenta][5][/magenta] Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_subject()
        elif choice == "2":
            generate_plan()
        elif choice == "3":
            view_plan()
        elif choice == "4":
            mark_done()
        elif choice == "5":
            rprint("[bold magenta]Goodbye! Keep studying![/bold magenta]")
            break
        else:
            rprint("[bold red]Invalid option, try again.[/bold red]")

if __name__ == "__main__":
    main()