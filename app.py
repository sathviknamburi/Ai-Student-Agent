import streamlit as st
from agent import create_study_plan


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📚 AI Study Planner")

st.markdown(
    """
    ### Create your personalized study plan with AI 🤖

    Enter your goal, subjects, available time, and current level.
    The AI will create a practical day-by-day study plan for you.
    """
)


st.divider()


# ============================================================
# SIDEBAR — STUDENT INFORMATION
# ============================================================

st.sidebar.header("🎓 Student Information")


name = st.sidebar.text_input(
    "Your Name",
    placeholder="Example: Sathvik"
)


goal = st.sidebar.text_input(
    "Your Goal",
    placeholder="Example: Crack placements"
)


current_level = st.sidebar.selectbox(
    "Current Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


subjects = st.sidebar.text_area(
    "Subjects / Topics",
    placeholder=(
        "Example:\n"
        "DSA\n"
        "Python\n"
        "Machine Learning\n"
        "SQL"
    ),
    height=150
)


hours_per_day = st.sidebar.number_input(
    "Study Hours Per Day",
    min_value=1,
    max_value=12,
    value=3,
    step=1
)


days = st.sidebar.number_input(
    "Number of Days",
    min_value=1,
    max_value=365,
    value=7,
    step=1
)


st.sidebar.divider()


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.sidebar.button(
    "🚀 Generate Study Plan",
    use_container_width=True,
    type="primary"
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if generate_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not name.strip():

        st.error("❌ Please enter your name.")

        st.stop()


    if not goal.strip():

        st.error("❌ Please enter your study goal.")

        st.stop()


    if not subjects.strip():

        st.error(
            "❌ Please enter at least one subject or topic."
        )

        st.stop()


    # --------------------------------------------------------
    # DISPLAY INPUT SUMMARY
    # --------------------------------------------------------

    st.subheader("📋 Your Study Details")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Student",
            name
        )


    with col2:

        st.metric(
            "Level",
            current_level
        )


    with col3:

        st.metric(
            "Hours / Day",
            hours_per_day
        )


    with col4:

        st.metric(
            "Days",
            days
        )


    st.divider()


    # --------------------------------------------------------
    # GENERATE STUDY PLAN
    # --------------------------------------------------------

    with st.spinner(
        "🤖 Groq AI is creating your personalized study plan..."
    ):

        plan = create_study_plan(
            name=name,
            goal=goal,
            current_level=current_level,
            subjects=subjects,
            hours_per_day=hours_per_day,
            days=days
        )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    if plan:

        st.success(
            "✅ Your personalized study plan is ready!"
        )

        st.divider()

        st.markdown(plan)


        # ----------------------------------------------------
        # DOWNLOAD PLAN
        # ----------------------------------------------------

        st.divider()

        st.subheader("📥 Save Your Study Plan")


        st.download_button(
            label="📄 Download Study Plan",
            data=plan,
            file_name="my_study_plan.md",
            mime="text/markdown",
            use_container_width=True
        )


else:

    # ========================================================
    # WELCOME SCREEN
    # ========================================================

    st.info(
        "👈 Enter your details in the sidebar and click "
        "**Generate Study Plan**."
    )


    st.subheader("✨ What this AI Study Planner does")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            ### 🎯 Personalized

            Creates a plan based on your:

            - Goal
            - Current level
            - Subjects
            - Available time
            """
        )


    with col2:

        st.markdown(
            """
            ### 🗓️ Day-by-Day

            You get:

            - Daily topics
            - Learning activities
            - Practice
            - Revision
            """
        )


    with col3:

        st.markdown(
            """
            ### 📈 Progress

            The plan includes:

            - Checkpoints
            - Expected outcomes
            - Consistency tips
            """
        )


    st.divider()


    st.subheader("🚀 Example")


    st.markdown(
        """
        **Goal:** Crack software placements

        **Subjects:** DSA, Java, SQL

        **Level:** Beginner

        **Available Time:** 3 hours/day

        **Duration:** 30 days

        The AI will convert these details into a structured
        30-day preparation plan.
        """
    )