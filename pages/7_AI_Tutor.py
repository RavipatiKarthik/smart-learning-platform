import streamlit as st

from backend.chains.tutor_chain import create_tutor_chain


st.title("🤖 AI Tutor")

st.write(
    "Ask questions about your learning topics and get personalized explanations using RAG."
)

st.divider()


# Check student profile
if "student" not in st.session_state:

    st.warning(
        "Please complete your Student Profile first."
    )

    st.stop()


student = st.session_state["student"]


st.subheader("👤 Your Learning Profile")

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


st.subheader("💬 Ask Your AI Tutor")


question = st.text_area(
    "Enter your question",
    placeholder="Example: Explain encapsulation in Java with a simple example.",
    height=120
)


if st.button(
    "🤖 Ask AI Tutor",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "🤖 Searching learning material and generating answer..."
        ):

            try:

                tutor = create_tutor_chain()

                answer = tutor(
                    question,
                    student
                )

                st.session_state[
                    "tutor_answer"
                ] = answer

            except Exception as e:

                st.error(
                    "❌ Unable to generate the answer."
                )

                st.exception(e)


if "tutor_answer" in st.session_state:

    st.divider()

    st.subheader("📖 AI Tutor Answer")

    st.markdown(
        st.session_state["tutor_answer"]
    )


st.divider()

st.info(
    "💡 Tip: Ask questions related to your competency gaps "
    "to improve your weak areas."
)
