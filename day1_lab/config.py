import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")