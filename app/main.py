from app import api_models, vad_detector, ai_calls, wrappers

from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from fastapi.responses import HTMLResponse, JSONResponse

import websockets, os, base64, json, base64, time
import numpy as np
import torch

monolito = FastAPI(title="Elvita API")

monolito.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@monolito.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):

    print("INCOMING CALL")

    form_data = await request.form()  # Get the incoming Twilio request data

    caller_number = form_data.get("To", "Unknown")  # Extract the caller's phone number

    response = VoiceResponse()
    
    host = request.url.hostname
    connect = Connect()
    
    connect.stream(
        url=f"wss://{host}/media-stream",
        parameter1_name="numero_celular",
        parameter1_value=caller_number
    )

    response.append(connect)

    return HTMLResponse(content=str(response), media_type="application/xml")

@monolito.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):

    ejecucion=api_models.Ejecucion(persona=api_models.Persona(nombre="Mercedes",nombre_asistente="Elvita"))

    ejecucion.vad_iterator=vad_detector.new_iterator(min_silence_duration_ms=700, speech_pad_ms=150)

    print("Client connected")

    await websocket.accept()

    conectado=await websocket.receive_json()
    info_call=await websocket.receive_json()

    print(info_call)

    ejecucion.stream_sid=info_call['start']['streamSid']

    while(True):
        
        chunk_json=await websocket.receive_json()

        ejecucion.iteracion_actual=int(chunk_json["sequenceNumber"])

        if(ejecucion.iteracion_actual<ejecucion.espacio_blanco): continue

        mulaw_chunk=base64.b64decode(chunk_json["media"]["payload"])

        ejecucion.buffer_audio.append(mulaw_chunk)

        ejecucion.pcm_buffer=np.concatenate([ejecucion.pcm_buffer, vad_detector.mulaw_to_float32(mulaw_chunk)])

        while len(ejecucion.pcm_buffer)>=vad_detector.WINDOW_SAMPLES:

            ventana=ejecucion.pcm_buffer[:vad_detector.WINDOW_SAMPLES]
            ejecucion.pcm_buffer=ejecucion.pcm_buffer[vad_detector.WINDOW_SAMPLES:]

            evento=ejecucion.vad_iterator(torch.from_numpy(ventana))

            if(evento and "start" in evento):
                ejecucion.habla_activa=True
                print("Hablando")

            if(evento and "end" in evento):
                ejecucion.habla_activa=False
                print("Silencio -> fin de turno")

                async for fragmento in wrappers.pipeline(ejecucion):

                    await websocket.send_json(
                        {
                            "event": "media",
                            "streamSid": ejecucion.stream_sid,
                            "media": {
                                "payload": base64.b64encode(fragmento).decode('utf-8')
                            }
                        }
                    )

                ejecucion.buffer_audio=[]
                ejecucion.vad_iterator.reset_states()

    return

@monolito.get("/")
def hola():
    return "Hola a todos"
