from openai import OpenAI
from config import GROQ_API_KEY, MODEL

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Say hello in one short sentence."
        }
    ]
)

print(response.choices[0].message.content)