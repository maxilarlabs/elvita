import os

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from groq import AsyncGroq

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY=os.environ.get("ANTHROPIC_API_KEY")
OPENAI_KEY=os.environ.get("OPENAI_KEY")
GROQ=os.environ.get("GROQ")

client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
openai_client = AsyncOpenAI(api_key=OPENAI_KEY)
groq_client = AsyncGroq(api_key=GROQ)

async def call_claude(sistema,messages,modelo="claude-haiku-4-5-20251001",temperatura=0):

  response = await client.messages.create(
      model=modelo,
      system=sistema,
      messages=messages,
      temperature=temperatura,
      max_tokens=8000
  )

  print(response)

  return response.content[0].text

async def call_luna(sistema,messages,modelo="gpt-5.6-luna"):

  full_messages=[{"role": "system","content": sistema}] + messages

  # gpt-5.6-luna solo soporta el temperature default (1), no se puede ajustar
  response = await openai_client.chat.completions.create(
      model=modelo,
      messages=full_messages,
  )

  print(response)

  return response.choices[0].message.content

async def call_groq_llama(sistema,messages,modelo="llama-3.3-70b-versatile",temperatura=0):

  full_messages=[{"role": "system","content": sistema}] + messages

  response = await groq_client.chat.completions.create(
      model=modelo,
      messages=full_messages,
      temperature=temperatura,
  )

  print(response)

  return response.choices[0].message.content
