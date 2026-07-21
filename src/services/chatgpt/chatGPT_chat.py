import os
from openai import OpenAI
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN', '')
FUNCTION_DESCRIPTION = os.environ.get('FUNCTION_DESCRIPTION', '')
PERSONALITY = os.environ.get('PERSONALITY', '')

client = OpenAI(api_key=OPENAI_TOKEN)

MODELS = {
    'gtp-3.5': 'gpt-3.5-turbo',
}

def generate_response(function_description: str, personality: str, prompt: list, temperature: float = 0.6, max_tokens: int = 100) -> str:
    """
    Genera una respuesta utilizando la API de OpenAI y el modelo especificado.
    """
    # MODO MANTENIMIENTO: Desactivado temporalmente por falta de cuota en la API
    return None

    try:
        response = client.chat.completions.create(
            model=MODELS['gtp-3.5'],
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=1,
            presence_penalty=1,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Se produjo un error al llamar a la API de OpenAI: {e}")
        return "Lo siento, mi cerebro artificial no funciona ahora mismo."

def bot_response(prompt: str, temperature: float = 0.8, max_tokens: int = 100) -> str:
    function_description = FUNCTION_DESCRIPTION
    personality = PERSONALITY

    historial_mensajes = [
        {
            "role": "system",
            "content": f'{function_description} Tu personalidad es: {personality}'
        },
        {
            "role": "user", 
            "content": f'{prompt}'
        },
    ]

    message = generate_response(
        function_description=function_description,
        personality=personality,
        prompt=historial_mensajes,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return message
