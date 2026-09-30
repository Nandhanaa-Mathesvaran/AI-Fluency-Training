"""
Day 2: Self-Consistency with multiple Chain-of-Thought runs.
"""

from collections import Counter
from openai import OpenAI

from config import GROQ_API_KEY, MODEL


# Create Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


RUNS = 5
TEMPERATURE = 0.8


QUESTION = (
    "A student takes three courses costing Rs. 12,000, Rs. 18,000 and "
    "Rs. 15,000. She gets a 15% scholarship on the total and pays the "
    "rest in 4 equal instalments. How much is each instalment?"
)


COT_PROMPT = (
    "You are a helpful assistant. Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: "
    "Final Answer: <answer>"
)


def get_final_answer(text):

    for line in reversed(text.splitlines()):

        if "final answer" in line.lower():

            answer = line.split(":", 1)[-1].strip()

            # Remove common formatting
            answer = answer.replace("**", "")
            answer = answer.replace("₹", "")
            answer = answer.replace("Rs.", "")
            answer = answer.replace("Rs", "")
            answer = answer.replace(",", "")

            # Extract the numerical answer
            import re

            match = re.search(r"\d+(?:\.\d+)?", answer)

            if match:
                return match.group()

            return answer.strip()

    # Fallback if model doesn't write "Final Answer:"
    import re

    numbers = re.findall(r"\d+(?:\.\d+)?", text)

    if numbers:
        return numbers[-1]

    return "Unknown"

def run_once():

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": COT_PROMPT
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        temperature=TEMPERATURE,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    print("=" * 72)
    print("SELF-CONSISTENCY")
    print("=" * 72)

    print("\nQUESTION:")
    print(QUESTION)

    print("\n--- 5 CoT RUNS ---")

    answers = []

    for attempt in range(1, RUNS + 1):

        result = run_once()

        answer = get_final_answer(result)

        print(f"\nRun {attempt}:")
        print(answer)

        answers.append(float(answer))


    print("\n" + "=" * 72)
    print("MAJORITY VOTE")
    print("=" * 72)

    counts = Counter(answers)

    winner, count = counts.most_common(1)[0]

    print(f"Majority answer: {winner:.2f}")
    print(f"Votes: {count}/{RUNS}")