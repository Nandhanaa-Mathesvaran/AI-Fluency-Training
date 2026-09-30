"""
Day 2: Compare answers with and without Chain-of-Thought.
"""

from openai import OpenAI
from config import GROQ_API_KEY, MODEL


# Create Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


QUESTIONS = [
    (
        "A student takes three courses costing Rs. 12,000, Rs. 18,000 and "
        "Rs. 15,000. She gets a 15% scholarship on the total and pays the "
        "rest in 4 equal instalments. How much is each instalment?"
    ),
    (
        "A lab has 18 computers. In the morning each computer is shared by "
        "2 students, and in the afternoon by 3 students. How many student "
        "sittings happen in one day?"
    ),
    (
        "Ravi is taller than Kumar. Kumar is taller than Arun. "
        "Priya is shorter than Arun. Who is the tallest and who is the shortest?"
    ),
]


DIRECT_PROMPT = (
    "You are a helpful assistant. Give only the final answer. "
    "Do not explain."
)


COT_PROMPT = (
    "You are a helpful assistant. Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: "
    "Final Answer: <answer>"
)


def ask(system_prompt, question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    print("=" * 72)
    print("CHAIN-OF-THOUGHT COMPARISON")
    print("=" * 72)

    for number, question in enumerate(QUESTIONS, start=1):

        print("\n" + "=" * 72)

        print(f"QUESTION {number}:")
        print(question)

        print("\n--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question))

        print("\n--- WITH CoT ---")
        print(ask(COT_PROMPT, question))

        print()