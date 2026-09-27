import streamlit as st

from crew import create_study_crew


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# LOAD CUSTOM CSS
# =========================================================

def load_css():

    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero-container">

        <div class="status-pill">
            <span class="status-dot"></span>
            AI STUDY ASSISTANT
        </div>

        <h1 class="hero-title">
            Study Smarter.<br>
            <span>Not Harder.</span>
        </h1>

        <p class="hero-subtitle">
            Your personalized AI tutor for understanding concepts,
            preparing for exams, and mastering difficult topics.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MAIN INPUT CARD
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        <span class="heading-icon">✦</span>
        Create Your Study Session
    </div>
    """,
    unsafe_allow_html=True
)


# Two-column layout
col1, col2 = st.columns(2, gap="large")


with col1:

    st.markdown(
        '<div class="input-label">SUBJECT</div>',
        unsafe_allow_html=True
    )

    subject = st.text_input(
        "Subject",
        placeholder="e.g. Pharmacology",
        label_visibility="collapsed"
    )


    st.markdown(
        '<div class="input-label">TOPIC</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Topic",
        placeholder="e.g. Beta Blockers",
        label_visibility="collapsed"
    )


    st.markdown(
        '<div class="input-label">LEARNING GOAL</div>',
        unsafe_allow_html=True
    )

    goal = st.selectbox(
        "Learning Goal",
        [
            "Understand the topic",
            "Exam preparation",
            "Quick revision",
            "Practice questions"
        ],
        label_visibility="collapsed"
    )


with col2:

    st.markdown(
        '<div class="input-label">YOUR LEVEL</div>',
        unsafe_allow_html=True
    )

    level = st.selectbox(
        "Student Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        label_visibility="collapsed"
    )


    st.markdown(
        '<div class="input-label">AVAILABLE STUDY TIME</div>',
        unsafe_allow_html=True
    )

    study_time = st.slider(
        "Study Time",
        min_value=10,
        max_value=300,
        value=60,
        step=10,
        label_visibility="collapsed"
    )

    st.markdown(
        f"""
        <div class="time-display">
            <span>⏱</span>
            <strong>{study_time}</strong> minutes available
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="tip-card">
            <span class="tip-icon">💡</span>
            <div>
                <strong>Study tip</strong>
                <p>
                    Short focused sessions usually work better
                    than passive reading.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# START BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

start = st.button(
    "✦  GENERATE MY STUDY SESSION",
    use_container_width=True
)


# =========================================================
# AI GENERATION
# =========================================================

if start:

    if not subject.strip():

        st.warning(
            "Please enter a subject before starting."
        )

    elif not topic.strip():

        st.warning(
            "Please enter a topic before starting."
        )

    else:

        with st.spinner(
            "Your AI tutor is preparing your study session..."
        ):

            try:

                crew = create_study_crew()

                result = crew.kickoff(
                    inputs={
                        "subject": subject,
                        "topic": topic,
                        "level": level,
                        "goal": goal,
                        "study_time": study_time,
                        "previous_context": (
                            "Use relevant memories from previous "
                            "study sessions when available."
                        )
                    }
                )

                # =================================================
                # RESULT HEADER
                # =================================================

                st.markdown(
                    """
                    <div class="result-header">

                        <div class="result-icon">
                            🧠
                        </div>

                        <div>
                            <h2>Your Personalized Study Session</h2>
                            <p>
                                Generated by your AI Study Tutor
                            </p>
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # =================================================
                # RESULT
                # =================================================

                st.markdown(
                    '<div class="result-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    result.raw
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    "Something went wrong while generating "
                    "your study session."
                )

                with st.expander("Technical details"):

                    st.exception(e)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        <div class="footer-line"></div>

        <p>
            Built with
            <span>Streamlit</span> ×
            <span>CrewAI</span> ×
            <span>Groq</span>
        </p>

        <small>
            AI-generated educational content should be reviewed
            against your course materials and trusted sources.
        </small>

    </div>
    """,
    unsafe_allow_html=True
)
