import sqlite3

DB_PATH = "database/learning.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# --------------------------------------------------
# Students
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    college TEXT NOT NULL,
    branch TEXT NOT NULL,
    year TEXT NOT NULL,
    target_skill TEXT NOT NULL,
    learning_goal TEXT NOT NULL
)
""")


# --------------------------------------------------
# Assessments
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    skill TEXT,
    level TEXT,
    goal TEXT,
    difficulty TEXT,
    score INTEGER,
    total INTEGER,
    percentage REAL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")


# --------------------------------------------------
# Assessment Topic Results
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS assessment_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER,
    student_id INTEGER,
    topic TEXT,
    correct INTEGER,
    total INTEGER,
    percentage REAL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")


# --------------------------------------------------
# Quiz Results
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    skill TEXT,
    score INTEGER,
    total INTEGER,
    percentage REAL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")


# --------------------------------------------------
# Progress
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    skill TEXT,
    topic TEXT,
    score REAL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")


# --------------------------------------------------
# Learning Plans
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS learning_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    skill TEXT,
    goal TEXT,
    plan_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")


conn.commit()
conn.close()

print("✅ SQLite database initialized successfully!")