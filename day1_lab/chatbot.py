from openai import OpenAI
from config import GROQ_API_KEY, MODEL

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

questions = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]

for question in questions:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": question}
        ]
    )

    print("\nQ:", question)
    print("A:", response.choices[0].message.content)