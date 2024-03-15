#!/usr/bin/env python
from openai import OpenAI

client = OpenAI(
    base_url='http://fulla:11434/v1/',

    # required but ignored
    api_key='',
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
