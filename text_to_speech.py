from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")

client = OpenAI(api_key=config['OPENAI_API_KEY'])

def text_to_speech(text):
  response = client.audio.speech.create(
      model="tts-1",
      voice="nova",
      input=text,
  )

  return response.read()

if __name__ == '__main__':
  text_to_speech("Hello, world!")