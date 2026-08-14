from collections import deque
from datetime import datetime, time, date
from typing import Literal
from fastapi import WebSocket, BackgroundTasks
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
import numpy as np

class Chat(BaseModel):
    persona: str
    ia: str|None=None

class Persona(BaseModel):

    chat: list[Chat]=[]
    nombre: str
    nombre_asistente: str

class Ejecucion(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    buffer_audio: list=[]
    pcm_buffer: np.ndarray = Field(default_factory=lambda: np.array([], dtype=np.float32))
    vad_iterator: object = None
    habla_activa: bool = False
    stream_sid: str=""
    persona: Persona
    espacio_blanco: float=0
    iteracion_actual: int=0

class Respuesta(BaseModel):

    respuesta: str