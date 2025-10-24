# take_forge/core/openai_client.py
from openai import OpenAI
import os

# Initialize once, reuse everywhere
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
