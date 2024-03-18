#!/usr/bin/env python3

import asyncio
import random

async def task_wait_random(max_delay: int = 10) -> float:
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay

async def task_wait_n(n: int, max_delay: int) -> list:
    delays = []
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays

async def main():
    n = 5  # Number of times to spawn task_wait_random
    max_delay = 10  # Maximum delay
    delays = await task_wait_n(n, max_delay)
    print("Delays:", delays)

asyncio.run(main())