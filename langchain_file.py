
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Cheia OPENAI_API_KEY nu a fost găsită!")

lang_model = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=openai_api_key
)

def model(prompt_text):
    messages = [HumanMessage(content=prompt_text)]
    response = lang_model.predict_messages(messages)
    return response.content
