#!/usr/bin/env python
"""Test the OpenAI GPT-3 API on the local server"""
import asyncio
import logging
import time
from typing import Dict, Optional
from venv import logger

import typer
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from rich.prompt import Prompt

# Local configuration
HOST_PORT = "fulla:1234"
URL = f"http://{HOST_PORT}/v1/chat/completions/"
TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s - %(funcName)s:%(lineno)d: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def post_async(url: str, data: Dict) -> Optional[Dict]:
    """Asynchronously POST data to the specified URL and return the JSON response."""
    async with ClientSession() as session:
        try:
            async with session.post(url, json=data, timeout=TIMEOUT) as response:
                response.raise_for_status()
                return await response.json()
        except (
            asyncio.TimeoutError,
            ClientConnectorError,
        ) as e:
            logging.error("Server down?: %s", e)
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
    start_time = time.time()
    user_prompt = Prompt.ask("[green]How can I be of assistance?[/green]")
    asyncio.run(main_async(user_prompt))
    logger.info("--- Elapsed time: %.2f seconds ---", time.time() - start_time)


if __name__ == "__main__":
    typer.run(main)
