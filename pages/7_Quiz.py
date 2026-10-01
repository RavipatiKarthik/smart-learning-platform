import streamlit as st

from backend.database.db import save_quiz_result
from backend.assessment.generator import generate_assessment


st.title("📝 AI Quiz")

st.write(
    "Take a personalized quiz based on your skill, "
    "learning goal, and current level."
)

st.divider()


# --------------------------------------------------
# Check Student Profile
# --------------------------------------------------

if "student" not in st.session_state:

    st.warning(
        "Please complete your Student Profile first."
    )

    st.stop()


student = st.session_state["student"]


# --------------------------------------------------
# Previous Assessment Configuration
# --------------------------------------------------

if "assessment_config" in st.session_state:

    previous_config = st.session_state[
        "assessment_config"
    ]

    default_skill = previous_config["skill"]
    default_level = previous_config["level"]
    default_goal = previous_config["goal"]

else:

    default_skill = student["target_skill"]
    default_level = "Beginner"
    default_goal = student["learning_goal"]


# --------------------------------------------------
# Quiz Configuration
# --------------------------------------------------

st.subheader("🎯 Quiz Configuration")

col1, col2 = st.columns(2)


with col1:

    skills = [
        "Java",
        "Python",
        "Data Structures",
        "DBMS",
        "Operating Systems",
        "Computer Networks",
        "AI / ML",
        "Web Development"
    ]

    skill = st.selectbox(
        "Skill",
        skills,
        index=(
            skills.index(default_skill)
            if default_skill in skills
            else 0
        )
    )


    levels = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    level = st.selectbox(
        "Level",
        levels,
        index=(
            levels.index(default_level)
            if default_level in levels
            else 0
        )
    )


with col2:

    goals = [
        "Placement Preparation",
        "Academic Improvement",
        "Competitive Programming",
        "Project Development",
        "Skill Development"
    ]

    goal = st.selectbox(
        "Learning Goal",
        goals,
        index=(
            goals.index(default_goal)
            if default_goal in goals
            else 0
        )
    )


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
        [5, 10, 15]
    )


st.divider()


# --------------------------------------------------
# Generate Quiz
# --------------------------------------------------

if st.button(
    "🤖 Generate Quiz",
    use_container_width=True
):

    with st.spinner(
        "🤖 Generating your personalized quiz..."
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
                "quiz_questions"
            ] = questions


            st.session_state[
                "quiz_config"
            ] = {
                "skill": skill,
                "level": level,
                "goal": goal,
                "difficulty": difficulty
            }


            # Clear previous answers

            for i in range(question_count):

                st.session_state.pop(
                    f"quiz_answer_{i}",
                    None
                )


            st.success(
                f"✅ {len(questions)} quiz questions generated!"
            )


        except Exception as e:

            st.error(
                "❌ Unable to generate quiz."
            )

            st.exception(e)


# --------------------------------------------------
# Display Quiz
# --------------------------------------------------

if "quiz_questions" in st.session_state:

    questions = st.session_state[
        "quiz_questions"
    ]

    st.divider()

    st.subheader("📋 Your AI Quiz")

    st.info(
        "Select one answer for every question before submitting."
    )


    with st.form("quiz_form"):

        answers = {}


        # ------------------------------------------
        # Display Questions
        # ------------------------------------------

        for i, question in enumerate(questions):

            st.markdown(
                f"### Question {i + 1}"
            )


            st.write(
                question["question"]
            )


            answers[i] = st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"quiz_answer_{i}"
            )


            st.caption(
                f"Topic: {question['topic']}"
            )


            st.divider()


        # ------------------------------------------
        # Submit Quiz
        # ------------------------------------------

        submitted = st.form_submit_button(
            "🚀 Submit Quiz",
            use_container_width=True
        )


        if submitted:

            # --------------------------------------
            # Check Unanswered Questions
            # --------------------------------------

            unanswered = [
                i + 1
                for i, answer in answers.items()
                if answer is None
            ]


            if unanswered:

                st.warning(
                    "⚠️ Please answer all questions "
                    "before submitting."
                )


                st.write(
                    "Unanswered questions:",
                    ", ".join(
                        f"Q{number}"
                        for number in unanswered
                    )
                )


                st.stop()


            # --------------------------------------
            # Calculate Score
            # --------------------------------------

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


                topic_results[
                    topic
                ]["total"] += 1


                if selected == correct:

                    score += 1

                    topic_results[
                        topic
                    ]["correct"] += 1


            # --------------------------------------
            # Calculate Percentage
            # --------------------------------------

            total = len(questions)


            percentage = round(
                (score / total) * 100,
                2
            )


            # --------------------------------------
            # Quiz Configuration
            # --------------------------------------

            quiz_config = st.session_state[
                "quiz_config"
            ]


            # --------------------------------------
            # Create Quiz Result
            # --------------------------------------

            quiz_result = {

                "score": score,

                "total": total,

                "percentage": percentage,

                "topic_results": topic_results,

                "skill": quiz_config["skill"],

                "level": quiz_config["level"],

                "goal": quiz_config["goal"],

                "difficulty": quiz_config["difficulty"]

            }


            # --------------------------------------
            # Store Latest Quiz Result
            # --------------------------------------

            st.session_state[
                "quiz_result"
            ] = quiz_result


            # --------------------------------------
            # Get Current Student ID
            # --------------------------------------

            student_id = student["id"]


            # --------------------------------------
            # Save Quiz Result
            # --------------------------------------

            save_quiz_result(
                student_id=student_id,
                skill=quiz_result["skill"],
                score=quiz_result["score"],
                total=quiz_result["total"],
                percentage=quiz_result["percentage"]
            )


            st.success(
                "💾 Quiz result saved to SQLite!"
            )


            # --------------------------------------
            # Store Progress History
            # --------------------------------------

            if "progress_history" not in st.session_state:

                st.session_state[
                    "progress_history"
                ] = []


            st.session_state[
                "progress_history"
            ].append(
                quiz_result
            )


            # --------------------------------------
            # Display Result
            # --------------------------------------

            st.success(
                f"🎉 Quiz completed! "
                f"Score: {score}/{total} "
                f"({percentage}%)"
            )


            # --------------------------------------
            # Performance Message
            # --------------------------------------

            if percentage >= 80:

                st.success(
                    "🟢 Excellent performance!"
                )

            elif percentage >= 60:

                st.info(
                    "🟡 Good performance. "
                    "Keep practicing."
                )

            else:

                st.warning(
                    "🔴 You need more practice "
                    "in this skill."
                )


            # --------------------------------------
            # Topic Performance
            # --------------------------------------

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