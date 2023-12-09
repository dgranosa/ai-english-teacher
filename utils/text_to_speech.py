import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def text_to_speech(text):
  response = client.audio.speech.create(
      model="tts-1",
      voice="nova",
      input=text,
  )

  return response.read()

if __name__ == '__main__':
  text_to_speech("Hello, world!")