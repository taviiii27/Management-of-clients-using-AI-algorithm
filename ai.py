import os
import openai
from dotenv import load_dotenv

load_dotenv()  
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not set. put it in .env")

def responses(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Eroare OpenAI API: {e}")
        return f"Error: {e}"
