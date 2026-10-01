import streamlit as st

from backend.database.db import (
    get_students,
    get_assessments,
    get_quiz_results
)


st.set_page_config(
    page_title="SmartLearn AI",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.title("🎓 SmartLearn AI")

st.subheader(
    "AI-Powered Student Learning Platform"
)

st.write(
    "Assess your skills, identify competency gaps, "
    "get personalized learning recommendations, "
    "and improve your performance."
)

st.divider()


# --------------------------------------------------
# Database Data
# --------------------------------------------------

students = get_students()

total_students = len(students)

total_assessments = 0
all_scores = []


for student in students:

    student_id = student[0]

    assessments = get_assessments(student_id)

    quiz_results = get_quiz_results(student_id)

    total_assessments += len(assessments)

    for assessment in assessments:
        all_scores.append(assessment[8])

    for quiz in quiz_results:
        all_scores.append(quiz[5])


# --------------------------------------------------
# Average Score
# --------------------------------------------------

if all_scores:

    average_score = round(
        sum(all_scores) / len(all_scores),
        2
    )

else:

    average_score = 0


# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------

st.subheader("📊 Platform Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👨‍🎓 Students",
        total_students
    )


with col2:

    st.metric(
        "📝 Assessments",
        total_assessments
    )


with col3:

    st.metric(
        "📈 Average Score",
        f"{average_score}%"
    )


st.divider()


# --------------------------------------------------
# Current Student
# --------------------------------------------------

if "student" in st.session_state:

    student = st.session_state["student"]

    st.subheader("👤 Current Student")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Name:** {student['name']}"
        )

        st.write(
            f"**College:** {student['college']}"
        )

        st.write(
            f"**Branch:** {student['branch']}"
        )

    with col2:

        st.write(
            f"**Academic Year:** {student['year']}"
        )

        st.write(
            f"**Target Skill:** {student['target_skill']}"
        )

        st.write(
            f"**Learning Goal:** {student['learning_goal']}"
        )

    st.divider()


# --------------------------------------------------
# Platform Features
# --------------------------------------------------

st.subheader("🚀 Learning Journey")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.info(
        "📝\n\n"
        "**AI Assessment**\n\n"
        "Evaluate your current skill level."
    )


with col2:

    st.info(
        "🎯\n\n"
        "**Competency Gaps**\n\n"
        "Identify topics that need improvement."
    )


with col3:

    st.info(
        "📚\n\n"
        "**Personalized Learning**\n\n"
        "Get an AI-generated learning plan."
    )


with col4:

    st.info(
        "🤖\n\n"
        "**AI Tutor**\n\n"
        "Ask questions using RAG-based learning."
    )


st.divider()


# --------------------------------------------------
# Start Learning
# --------------------------------------------------

st.subheader("🎓 Start Your Learning Journey")

if not students:

    st.info(
        "👈 Start by creating your Student Profile."
    )

else:

    st.success(
        "✅ Your profile is ready. "
        "Continue with Assessment → Learning Plan → Quiz → Progress."
    )