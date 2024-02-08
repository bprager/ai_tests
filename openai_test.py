#!/usr/bin/env python
import openai

host = "192.168.1.124"
api_base = f"http://{host}:1234/v1"  # point to the local server ! does not seem to be supported
api_key = ""  # no need for an API key

openai.api_key = api_key
openai.base_url = api_base

completion = openai.chat.completions.create(
    model="local-model",  # this field is currently unused
    messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "Introduce yourself."},
    ],
)

print(completion.choices[0].message)
