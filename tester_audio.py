import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ=os.environ.get("GROQ")

# Initialize the Groq client
client = Groq(api_key=GROQ)

# Specify the path to the audio file
filename = "pruebas.wav" 

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=file, 
      model="whisper-large-v3-turbo",
      prompt="Vas a recibir fragmentos del audio de una llamada en español latino",
      response_format="text",
      language="es",
      temperature=0.0
      #timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)

    )
    # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
    print(transcription)