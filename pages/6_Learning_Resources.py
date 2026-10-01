import streamlit as st
from pathlib import Path


st.title("📚 Learning Resources")

st.write(
    "Access learning materials recommended according to your competency gaps."
)

st.divider()


# Check student
if "student" not in st.session_state:

    st.warning(
        "Please complete your Student Profile first."
    )

    st.stop()


# Check competency gaps
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


# No gaps
if not gaps:

    st.success(
        "🎉 No major competency gaps detected!"
    )

    st.info(
        "You can explore advanced learning materials."
    )

    st.stop()


st.subheader("🎯 Recommended Learning Materials")


# Java document mapping
document_mapping = {

    "Java Basics":
        "java_basics.pdf",

    "Variables and Data Types":
        "java_basics.pdf",

    "OOP":
        "oop.pdf",

    "Java OOP":
        "oop.pdf",

    "Encapsulation":
        "oop.pdf",

    "Inheritance":
        "oop.pdf",

    "Polymorphism":
        "oop.pdf",

    "Abstraction":
        "oop.pdf",

    "Collections":
        "collections.pdf",

    "Exception Handling":
        "exception_handling.pdf",

    "Loops":
        "java_basics.pdf"

}


documents_folder = Path(
    "data/documents/java"
)


for gap in gaps:

    st.markdown(
        f"### 🔴 {gap}"
    )

    file_name = document_mapping.get(
        gap
    )


    if not file_name:

        st.warning(
            f"No learning document mapped for **{gap}**."
        )

        st.divider()

        continue


    file_path = (
        documents_folder / file_name
    )


    if file_path.exists():

        st.success(
            f"📄 Recommended: {file_name}"
        )


        with open(
            file_path,
            "rb"
        ) as file:

            pdf_data = file.read()


        st.download_button(

            label="⬇️ Download Learning Document",

            data=pdf_data,

            file_name=file_name,

            mime="application/pdf",

            key=f"download_{gap}"

        )


        st.info(
            "📖 Study this document before taking the topic quiz."
        )


    else:

        st.error(
            f"❌ Document not found: {file_name}"
        )


    st.divider()


# Learning process
st.subheader(
    "🚀 Recommended Learning Process"
)

st.write(
    "1. 📄 Study the recommended document"
)

st.write(
    "2. 🤖 Ask questions using AI Tutor"
)

st.write(
    "3. 📝 Take the topic-based quiz"
)

st.write(
    "4. 📊 Review your performance"
)

st.write(
    "5. 🔄 Reassess your competency"
)
