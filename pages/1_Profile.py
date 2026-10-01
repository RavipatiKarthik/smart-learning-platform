import streamlit as st

from backend.database.db import (
    save_student,
    get_students
)


st.title("👤 Student Profile")

st.write(
    "Create a new student profile or continue with an existing student."
)

st.divider()


# --------------------------------------------------
# Select New / Existing Student
# --------------------------------------------------

option = st.radio(
    "Choose an option",
    [
        "🆕 New Student",
        "👤 Existing Student"
    ],
    horizontal=True
)


# ==================================================
# EXISTING STUDENT
# ==================================================

if option == "👤 Existing Student":

    students = get_students()

    if not students:

        st.info(
            "No existing students found. "
            "Please create a new student profile."
        )

    else:

        student_options = {}

        for student in students:

            student_id = student[0]
            name = student[1]
            college = student[2]
            branch = student[3]

            display_name = (
                f"{name} | {college} | {branch}"
            )

            student_options[display_name] = student

        selected = st.selectbox(
            "Select Existing Student",
            list(student_options.keys())
        )

        if st.button(
            "✅ Continue as This Student",
            use_container_width=True
        ):

            student = student_options[selected]

            st.session_state["student"] = {
                "id": student[0],
                "name": student[1],
                "college": student[2],
                "branch": student[3],
                "year": student[4],
                "target_skill": student[5],
                "learning_goal": student[6]
            }

            st.success(
                f"Welcome back, {student[1]}! 👋"
            )

            st.rerun()


# ==================================================
# NEW STUDENT
# ==================================================

else:

    st.subheader("🆕 Create New Student Profile")

    with st.form("student_profile_form"):

        name = st.text_input(
            "Full Name"
        )

        col1, col2 = st.columns(2)

        with col1:

            college = st.text_input(
                "College Name"
            )

            branch = st.selectbox(
                "Branch",
                [
                    "CSE",
                    "ECE",
                    "EEE",
                    "MECH",
                    "CIVIL",
                    "IT",
                    "Other"
                ]
            )

        with col2:

            year = st.selectbox(
                "Academic Year",
                [
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "Final Year"
                ]
            )

            target_skill = st.selectbox(
                "Target Skill",
                [
                    "Java",
                    "Python",
                    "Data Structures",
                    "DBMS",
                    "Operating Systems",
                    "Computer Networks",
                    "AI / ML"
                ]
            )

        learning_goal = st.selectbox(
            "Learning Goal",
            [
                "Placement Preparation",
                "Academic Improvement",
                "Competitive Programming",
                "Project Development",
                "Skill Development"
            ]
        )

        submitted = st.form_submit_button(
            "💾 Create Profile",
            use_container_width=True
        )

        if submitted:

            if not name or not college:

                st.error(
                    "Please enter your name and college."
                )

            else:

                student = {
                    "name": name,
                    "college": college,
                    "branch": branch,
                    "year": year,
                    "target_skill": target_skill,
                    "learning_goal": learning_goal
                }

                save_student(student)

                students = get_students()

                student_id = students[-1][0]

                student["id"] = student_id

                st.session_state["student"] = student

                st.success(
                    f"✅ Profile created successfully for {name}!"
                )

                st.rerun()


# ==================================================
# CURRENT STUDENT
# ==================================================

if "student" in st.session_state:

    student = st.session_state["student"]

    st.divider()

    st.subheader("📋 Current Student")

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
            f"**Year:** {student['year']}"
        )

        st.write(
            f"**Target Skill:** {student['target_skill']}"
        )

        st.write(
            f"**Goal:** {student['learning_goal']}"
        )

    st.success(
        "✅ This student is currently active."
    )