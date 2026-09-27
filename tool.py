from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = (
        "Useful for performing simple mathematical calculations. "
        "Input should be a mathematical expression such as 25*4 or 100/5."
    )

    def _run(self, expression: str) -> str:
        allowed = "0123456789+-*/(). %"

        if not all(char in allowed for char in expression):
            return "Invalid mathematical expression."

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except Exception:
            return "Could not calculate the expression."


class StudyPlannerTool(BaseTool):
    name: str = "Study Planner"
    description: str = (
        "Creates a simple study schedule based on available study time."
    )

    def _run(self, study_time: str) -> str:
        try:
            minutes = int(study_time)
        except ValueError:
            return (
                "Please provide study time as a number of minutes, "
                "for example 60."
            )

        if minutes <= 0:
            return "Study time must be greater than zero."

        explanation = round(minutes * 0.40)
        practice = round(minutes * 0.30)
        revision = minutes - explanation - practice

        return (
            f"Study Plan for {minutes} minutes:\n"
            f"- Explanation & learning: {explanation} minutes\n"
            f"- Practice & questions: {practice} minutes\n"
            f"- Revision & recall: {revision} minutes"
        )
