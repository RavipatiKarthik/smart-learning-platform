import sqlite3
import json

DB_PATH = "database/learning.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def save_student(student):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO students
        (name, college, branch, year, target_skill, learning_goal)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            student["name"],
            student["college"],
            student["branch"],
            student["year"],
            student["target_skill"],
            student["learning_goal"]
        )
    )

    conn.commit()
    conn.close()


def get_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students


def save_assessment(
    student_id,
    skill,
    level,
    goal,
    difficulty,
    score,
    total,
    percentage
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO assessments
        (student_id, skill, level, goal, difficulty,
         score, total, percentage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            skill,
            level,
            goal,
            difficulty,
            score,
            total,
            percentage
        )
    )

    conn.commit()
    conn.close()


def get_assessments(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM assessments
        WHERE student_id = ?
        ORDER BY id DESC
        """,
        (student_id,)
    )

    assessments = cursor.fetchall()

    conn.close()

    return assessments

def get_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    return student
def save_learning_plan(
    student_id,
    skill,
    goal,
    plan
):
    conn = get_connection()
    cursor = conn.cursor()

    plan_json = json.dumps(plan)

    cursor.execute(
        """
        INSERT INTO learning_plans
        (student_id, skill, goal, plan_json)
        VALUES (?, ?, ?, ?)
        """,
        (
            student_id,
            skill,
            goal,
            plan_json
        )
    )

    conn.commit()
    conn.close()


def get_learning_plans(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM learning_plans
        WHERE student_id = ?
        ORDER BY id DESC
        """,
        (student_id,)
    )

    plans = cursor.fetchall()

    conn.close()

    return plans

def save_quiz_result(
    student_id,
    skill,
    score,
    total,
    percentage
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO quiz_results
        (student_id, skill, score, total, percentage)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            skill,
            score,
            total,
            percentage
        )
    )

    conn.commit()
    conn.close()


def get_quiz_results(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM quiz_results
        WHERE student_id = ?
        ORDER BY id DESC
        """,
        (student_id,)
    )

    results = cursor.fetchall()

    conn.close()

    return results

def save_assessment_topic(
    assessment_id,
    student_id,
    topic,
    correct,
    total,
    percentage
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO assessment_topics
        (
            assessment_id,
            student_id,
            topic,
            correct,
            total,
            percentage
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            assessment_id,
            student_id,
            topic,
            correct,
            total,
            percentage
        )
    )

    conn.commit()
    conn.close()


def get_assessment_topics(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM assessment_topics
        WHERE student_id = ?
        ORDER BY id DESC
        """,
        (student_id,)
    )

    topics = cursor.fetchall()

    conn.close()

    return topics