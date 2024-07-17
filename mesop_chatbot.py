import random
import time
import mesop as me
import mesop.labs as mel
import requests
import os
from dotenv import load_dotenv

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'  
MODEL_NAME = os.getenv('MODEL_NAME')

@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/chat",
  title="Mesop Demo Chat",
)
def page():
  mel.chat(transform, title="Mesop Demo Chat", bot_user="Mesop Bot")

def transform(input: str, history: list[mel.ChatMessage]):
  headers = {
      'Authorization': f'Bearer {GROQ_API_KEY}',
      'Content-Type': 'application/json'
  }

  data = {
      'model': MODEL_NAME,
      'messages': [{'role': 'user', 'content': input}]
  }

  try:
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    if response.status_code == 200:
      result = response.json()
      for choice in result.get('choices', []):
        yield choice['message']['content'] + " "
    else:
      yield "I'm having trouble connecting to the Groq API right now."
  except Exception as e:
    print(f"Exception: {e}")
    yield "An error occurred while connecting to the Groq API."

# Sample static lines (could be removed or modified if needed)
LINES = [
  "Hello! How can I assist you today?",
  "I'm here to help with any questions you have.",
  "Feel free to ask me anything about our services.",
]
