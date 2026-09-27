from crewai import Agent, Task, Crew, Process, LLM
from study_tools import CalculatorTool, StudyPlannerTool
from memory import create_memory
from config import MODEL_NAME

def create_study_crew():

    # -------------------------
    # LLM
    # -------------------------

    llm = LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.3
    )

    # -------------------------
    # Tools
    # -------------------------

    calculator = CalculatorTool()
    study_planner = StudyPlannerTool()

    tools = [
        calculator,
        study_planner
    ]

    # -------------------------
    # Memory
    # -------------------------

    memory = create_memory()

    # -------------------------
    # Agent
    # -------------------------

    tutor = Agent(
        role="Personal Study Tutor",

        goal=(
            "Help students understand academic topics clearly, "
            "efficiently and according to their learning level."
        ),

        backstory=(
            "You are an experienced academic tutor. "
            "You explain difficult concepts using simple language, "
            "adapt explanations to the student's level, "
            "focus on conceptual understanding, "
            "and help students prepare effectively for exams."
        ),

        llm=llm,

        tools=tools,

        memory=memory,

        verbose=True,

        allow_delegation=False
    )

    # -------------------------
    # Task
    # -------------------------

    study_task = Task(

        description="""
        Create a personalized study session for the student.

        Student information:

        Subject:
        {subject}

        Topic:
        {topic}

        Student Level:
        {level}

        Learning Goal:
        {goal}

        Available Study Time:
        {study_time} minutes

        Previous learning context:
        {previous_context}

        Your response must contain:

        1. Topic overview
        2. Simple explanation
        3. Core concepts
        4. Important exam points
        5. Common mistakes or misconceptions
        6. Memory aid
        7. Practice questions
        8. Five MCQs with answers
        9. A study plan based on the available time

        Adapt the difficulty to the student's level.

        If a tool is useful, use the appropriate tool.

        Do not make up citations or claim that you consulted
        external sources when you did not.
        """,

        expected_output="""
        A clear, structured and student-friendly study session
        containing explanations, key concepts, exam points,
        practice questions, MCQs and a time-based study plan.
        """,

        agent=tutor
    )

    # -------------------------
    # Crew
    # -------------------------

    crew = Crew(

        agents=[tutor],

        tasks=[study_task],

        process=Process.sequential,

        memory=memory,

        verbose=True
    )

    return crew
