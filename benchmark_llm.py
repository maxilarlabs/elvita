import asyncio
import os
import statistics
import time

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app import api_models, ai_wrappers
from app.prompts import dulce

load_dotenv()

OPENAI_KEY = os.environ.get("OPENAI_KEY")

openai_client = AsyncOpenAI(api_key=OPENAI_KEY)

N_ITERACIONES = 5

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
OPENAI_MODEL = "gpt-5.6-luna"
GROQ_MODEL = "llama-3.3-70b-versatile"


def construir_prompts():

    ejecucion = api_models.Ejecucion(
        persona=api_models.Persona(
            chat=[api_models.Chat(persona="Hola, ¿quién habla?")],
            nombre="Cris",
            nombre_asistente="Max",
        )
    )

    sistema = dulce.sistema_prompt(ejecucion)
    usuario = dulce.usuario_prompt(ejecucion)

    messages = [{"role": "user", "content": usuario}]

    for i in ejecucion.persona.chat:
        messages.append({"role": "user", "content": i.persona})
        if i.ia is not None:
            messages.append({"role": "assistant", "content": i.ia})

    return sistema, messages


async def call_openai_luna(sistema, messages):

    full_messages = [{"role": "system", "content": sistema}] + messages

    # gpt-5.6-luna solo soporta el temperature default (1), no se puede ajustar
    response = await openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=full_messages,
    )

    return response.choices[0].message.content


async def medir(nombre, funcion, n=N_ITERACIONES):

    tiempos = []
    ultima_respuesta = None

    await funcion()  # warmup, no se mide (conexion fria/cache)

    for i in range(n):

        st = time.perf_counter()
        ultima_respuesta = await funcion()
        tiempos.append(time.perf_counter() - st)

        print(f"  [{nombre}] intento {i+1}/{n} -> {tiempos[-1]:.3f}s")

    print(f"\n=== {nombre} ===")
    print(f"  min:    {min(tiempos):.3f}s")
    print(f"  max:    {max(tiempos):.3f}s")
    print(f"  media:  {statistics.mean(tiempos):.3f}s")
    print(f"  mediana:{statistics.median(tiempos):.3f}s")
    print(f"  ultima respuesta -> {ultima_respuesta!r}\n")

    return tiempos


async def main():

    sistema, messages = construir_prompts()

    tiempos_claude = await medir(
        "Claude Haiku 4.5",
        lambda: ai_wrappers.call_claude(sistema, messages, modelo=CLAUDE_MODEL, temperatura=0.35),
    )

    tiempos_openai = await medir(
        "GPT-5.6 Luna",
        lambda: call_openai_luna(sistema, messages),
    )

    tiempos_groq = await medir(
        "Groq Llama 3.3 70B",
        lambda: ai_wrappers.call_groq_llama(sistema, messages, modelo=GROQ_MODEL, temperatura=0.35),
    )

    print("=== Resumen ===")
    print(f"Claude Haiku 4.5   -> media {statistics.mean(tiempos_claude):.3f}s")
    print(f"GPT-5.6 Luna       -> media {statistics.mean(tiempos_openai):.3f}s")
    print(f"Groq Llama 3.3 70B -> media {statistics.mean(tiempos_groq):.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
