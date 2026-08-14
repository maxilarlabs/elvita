import audioop
import numpy as np
import torch
from silero_vad import load_silero_vad, VADIterator

SAMPLE_RATE = 8000
WINDOW_SAMPLES = 256  # fijo: el modelo exige exactamente 256 muestras a 8kHz

_model = load_silero_vad()

def new_iterator(threshold=0.5, min_silence_duration_ms=550, speech_pad_ms=150):

    return VADIterator(
        _model,
        threshold=threshold,
        sampling_rate=SAMPLE_RATE,
        min_silence_duration_ms=min_silence_duration_ms,
        speech_pad_ms=speech_pad_ms,
    )

def mulaw_to_float32(mulaw_chunk: bytes) -> np.ndarray:

    pcm16 = audioop.ulaw2lin(mulaw_chunk, 2)

    return np.frombuffer(pcm16, dtype=np.int16).astype(np.float32) / 32768.0
