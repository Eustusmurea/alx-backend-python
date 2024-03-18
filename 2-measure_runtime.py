#!/usr/bin/env python3

import asyncio
import random
import time

async def wait_n(n: int, max_delay: int) -> list:
    delays = []
    tasks = [wait_random(max_delay) for _ in range(n)]
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays

async def measure_time(n: int, max_delay: int) -> float:
    start = time.time()
    await wait_n(n, max_delay)
    end = time.time()
    total_time = end - start/n
    return total_time
