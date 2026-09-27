import streamlit as st
from pathlib import Path

from crew import create_study_crew


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# LOAD CUSTOM CSS
# =========================================================

css_file = Path(__file__).parent / "styles.css"

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 25px 10px 15px 10px;
    ">
        <div style="
            display: inline-block;
            padding: 7px 16px;
            border-radius: 999px;
            border: 1px solid rgba(0, 229, 255, 0.25);
            background: rgba(0, 229, 255, 0.06);
            color: #00e5ff;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
        ">
            🟢 AI STUDY ASSISTANT
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 style="
        text-align: center;
        font-size: clamp(42px, 6vw, 70px);
        line-height: 1.05;
        margin: 15px 0 10px 0;
        font-weight: 800;
        color: #f8fafc;
    ">
        Study Smarter.<br>
        <span style="
            background: linear-gradient(
                90deg,
                #00e5ff,
                #38bdf8,
                #7c3aed
            );
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        ">
            Not Harder.
        </span>
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="
        text-align: center;
        max-width: 700px;
        margin: 0 auto 35px auto;
        color: #94a3b8;
        font-size: 16px;
        line-height: 1.7;
    ">
        Your personalized AI tutor for understanding concepts,
        preparing for exams, and mastering difficult topics.
    </p>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# APPLICATION HEADER
# =========================================================

st.markdown("## 🎓 Build Your Study Session")

st.caption(
    "Tell the tutor what you want to learn and it will create "
    "a structured study guide for you."
)


# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2, gap="large")


with col1:

    subject = st.text_input(
        "📚 Subject",
        placeholder="e.g. Pharmacology",
        help="Enter the subject you are studying.",
    )

    topic = st.text_input(
        "🔬 Topic",
        placeholder="e.g. Pharmacokinetics",
        help="Enter the specific topic you want to study.",
    )

    level = st.selectbox(
        "🎓 Student Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
        index=0,
    )


with col2:

    goal = st.selectbox(
        "🎯 Learning Goal",
        [
            "Understand the concept",
            "Prepare for an exam",
            "Quick revision",
            "Practice questions",
            "Deep understanding",
        ],
        index=1,
    )

    study_time = st.number_input(
        "⏱️ Available Study Time (minutes)",
        min_value=10,
        max_value=600,
        value=60,
        step=10,
        help="How much time do you have available for this study session?",
    )

    st.markdown(
        """
        <div style="
            padding: 15px;
            margin-top: 10px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.07);
            background: rgba(255,255,255,0.025);
        ">
            <div style="
                color: #94a3b8;
                font-size: 12px;
                line-height: 1.6;
            ">
                💡 <b style="color:#cbd5e1;">Tip:</b>
                For better results, use a specific topic rather
                than an entire subject.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# START BUTTON
# =========================================================

st.markdown("")

start_button = st.button(
    "🚀 Create My Study Guide",
    type="primary",
    use_container_width=True,
)


# =========================================================
# AGENT EXECUTION
# =========================================================

if start_button:

    # ---------------------------------------------
    # Validate inputs
    # ---------------------------------------------

    if not subject.strip():
        st.warning("Please enter a subject.")

        st.stop()

    if not topic.strip():
        st.warning("Please enter a topic.")

        st.stop()


    # ---------------------------------------------
    # Progress / status area
    # ---------------------------------------------

    status_container = st.empty()

    status_container.info(
        "🧠 AI Study Tutor is preparing your personalized study guide..."
    )


    try:

        # -----------------------------------------
        # Create Crew
        # -----------------------------------------

        crew = create_study_crew()


        # -----------------------------------------
        # Prepare inputs
        # -----------------------------------------

        inputs = {
            "subject": subject,
            "topic": topic,
            "level": level,
            "goal": goal,
            "study_time": str(study_time),
            "previous_context": "",
        }


        # -----------------------------------------
        # Run CrewAI
        # -----------------------------------------

        with st.spinner(
            "🤖 Study Tutor is thinking and building your guide..."
        ):

            result = crew.kickoff(
                inputs=inputs
            )


        # -----------------------------------------
        # Success
        # -----------------------------------------

        status_container.success(
            "✅ Your personalized study guide is ready!"
        )


        # -----------------------------------------
        # Result Header
        # -----------------------------------------

        st.markdown("")

        st.markdown(
            """
            <div style="
                padding: 18px 20px;
                margin-top: 10px;
                margin-bottom: 20px;
                border-radius: 15px;
                border: 1px solid rgba(0,229,255,0.12);
                background: rgba(0,229,255,0.035);
            ">
                <div style="
                    color:#00e5ff;
                    font-size:11px;
                    font-weight:700;
                    letter-spacing:1.4px;
                ">
                    AI GENERATED STUDY GUIDE
                </div>

                <div style="
                    color:#f8fafc;
                    font-size:24px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    Ready to Learn 🚀
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        # -----------------------------------------
        # Display Result
        # -----------------------------------------

        if hasattr(result, "raw"):

            st.markdown(result.raw)

        else:

            st.markdown(str(result))


    except Exception as e:

        status_container.error(
            "❌ The AI Study Tutor could not complete the request."
        )

        st.error(
            "Something went wrong while running the study tutor."
        )

        with st.expander("Technical details"):

            st.code(
                str(e)
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px 10px 25px 10px;
    ">

        <div style="
            color:#64748b;
            font-size:13px;
        ">
            Built with
            <span style="color:#00e5ff;font-weight:600;">
                Streamlit
            </span>
            ×
            <span style="color:#00e5ff;font-weight:600;">
                CrewAI
            </span>
            ×
            <span style="color:#00e5ff;font-weight:600;">
                Groq
            </span>
        </div>

        <div style="
            color:#475569;
            font-size:11px;
            line-height:1.6;
            max-width:650px;
            margin:10px auto 0 auto;
        ">
            AI-generated educational content should be reviewed
            against your course materials and trusted sources.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
