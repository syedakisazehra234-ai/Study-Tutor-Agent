from crewai import Agent, Task, Crew, Process, LLM

# Fix CrewAI + Groq cache_breakpoint incompatibility
try:
    import crewai.llms.cache as crew_cache
    crew_cache.mark_cache_breakpoint = lambda msg: msg
except Exception:
    pass

from study_tools import CalculatorTool, StudyPlannerTool
from memory import create_memory
from config import MODEL_NAME

def create_study_crew():

    memory = create_memory()

    llm = LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.3
    )

    tools = [
        CalculatorTool(),
        StudyPlannerTool()
    ]

    tutor = Agent(
        role="AI Study Tutor",
        goal="Help students understand academic topics clearly and prepare effectively for exams.",
        backstory=(
            "You are a patient and structured academic tutor. "
            "You explain difficult concepts in simple language and "
            "help students prepare efficiently for examinations."
        ),
        llm=llm,
        tools=tools,
        memory=memory,
        verbose=True,
        allow_delegation=False
    )

    task = Task(
        description="""
        Create a comprehensive study guide based on the student's inputs.

        Subject: {subject}
        Topic: {topic}
        Student level: {level}
        Learning goal: {goal}
        Available study time: {study_time}

        Provide:

        1. Topic overview
        2. Simple explanation
        3. Core concepts
        4. Important exam points
        5. Common mistakes
        6. Memory aid
        7. Practice questions
        8. Five MCQs with answers
        9. Personalized study plan

        Keep the explanation appropriate for the student's level.
        """,

        expected_output="""
        A clear and structured study guide containing:
        - Topic overview
        - Simple explanation
        - Core concepts
        - Exam points
        - Common mistakes
        - Memory aid
        - Practice questions
        - 5 MCQs with answers
        - Study plan
        """,

        agent=tutor
    )

    crew = Crew(
        agents=[tutor],
        tasks=[task],
        process=Process.sequential,
        memory=memory,
        verbose=True
    )

    return crew
