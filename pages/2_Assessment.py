import streamlit as st

from backend.assessment.generator import generate_assessment
from backend.database.db import (
    save_assessment,
    get_students,
    get_student
)


st.title("📝 AI Skill Assessment")

st.write(
    "Create a personalized assessment based on your skill, "
    "current level, learning goal, and difficulty."
)

st.divider()


# --------------------------------------------------
# Check Student Profile
# --------------------------------------------------

if "student" not in st.session_state:

    students = get_students()

    if students:

        student_id = students[-1][0]

        saved_student = get_student(student_id)

        st.session_state["student"] = {
            "id": saved_student[0],
            "name": saved_student[1],
            "college": saved_student[2],
            "branch": saved_student[3],
            "year": saved_student[4],
            "target_skill": saved_student[5],
            "learning_goal": saved_student[6]
        }

    else:

        st.warning(
            "Please complete your Student Profile first."
        )

        st.stop()


student = st.session_state["student"]


# --------------------------------------------------
# Assessment Configuration
# --------------------------------------------------

st.subheader("🎯 Assessment Requirements")

col1, col2 = st.columns(2)


with col1:

    skill = st.selectbox(
        "Select Skill",
        [
            "Java",
            "Python",
            "Data Structures",
            "DBMS",
            "Operating Systems",
            "Computer Networks",
            "AI / ML",
            "Web Development"
        ],
        index=(
            [
                "Java",
                "Python",
                "Data Structures",
                "DBMS",
                "Operating Systems",
                "Computer Networks",
                "AI / ML",
                "Web Development"
            ].index(student["target_skill"])
            if student["target_skill"]
            in [
                "Java",
                "Python",
                "Data Structures",
                "DBMS",
                "Operating Systems",
                "Computer Networks",
                "AI / ML",
                "Web Development"
            ]
            else 0
        )
    )


    level = st.selectbox(
        "Current Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


    goal = st.selectbox(
        "Learning Goal",
        [
            "Placement Preparation",
            "Academic Improvement",
            "Competitive Programming",
            "Project Development",
            "Skill Development"
        ],
        index=(
            [
                "Placement Preparation",
                "Academic Improvement",
                "Competitive Programming",
                "Project Development",
                "Skill Development"
            ].index(student["learning_goal"])
            if student["learning_goal"]
            in [
                "Placement Preparation",
                "Academic Improvement",
                "Competitive Programming",
                "Project Development",
                "Skill Development"
            ]
            else 0
        )
    )


with col2:

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
            "Mixed"
        ]
    )


    question_count = st.selectbox(
        "Number of Questions",
        [5, 10, 15, 20]
    )


st.divider()


# --------------------------------------------------
# Generate Assessment
# --------------------------------------------------

if st.button(
    "🤖 Generate AI Assessment",
    use_container_width=True
):

    with st.spinner(
        "🤖 Creating your personalized assessment..."
    ):

        try:

            questions = generate_assessment(
                skill=skill,
                level=level,
                goal=goal,
                difficulty=difficulty,
                question_count=question_count
            )

            st.session_state[
                "generated_assessment"
            ] = questions

            st.session_state[
                "assessment_config"
            ] = {
                "skill": skill,
                "level": level,
                "goal": goal,
                "difficulty": difficulty
            }

            st.success(
                f"✅ {len(questions)} questions generated!"
            )

        except Exception as e:

            st.error(
                "❌ Unable to generate the assessment."
            )

            st.exception(e)


# --------------------------------------------------
# Display Generated Assessment
# --------------------------------------------------

if "generated_assessment" in st.session_state:

    questions = st.session_state[
        "generated_assessment"
    ]

    st.divider()

    st.subheader("📋 Your AI Assessment")

    st.info(
        "Select one answer for every question before submitting."
    )


    with st.form("assessment_form"):

        answers = {}

        for i, question in enumerate(questions):

            st.markdown(
                f"### Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            answers[i] = st.radio(
                "Select your answer:",
                question["options"],
                index=None,
                key=f"assessment_answer_{i}"
            )

            st.caption(
                f"Topic: {question['topic']}"
            )

            st.divider()


        submitted = st.form_submit_button(
            "📊 Submit Assessment",
            use_container_width=True
        )


        if submitted:

            # ------------------------------------------
            # Check Unanswered Questions
            # ------------------------------------------

            unanswered = [
                i + 1
                for i, answer in answers.items()
                if answer is None
            ]

            if unanswered:

                st.warning(
                    "⚠️ Please answer all questions before submitting."
                )

                st.write(
                    "Unanswered questions:",
                    ", ".join(
                        f"Q{number}"
                        for number in unanswered
                    )
                )

                st.stop()


            # ------------------------------------------
            # Calculate Score
            # ------------------------------------------

            score = 0

            topic_results = {}


            for i, question in enumerate(questions):

                selected = answers[i]

                correct = question["answer"]

                topic = question["topic"]


                if topic not in topic_results:

                    topic_results[topic] = {
                        "correct": 0,
                        "total": 0
                    }


                topic_results[topic]["total"] += 1


                if selected == correct:

                    score += 1

                    topic_results[
                        topic
                    ]["correct"] += 1


            # ------------------------------------------
            # Calculate Percentage
            # ------------------------------------------

            total = len(questions)

            percentage = round(
                (score / total) * 100,
                2
            )


            # ------------------------------------------
            # Get Current Student ID
            # ------------------------------------------

            student_id = student["id"]


            # ------------------------------------------
            # Save Assessment
            # ------------------------------------------

            save_assessment(
                student_id=student_id,
                skill=skill,
                level=level,
                goal=goal,
                difficulty=difficulty,
                score=score,
                total=total,
                percentage=percentage
            )


            # ------------------------------------------
            # Store Result in Session
            # ------------------------------------------

            st.session_state[
                "assessment"
            ] = {

                "score": score,

                "total": total,

                "percentage": percentage,

                "topic_results": topic_results,

                "skill": skill,

                "level": level,

                "goal": goal,

                "difficulty": difficulty
            }


            # ------------------------------------------
            # Result
            # ------------------------------------------

            st.success(
                f"🎉 Assessment completed! "
                f"Score: {score}/{total} "
                f"({percentage}%)"
            )


            st.success(
                "💾 Assessment result saved to SQLite."
            )


            # ------------------------------------------
            # Performance Message
            # ------------------------------------------

            if percentage >= 80:

                st.success(
                    "🟢 Excellent performance!"
                )

            elif percentage >= 60:

                st.info(
                    "🟡 Good performance. Keep practicing."
                )

            else:

                st.warning(
                    "🔴 You need more practice in this skill."
                )


            # ------------------------------------------
            # Topic Performance
            # ------------------------------------------

            st.subheader(
                "📊 Topic Performance"
            )


            for topic, result in topic_results.items():

                topic_percentage = round(
                    (
                        result["correct"]
                        / result["total"]
                    ) * 100,
                    2
                )


                st.write(
                    f"**{topic}:** "
                    f"{result['correct']}/"
                    f"{result['total']} "
                    f"({topic_percentage}%)"
                )


                st.progress(
                    topic_percentage / 100
                )