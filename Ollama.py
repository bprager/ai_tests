#!/usr/bin/env python
"""Test the OpenAI GPT-3 API on the local server"""
import asyncio
import logging
import time
from typing import Dict, Optional
from venv import logger

import aiohttp
import typer
from aiohttp.client_exceptions import ClientConnectorError
from rich.prompt import Prompt

# Local configuration
HOST_PORT = "fulla:11434"
CHAT_URL = f"http://{HOST_PORT}/v1/chat/completions"
MODELS_URL = f"http://{HOST_PORT}/api/tags"
TIMEOUT = 60
# Models preference list
MODELS = [
    "dolphin-mixtral:latest",
    "dolphin-phi:latest",
    "mistral:latest"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s - %(funcName)s:%(lineno)d: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def post_async(url: str, data: Dict) -> Optional[Dict]:
    """Asynchronously POST data to the specified URL and return the JSON response."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data, timeout=TIMEOUT) as resp:
                resp.raise_for_status()
                return await resp.json()
        except asyncio.TimeoutError:
            logging.error("Request exceeded timeout of %d seconds.", TIMEOUT)
            return None
        except ClientConnectorError as e:
            logging.error("Can't reach service: %s", e)
            return None

async def fetch_models_async(url: str) -> list[str]:
    """Asynchronously fetch the list of available models."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=TIMEOUT) as resp:
                resp.raise_for_status()
                json_data = await resp.json()
                return [model['name'] for model in json_data['models']]
        except asyncio.TimeoutError:
            logging.error("Request exceeded timeout of %d seconds.", TIMEOUT)
            return []
        except ClientConnectorError as e:
            logging.error("Can't reach service: %s", e)
            return []

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
    available_models: list[str] = await fetch_models_async(MODELS_URL)
    logging.debug("available_models: %s", available_models)
    model_used = next((m for m in MODELS if m in available_models), None)
    if model_used:
        data["model"] = f"{model_used}"
        logging.debug("Using model: %s", model_used)
    else:
        logging.error("No available models found.")
        return
    response = await post_async(CHAT_URL, data)
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
