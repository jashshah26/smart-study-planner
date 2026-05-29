# smart-study-planner
A CLI-based smart study planner built with Python and SQLite
# Smart Study Planner

I built this because I kept forgetting to study for exams until it was too late.
This is a simple command-line app that takes your subjects, exam dates, and how 
hard each subject is — and builds you a realistic day-by-day study schedule automatically.

## What it does

- You add your subjects and tell it when your exam is
- It figures out how many days you have left
- It creates a study plan for every single day until your exam
- Harder subjects automatically get more hours
- You can mark days as done to track your progress

## Built with

- Python 3
- SQLite3 — to store your subjects and study sessions
- Rich — to make the terminal look clean and readable

## How to run it

1. Clone the repo
   git clone git@github.com:jashshah26/smart-study-planner.git

2. Go into the folder
   cd smart-study-planner

3. Install the one dependency
   pip3 install -r requirements.txt

4. Start the app
   python3 app.py

## How to use it

When you run it you get a simple menu. Start by adding a subject,
then generate your plan, then view it. That's really it.

If you study for the day just mark it as done so you can
keep track of where you are.

## Folder structure

smart-study-planner/
├── app.py              # everything is here
├── requirements.txt    # just one library
└── README.md           # you are here

## About

Made by Jash Shah — a first year CS student who needed
a better way to plan for exams.

github.com/jashshah26