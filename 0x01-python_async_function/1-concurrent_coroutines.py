#!/usr/bin/env python3

import asyncio
import importlib

basic_async_syntax = importlib.import_module("0-basic_async_syntax")
from basic_async_syntax import wait_random  
async def wait_n(n: int, max_delay: int) -> list:
    delays = []
    tasks = [wait_random(max_delay) for _ in range(n)]
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays

# Example usage:
async def main():
    n = 5  # Number of times to spawn wait_random
    max_delay = 10  # Maximum delay
    delays = await wait_n(n, max_delay)
    print("Delays:", delays)

asyncio.run(main())
