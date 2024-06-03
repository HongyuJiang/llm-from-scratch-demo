import os
import configparser
import requests
from openai import OpenAI

LLM_API_KEY = os.environ.get('LLM_API_KEY')
if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY environment variable is not set.")

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../', 'config.ini'))
plat_url = config['LLM']['plat_url']
general_model = config['LLM']['general_model']
code_model = config['LLM']['code_model']

client = OpenAI(
    base_url=plat_url,
    api_key=LLM_API_KEY
)


def chat(query, stream=False, history=[], max_length=168, temperature=0, senarios=None):
    model = general_model
    if senarios == 'code':
        model = code_model

    params = dict(model=model, messages=[{"role": "user", "content": query}] + history, stream=stream)
    params["max_tokens"] = max_length
    params["temperature"] = temperature
    params["stream"] = False

    response = client.chat.completions.create(**params)

    reply = response.choices[0].message.content
    return reply
