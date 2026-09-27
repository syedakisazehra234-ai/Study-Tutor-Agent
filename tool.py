from crewai.tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = (
        "Useful for performing basic mathematical calculations. "
        "Input should be a simple mathematical expression such as 25*4 or 100/5."
    )

    def _run(self, expression: str) -> str:
        try:
            allowed_characters = "0123456789+-*/(). "

            if not all(char in allowed_characters for char in expression):
                return "Invalid mathematical expression."

            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)

        except Exception:
            return "Unable to calculate the expression."


class StudyPlannerTool(BaseTool):
    name: str = "Study Planner"
    description: str = (
        "Creates a simple study schedule based on available study time "
        "in minutes."
    )

    def _run(self, minutes: int) -> str:

        try:
            minutes = int(minutes)

            if minutes <= 0:
                return "Study time must be greater than zero."

            explanation = round(minutes * 0.40)
            practice = round(minutes * 0.30)
            revision = minutes - explanation - practice

            return (
                f"Study plan for {minutes} minutes:\n"
                f"- {explanation} minutes: Learn/explain the concept\n"
                f"- {practice} minutes: Practice questions\n"
                f"- {revision} minutes: Revision and recall"
            )

        except Exception:
            return "Please provide study time as a number of minutes."
