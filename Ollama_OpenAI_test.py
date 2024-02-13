#!/usr/bin/env python
from openai import OpenAI

HOST = "192.168.1.114"
base_url = f"http://{HOST}:11434"  # point to the local server ! does not seem to be supported
KEY = ""  # no need for an API key

client = OpenAI(
    api_key=KEY,
    base_url=base_url,
    timeout=60,
)

completion = client.chat.completions.create(
    model="dolphin-mixtral",  # this field is currently unused
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Introduce yourself."},
    ],
)

print(completion.choices[0].message)
