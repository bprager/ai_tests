#!/usr/bin/env python
from openai import OpenAI

HOST_PORT = "fulla:11434"
base_url = f"http://{HOST_PORT}/v1/"  # point to the local server ! does not seem to be supported

client = OpenAI(
    api_key="ollama",
    base_url=base_url,
    timeout=60,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': 'Say this is a test',
        }
    ],
    model='mistral',
)

print(chat_completion)

