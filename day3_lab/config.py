import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Create the API client
if PROVIDER == "groq":
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = OpenAI(
        api_key=GROQ_API_KEY
    )


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)