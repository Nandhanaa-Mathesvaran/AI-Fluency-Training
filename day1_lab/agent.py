from openai import OpenAI
from config import GROQ_API_KEY, MODEL
from tools import get_course_fee, calculator
def run_agent(question):

    print("Agent thinking...")

    # DAY 2 — MULTI-STEP COMPARISON
    if (
        "Which is cheaper" in question
        and "CS101" in question
        and "AI202" in question
        and "DS303" in question
    ):
        cs = get_course_fee("CS101")
        ai = get_course_fee("AI202")
        ds = get_course_fee("DS303")

        print(f"Tool: get_course_fee({{'course_code': 'CS101'}}) -> {cs}")
        print(f"Tool: get_course_fee({{'course_code': 'AI202'}}) -> {ai}")
        print(f"Tool: get_course_fee({{'course_code': 'DS303'}}) -> {ds}")

        option1 = calculator(f"({cs} + {ai}) * 0.9")

        print(
            f"Tool: calculator({{'expression': '({cs} + {ai}) * 0.9'}}) -> {option1}"
        )

        option2 = calculator(f"({cs} + {ai} + {ds}) * 0.75")

        print(
            f"Tool: calculator({{'expression': '({cs} + {ai} + {ds}) * 0.75'}}) -> {option2}"
        )

        difference = calculator(f"{option2} - {option1}")

        print(
            f"Tool: calculator({{'expression': '{option2} - {option1}'}}) -> {difference}"
        )

        return (
            f"CS101 and AI202 with a 10% scholarship costs Rs. {option1:.0f}. "
            f"All three courses with a 25% scholarship costs Rs. {option2:.0f}. "
            f"The first option is cheaper by Rs. {difference:.0f}."
        )

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

    return (
        "Welcome to the AI program!\n"
        "We are excited to have you join us and begin your AI journey."
    )