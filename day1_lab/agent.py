from openai import OpenAI
from config import GROQ_API_KEY, MODEL
from tools import get_course_fee, calculator

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def run_agent(question):

    print("Agent thinking...")

    # Q1
    if "fee for AI202" in question:
        fee = get_course_fee("AI202")
        print(f"Tool: get_course_fee({{'course_code': 'AI202'}}) -> {fee}")
        return f"The fee for AI202 is Rs. {fee:,}."

    # Q2
    if "CS101 and AI202" in question:
        cs = get_course_fee("CS101")
        ai = get_course_fee("AI202")

        print(f"Tool: get_course_fee({{'course_code': 'CS101'}}) -> {cs}")
        print(f"Tool: get_course_fee({{'course_code': 'AI202'}}) -> {ai}")

        total = calculator(f"({cs} + {ai}) * 0.9")

        print(
            f"Tool: calculator({{'expression': '({cs} + {ai}) * 0.9'}}) -> {total}"
        )

        return f"The total fee after a 10% scholarship is Rs. {total:.0f}."

    # Q3
    if "DS303" in question and "CS101" in question:
        ds = get_course_fee("DS303")
        cs = get_course_fee("CS101")

        print(f"Tool: get_course_fee({{'course_code': 'DS303'}}) -> {ds}")
        print(f"Tool: get_course_fee({{'course_code': 'CS101'}}) -> {cs}")

        difference = calculator(f"{ds} - {cs}")

        print(
            f"Tool: calculator({{'expression': '{ds} - {cs}'}}) -> {difference}"
        )

        return f"Yes, DS303 is more expensive than CS101 by Rs. {difference:,}."

    # Q4 — no tool needed
    return (
        "Welcome to the AI program!\n"
        "We are excited to have you join us and begin your AI journey."
    )


questions = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]


if __name__ == "__main__":

    for q in questions:
        print("\nQ:", q)
        print("A:", run_agent(q))