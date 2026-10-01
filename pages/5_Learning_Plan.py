import streamlit as st

from backend.chains.learning_chain import generate_learning_plan
from backend.database.db import save_learning_plan


st.title("📚 Personalized Learning Plan")

st.write(
    "Get an AI-generated learning plan based on your competency gaps and target skill."
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


# --------------------------------------------------
# Check Competency Gaps
# --------------------------------------------------

if "competency_gaps" not in st.session_state:

    st.warning(
        "Please complete the Competency Gap Analysis first."
    )

    st.stop()


student = st.session_state["student"]

gaps = st.session_state.get(
    "competency_gaps",
    []
)

moderate_topics = st.session_state.get(
    "moderate_topics",
    []
)


# --------------------------------------------------
# Student Information
# --------------------------------------------------

st.subheader("👤 Student Information")

col1, col2 = st.columns(2)


with col1:

    st.write(
        f"**Name:** {student['name']}"
    )

    st.write(
        f"**Target Skill:** {student['target_skill']}"
    )


with col2:

    st.write(
        f"**Branch:** {student['branch']}"
    )

    st.write(
        f"**Goal:** {student['learning_goal']}"
    )


st.divider()


# --------------------------------------------------
# Competency Gaps
# --------------------------------------------------

st.subheader("🎯 Your Competency Gaps")

if gaps:

    for topic in gaps:

        st.write(
            f"🔴 **{topic}**"
        )

else:

    st.success(
        "🎉 No major competency gaps detected!"
    )


# --------------------------------------------------
# Moderate Topics
# --------------------------------------------------

if moderate_topics:

    st.subheader("🟡 Topics to Improve")

    for topic in moderate_topics:

        st.write(
            f"⚠️ **{topic}**"
        )


st.divider()


# --------------------------------------------------
# Generate Learning Plan
# --------------------------------------------------

if st.button(
    "🤖 Generate Personalized Learning Plan",
    use_container_width=True
):

    with st.spinner(
        "🤖 AI is creating your personalized learning plan..."
    ):

        try:

            # Generate plan using AI + RAG

            plan = generate_learning_plan(
                student,
                gaps,
                moderate_topics
            )


            # Store plan in session

            st.session_state[
                "learning_plan"
            ] = plan


            # ------------------------------------------
            # Get Current Student ID
            # ------------------------------------------

            student_id = student["id"]


            # ------------------------------------------
            # Save Learning Plan
            # ------------------------------------------

            save_learning_plan(
                student_id=student_id,
                skill=student["target_skill"],
                goal=student["learning_goal"],
                plan=plan
            )


            st.success(
                "✅ Personalized learning plan generated and saved!"
            )


        except Exception as e:

            st.error(
                "❌ Unable to generate the learning plan."
            )

            st.exception(e)


# --------------------------------------------------
# Display Learning Plan
# --------------------------------------------------

if "learning_plan" in st.session_state:

    plan = st.session_state[
        "learning_plan"
    ]

    st.divider()

    st.subheader(
        "🗓️ Your AI Personalized Learning Plan"
    )


    for index, item in enumerate(
        plan,
        start=1
    ):

        priority = item.get(
            "priority",
            "Medium"
        )


        st.markdown(
            f"### Day {index}: {item['topic']}"
        )


        st.write(
            f"**Priority:** {priority}"
        )


        st.write(
            f"**Duration:** {item['duration']}"
        )


        st.write(
            "📖 **Concepts to Learn:**"
        )


        for concept in item["concepts"]:

            st.write(
                f"• {concept}"
            )


        st.write(
            f"📝 **Practice Activity:** "
            f"{item['activity']}"
        )


        st.divider()


    st.success(
        "🎉 Your personalized learning plan is ready!"
    )


# --------------------------------------------------
# Recommended Learning Process
# --------------------------------------------------

st.subheader(
    "🚀 Recommended Learning Process"
)


st.write(
    "1. 📄 Study the recommended topic"
)


st.write(
    "2. 🤖 Ask questions using the AI Tutor"
)


st.write(
    "3. 📝 Take a topic-based quiz"
)


st.write(
    "4. 📊 Review incorrect answers"
)


st.write(
    "5. 🔄 Reassess your competency"
)
