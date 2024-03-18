#!/usr/bin/env python3

import asyncio
import random

async def wait_random(max_delay: int = 10) -> float:
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay

async def wait_n(n: int, max_delay: int) -> list:
    delays = []
    tasks = [wait_random(max_delay) for _ in range(n)]
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays

async def main():
    n = 5  # Number of times to spawn wait_random
    max_delay = 10  # Maximum delay
    delays = await wait_n(n, max_delay)
    print("Delays:", delays)

asyncio.run(main())