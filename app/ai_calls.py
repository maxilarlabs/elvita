from dotenv import load_dotenv
from twilio.rest import Client
from groq import AsyncGroq
from elevenlabs.client import AsyncElevenLabs

import os, asyncio, uuid

load_dotenv()

GROQ=os.environ.get("GROQ")
ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

groq_client = AsyncGroq(api_key=GROQ)

eleven_client = AsyncElevenLabs(
  api_key=ELEVENLABS_API_KEY,
  timeout=600
)

async def generar_voz(texto:str):

  abuela="eBthAb30UYbt2nojGXeA"
  jorge="HAsl3FenyWHYwECSP6Hl"
  cristina="CaJslL1xziwefCeTNzHv"
  jorge_2 = "ByVRQtaK1WDOvTmP1PKO"
  
  results = eleven_client.text_to_speech.stream(
    voice_id=jorge_2,
    output_format="ulaw_8000",
    text=texto,
    model_id="eleven_flash_v2_5")

  async for value in results: yield value

async def transcript(path:str):

  with open(path, "rb") as file:

    transcription = await groq_client.audio.transcriptions.create(
      file=file,
      model="whisper-large-v3-turbo",
      prompt="El audio ha escuchar es recolectado en tiempo real de una llamada telefónica en Lima Peru. En caso no detectas nada, devuelve una cadena vacia.",
      response_format="text",
      language="es",
      temperature=0.0
    )

  return transcription