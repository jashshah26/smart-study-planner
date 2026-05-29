# Smart Study Planner

I built this because I kept forgetting to study for exams until it was too late.
This is a web app that takes your subjects, exam dates, and how hard each subject 
is — and builds you a realistic day-by-day study schedule automatically.

## What it does

- Add your subjects with exam dates and difficulty levels
- Auto generates a day-by-day study plan for every subject
- Harder subjects automatically get more study hours
- View your full plan in a clean table
- Mark sessions as done to track your progress
- Stats dashboard showing subjects added and next exam date

## Built with

- Python 3
- Flask — web framework
- SQLite3 — to store subjects and study sessions
- HTML + CSS — frontend
- Rich — for the original CLI version

## How to run it

1. Clone the repo
   git clone git@github.com:jashshah26/smart-study-planner.git

2. Go into the folder
   cd smart-study-planner

3. Install dependencies
   pip3 install -r requirements.txt

4. Start the web app
   python3 web.py

5. Open your browser and go to
   http://127.0.0.1:5000

## How to use it

1. Add your subjects one by one with their exam dates and difficulty
2. Click Generate Study Plan
3. View your personalized day-by-day plan
4. Mark sessions as done as you study

## Project structure

smart-study-planner/
├── web.py               # Flask web app
├── app.py               # Original CLI version
├── requirements.txt     # Dependencies
├── static/
│   └── style.css        # Styling
├── templates/
│   ├── index.html       # Home page
│   └── plan.html        # Study plan page
└── README.md            # You are here

## About

Made by Jash Shah — a first year CS student who needed
a better way to plan for exams.

github.com/jashshah26
