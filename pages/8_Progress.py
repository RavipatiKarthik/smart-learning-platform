import streamlit as st
from backend.database.db import (
    get_students,
    get_assessments,
    get_quiz_results
)
st.title("📊 Student Progress")

st.write(
    "Track your assessment results, quiz performance, "
    "and overall learning progress."
)
st.divider()
# --------------------------------------------------
# Get Current Student
# --------------------------------------------------
if "student" not in st.session_state:
    students = get_students()
    if not students:
        st.warning(
            "Please complete your Student Profile first."
        )
        st.stop()
    latest_student = students[-1]
    student = {
        "id": latest_student[0],
        "name": latest_student[1],
        "college": latest_student[2],
        "branch": latest_student[3],
        "year": latest_student[4],
        "target_skill": latest_student[5],
        "learning_goal": latest_student[6]
    }
    st.session_state["student"] = student
else:
    student = st.session_state["student"]
# IMPORTANT:
# Always use the currently selected student's ID.
student_id = student["id"]
# --------------------------------------------------
# Student Information
# --------------------------------------------------
st.subheader("👤 Student")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(
        f"**Name:** {student['name']}"
    )
with col2:
    st.write(
        f"**Target Skill:** {student['target_skill']}"
    )
with col3:
    st.write(
        f"**Goal:** {student['learning_goal']}"
    )
st.divider()
# --------------------------------------------------
# Get Student Data
# --------------------------------------------------
assessments = get_assessments(
    student_id
)
quiz_results = get_quiz_results(
    student_id
)
# --------------------------------------------------
# No Progress Data
# --------------------------------------------------

if not assessments and not quiz_results:

    st.info(
        "📚 No progress data available yet. "
        "Complete an assessment or quiz to start tracking progress."
    )

    st.stop()


# --------------------------------------------------
# Calculate Statistics
# --------------------------------------------------

assessment_scores = [
    assessment[8]
    for assessment in assessments
]


quiz_scores = [
    quiz[5]
    for quiz in quiz_results
]


all_scores = (
    assessment_scores
    + quiz_scores
)


average_score = round(
    sum(all_scores) / len(all_scores),
    2
)


highest_score = round(
    max(all_scores),
    2
)


lowest_score = round(
    min(all_scores),
    2
)


# --------------------------------------------------
# Overall Performance
# --------------------------------------------------

st.subheader("📈 Overall Performance")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Average Score",
        f"{average_score}%"
    )


with col2:

    st.metric(
        "Highest Score",
        f"{highest_score}%"
    )


with col3:

    st.metric(
        "Lowest Score",
        f"{lowest_score}%"
    )


with col4:

    st.metric(
        "Total Activities",
        len(all_scores)
    )


st.divider()


# --------------------------------------------------
# Assessment History
# --------------------------------------------------

st.subheader("📝 Assessment History")


if assessments:

    for index, assessment in enumerate(
        assessments,
        start=1
    ):

        skill = assessment[2]

        difficulty = assessment[5]

        score = assessment[6]

        total = assessment[7]

        percentage = assessment[8]


        st.write(
            f"**Assessment {index} — {skill}**"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.write(
                f"Score: **{score}/{total}**"
            )


        with col2:

            st.write(
                f"Percentage: **{percentage}%**"
            )


        with col3:

            st.write(
                f"Difficulty: **{difficulty}**"
            )


        st.progress(
            min(
                percentage / 100,
                1.0
            )
        )


        st.divider()


else:

    st.info(
        "No assessment records available."
    )


# --------------------------------------------------
# Quiz History
# --------------------------------------------------

st.subheader("🎯 Quiz History")


if quiz_results:

    for index, quiz in enumerate(
        quiz_results,
        start=1
    ):

        skill = quiz[2]

        score = quiz[3]

        total = quiz[4]

        percentage = quiz[5]


        st.write(
            f"**Quiz {index} — {skill}**"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"Score: **{score}/{total}**"
            )


        with col2:

            st.write(
                f"Percentage: **{percentage}%**"
            )


        st.progress(
            min(
                percentage / 100,
                1.0
            )
        )


        st.divider()


else:

    st.info(
        "No quiz records available."
    )


# --------------------------------------------------
# Current Performance
# --------------------------------------------------

st.subheader("🎯 Current Performance")


if average_score >= 80:

    st.success(
        "🟢 Excellent performance! "
        "Continue practicing advanced topics."
    )


elif average_score >= 60:

    st.info(
        "🟡 Good progress! "
        "Focus on your weaker topics to improve further."
    )


else:

    st.warning(
        "🔴 More practice is recommended. "
        "Review your learning resources and use the AI Tutor."
    )


st.divider()


# --------------------------------------------------
# Recommended Next Step
# --------------------------------------------------

st.subheader("🚀 Recommended Next Step")


if average_score < 60:

    st.write(
        "📖 Review your learning resources → "
        "🤖 Ask the AI Tutor → "
        "📝 Take another quiz"
    )


elif average_score < 80:

    st.write(
        "📚 Practice moderate topics → "
        "📝 Take another quiz → "
        "📊 Review your progress"
    )


else:

    st.write(
        "🚀 Move to advanced topics → "
        "🧠 Practice challenging questions → "
        "🏆 Continue improving your score"
    )