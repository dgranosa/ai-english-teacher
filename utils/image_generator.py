import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_image(prompt, size="1024x1024", quality="standard", n=1):
  response = client.images.generate(
    model="dall-e-2",
    prompt=prompt,
    size=size,
    quality=quality,
    n=n,
  )

  return response.data[0].url