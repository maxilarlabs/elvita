from app import api_models, ai_wrappers
from app.prompts import elvita, dulce
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def conversa(ejecucion:api_models.Ejecucion):

    messages=[{"role": "user","content": dulce.usuario_prompt(ejecucion)}]

    for i in ejecucion.persona.chat:

        messages.append({"role": "user", "content": i.persona})
        if(i.ia!=None): messages.append({"role": "assistant", "content": i.ia})

    respuesta = await ai_wrappers.call_groq_llama(dulce.sistema_prompt(ejecucion),messages,temperatura=0.35)

    return respuesta


#Tu objetivo es preguntarle a Enzo cuando llega a Lima porque en base a eso Matias comprara el 'dulce'
#Si te preguntan que es dulce tu dices que es hierba buena o I wanna love you de Bob Marley.
#Consigue la fecha de su viaje.
#Tu unico objetivo es hablar conmigo.
#Mi nombre -> {api_state.persona.nombre}
#Nuestra conversacion -> {api_state.persona.chat}