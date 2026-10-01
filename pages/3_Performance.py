import streamlit as st

st.title("📊 Performance Dashboard")

if "student" not in st.session_state:
    st.warning("Please complete your Student Profile first.")
    st.stop()

if "assessment" not in st.session_state:
    st.warning("Please complete the Skill Assessment first.")
    st.stop()

student = st.session_state["student"]
assessment = st.session_state["assessment"]

st.write(
    f"### Welcome, {student['name']} 👋"
)

st.write(
    f"Target Skill: **{student['target_skill']}**"
)

st.divider()

# Overall performance
score = assessment["score"]
total = assessment["total"]
percentage = assessment["percentage"]

st.subheader("🎯 Overall Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Assessment Score",
        f"{score}/{total}"
    )

with col2:
    st.metric(
        "Percentage",
        f"{percentage:.0f}%"
    )

with col3:

    if percentage >= 80:
        level = "Excellent"
    elif percentage >= 60:
        level = "Good"
    elif percentage >= 40:
        level = "Needs Improvement"
    else:
        level = "Beginner"

    st.metric(
        "Performance Level",
        level
    )

st.divider()

# Progress bar
st.subheader("📈 Overall Progress")

st.progress(percentage / 100)

st.write(
    f"You have achieved **{percentage:.0f}%** "
    "in your current assessment."
)

st.divider()

# Topic performance
st.subheader("📚 Topic Performance")

topic_results = assessment["topic_results"]

for topic, result in topic_results.items():

    topic_score = (
        result["correct"] / result["total"]
    ) * 100

    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"**{topic}**")

    with col2:
        st.write(f"**{topic_score:.0f}%**")

    st.progress(topic_score / 100)

st.divider()

# Strong and weak areas
strong_topics = []
weak_topics = []

for topic, result in topic_results.items():

    topic_score = (
        result["correct"] / result["total"]
    ) * 100

    if topic_score >= 80:
        strong_topics.append(topic)

    elif topic_score < 60:
        weak_topics.append(topic)

col1, col2 = st.columns(2)

with col1:

    st.subheader("💪 Strong Areas")

    if strong_topics:

        for topic in strong_topics:
            st.success(f"✓ {topic}")

    else:
        st.info("No strong areas identified yet.")

with col2:

    st.subheader("⚠️ Areas to Improve")

    if weak_topics:

        for topic in weak_topics:
            st.warning(f"⚠ {topic}")

    else:
        st.success("No major weak areas!")

st.divider()

# Learning recommendation
st.subheader("🎯 Current Recommendation")

if weak_topics:

    st.info(
        "Focus on: "
        + ", ".join(weak_topics)
        + ". These topics will be used to create "
        "your personalized learning plan."
    )

else:

    st.success(
        "Your fundamentals are strong. "
        "You can move to advanced topics."
    )