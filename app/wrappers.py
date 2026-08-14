from app import aux_functions, api_models, ai_calls, emma
import time

async def pipeline(ejecucion:api_models.Ejecucion):

    audio_guardado=aux_functions.save_audio_from_chunks(ejecucion)

    st=time.time()

    st_transcript=time.time()
    texto=await ai_calls.transcript(audio_guardado)
    tiempo_transcript=time.time()-st_transcript

    print("Transcripcion ->",texto)

    ejecucion.persona.chat.append(api_models.Chat(persona=texto))

    st_ia=time.time()
    respuesta=await emma.conversa(ejecucion)
    tiempo_ia=time.time()-st_ia

    print("IA ->",respuesta)

    ejecucion.persona.chat[-1].ia=respuesta

    st_voz=time.time()
    fragmentos_enviados=[]

    async for fragmento in ai_calls.generar_voz(respuesta):
        fragmentos_enviados.append(fragmento)
        yield fragmento

    tiempo_voz=time.time()-st_voz

    tiempo_total=time.time()-st

    ejecucion.espacio_blanco=tiempo_total*1.1*50+aux_functions.get_audio_duration_ms(fragmentos_enviados)/20+ejecucion.iteracion_actual

    print(f"Tiempo transcripcion -> {tiempo_transcript:.3f}s")
    print(f"Tiempo IA -> {tiempo_ia:.3f}s")
    print(f"Tiempo voz -> {tiempo_voz:.3f}s")
    print(f"Tiempo total demorado -> {tiempo_total:.3f}s")