#!/usr/bin/env python
"""Test the OpenAI GPT-3 API on the local server"""
import asyncio
from typing import Optional, Dict
from aiohttp import ClientSession
import typer
from rich.prompt import Prompt

# Local configuration
HOST_PORT = "192.168.1.124:1234"
URL = f"http://{HOST_PORT}/v1/chat/completions/"
TIMEOUT = 10


async def post_async(url: str, data: Dict) -> Optional[Dict]:
    """Asynchronously POST data to the specified URL and return the JSON response."""
    async with ClientSession() as session:
        try:
            async with session.post(url, json=data, timeout=TIMEOUT) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None


async def main_async(prompt: str):
    """Asynchronous main function to handle the API request."""
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.5,
        "max_tokens": -1,
        "stream": False,
    }
    response = await post_async(URL, data)
    if response:
        content = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        print(content)


def main():
    """Synchronous wrapper for the asynchronous main function."""
    user_prompt = Prompt.ask("[green]How can I be of assistance?[/green]")
    asyncio.run(main_async(user_prompt))


if __name__ == "__main__":
    typer.run(main)
