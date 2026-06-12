import os
from groq import Groq
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file (find_dotenv searches parent directories)
load_dotenv(find_dotenv())

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        response_format={"type": "json_object"}  
    )

    return response.choices[0].message.content

