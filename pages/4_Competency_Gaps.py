import streamlit as st

from backend.database.db import (
    get_students,
    get_assessments
)


st.title("🎯 Competency Gap Analysis")

st.write(
    "Identify your strong areas, moderate areas, "
    "and topics that need improvement."
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


student_id = student["id"]


# --------------------------------------------------
# Get Assessment Data
# --------------------------------------------------

assessments = get_assessments(
    student_id
)


if not assessments:

    st.warning(
        "Please complete an AI Assessment first."
    )

    st.stop()


# --------------------------------------------------
# Get Latest Assessment
# --------------------------------------------------

latest_assessment = assessments[0]


assessment_id = latest_assessment[0]

skill = latest_assessment[2]

level = latest_assessment[3]

goal = latest_assessment[4]

difficulty = latest_assessment[5]

score = latest_assessment[6]

total = latest_assessment[7]

percentage = latest_assessment[8]


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
        f"**Target Skill:** {skill}"
    )


with col3:

    st.write(
        f"**Learning Goal:** {goal}"
    )


st.divider()


# --------------------------------------------------
# Overall Performance
# --------------------------------------------------

st.subheader("📊 Overall Performance")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Score",
        f"{score}/{total}"
    )


with col2:

    st.metric(
        "Percentage",
        f"{percentage}%"
    )


with col3:

    st.metric(
        "Level",
        level
    )


with col4:

    st.metric(
        "Difficulty",
        difficulty
    )


st.divider()


# --------------------------------------------------
# Overall Competency
# --------------------------------------------------

st.subheader("🎯 Overall Competency")


if percentage >= 80:

    overall_level = "Strong"

elif percentage >= 60:

    overall_level = "Moderate"

else:

    overall_level = "Needs Improvement"


if overall_level == "Strong":

    st.success(
        "🟢 Your overall competency is strong."
    )

elif overall_level == "Moderate":

    st.info(
        "🟡 Your overall competency is moderate."
    )

else:

    st.warning(
        "🔴 Your overall competency needs improvement."
    )


st.divider()


# --------------------------------------------------
# Topic Analysis
# --------------------------------------------------

st.subheader("📚 Topic Analysis")


# Current assessment table stores the overall score.
# Topic-level results are available from the current
# assessment session when available.

if "assessment" in st.session_state:

    current_assessment = st.session_state["assessment"]

    topic_results = current_assessment.get(
        "topic_results",
        {}
    )

else:

    topic_results = {}


weak_topics = []

moderate_topics = []

strong_topics = []


if topic_results:

    for topic, result in topic_results.items():

        correct = result["correct"]

        topic_total = result["total"]

        topic_percentage = round(
            (correct / topic_total) * 100,
            2
        )


        st.write(
            f"**{topic}:** "
            f"{correct}/{topic_total} "
            f"({topic_percentage}%)"
        )


        st.progress(
            min(
                topic_percentage / 100,
                1.0
            )
        )


        if topic_percentage < 60:

            weak_topics.append(topic)

        elif topic_percentage < 80:

            moderate_topics.append(topic)

        else:

            strong_topics.append(topic)


else:

    st.info(
        "Topic-level analysis is available for the "
        "current assessment session. Complete a new "
        "assessment to generate detailed topic gaps."
    )


st.divider()


# --------------------------------------------------
# Strong Areas
# --------------------------------------------------

if strong_topics:

    st.subheader("🟢 Strong Areas")

    for topic in strong_topics:

        st.write(
            f"✅ {topic}"
        )


# --------------------------------------------------
# Moderate Areas
# --------------------------------------------------

if moderate_topics:

    st.subheader("🟡 Moderate Areas")

    for topic in moderate_topics:

        st.write(
            f"⚠️ {topic}"
        )


# --------------------------------------------------
# Competency Gaps
# --------------------------------------------------

if weak_topics:

    st.subheader("🔴 Competency Gaps")

    for topic in weak_topics:

        st.write(
            f"❌ {topic}"
        )

else:

    if topic_results:

        st.success(
            "🎉 No major competency gaps detected!"
        )


# --------------------------------------------------
# Save in Session
# --------------------------------------------------

st.session_state["competency_gaps"] = weak_topics

st.session_state["moderate_topics"] = moderate_topics

st.session_state["strong_topics"] = strong_topics


# --------------------------------------------------
# Recommended Action
# --------------------------------------------------

st.divider()

st.subheader("🚀 Recommended Action")


if weak_topics:

    st.warning(
        "Focus your learning plan primarily on: "
        + ", ".join(weak_topics)
    )


elif moderate_topics:

    st.info(
        "Focus on improving these topics: "
        + ", ".join(moderate_topics)
    )


elif strong_topics:

    st.success(
        "Your current performance is strong. "
        "You can move toward advanced topics."
    )


else:

    if percentage < 60:

        st.info(
            "Review your learning resources and "
            "take another assessment."
        )

    elif percentage < 80:

        st.info(
            "Practice more questions and use the "
            "AI Tutor to strengthen your knowledge."
        )

    else:

        st.success(
            "Continue with advanced learning and "
            "challenging practice questions."
        )