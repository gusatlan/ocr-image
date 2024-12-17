from openai import OpenAI
from os_utils.osutils import get_parameter
from ollama import chat, ChatResponse, Client
import google.generativeai as genai
import re


AI_MODEL_ENV='ai_model'
AI_PROMPT_ENV='ai_prompt'
AI_HOST_ENV='ai_host'
AI_OPENAI_API_KEY_ENV='ai_openapi_api_key'
AI_GEMINI_API_KEY_ENV='ai_gemini_api_key'


def get_ai_model() -> str:
    return get_parameter(env_variable=AI_MODEL_ENV)


def get_ai_prompt() -> str:
    return get_parameter(env_variable=AI_PROMPT_ENV)


def get_ai_host() -> str:
    return get_parameter(env_variable=AI_HOST_ENV)


def get_api_key() -> str:
    return get_parameter(env_variable=AI_OPENAI_API_KEY_ENV)


def get_gemini_api_key() -> str:
    return get_parameter(env_variable=AI_GEMINI_API_KEY_ENV)


def chat_with_gpt(prompt:str, image:str=None, image_type:str=None, max_tokens:int=150, temperature:float=0.7):
    response = None
    client = OpenAI(api_key=get_api_key())

    try:
        messages = [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt}
                ]

            }
        ]

        if image and image_type:
            content_image = {
                'type': 'image_url',
                'image_url': {
                    'url': f'data:{image_type};base64,{image}'
                }
            }

            messages[0]['content'].append(content_image)


        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # "gpt-4o"
            messages=messages,
        #max_tokens=max_tokens,  # Limite de tokens na resposta
        #temperature=temperature,  # Controle da criatividade
        )
    except Exception as e:
        response=None

    return response


def chat_with_ollama(prompt:str, images:list, host:str, model:str='llama3.2:latest'):
    client = Client(host=host)

    messages = [
        {
            'role': 'user',
            'content': prompt
        }
    ]

    if images:
        im = {'images': images}
        messages[0].update(im)

    response: ChatResponse = client.chat(
        model=model,
        messages=messages
    )

    return response.message.content


def chat_with_gemini(prompt:str, image:dict, host:str='', model:str='gemini-2.0-flash-exp'):
    genai.configure(api_key=get_gemini_api_key())
    model = genai.GenerativeModel(model_name = model)

    response = model.generate_content(
        contents=[image, prompt]
    )

    return response.text


def extract_value(text: str) -> float:
    pattern = r"[-+]?\d*\.\d+|\d+"
    return float(re.search(pattern=pattern, string=text).group())
