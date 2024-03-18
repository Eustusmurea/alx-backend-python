#!/usr/bin/env python3

import asyncio
import random
from basic_async_syntax import wait_random

def task_wait_random(max_delay: int) -> asyncio.Task:
    return asyncio.create_task(wait_random(max_delay))

# Example usage:
async def main():
    max_delay = 10  # Maximum delay
    task = task_wait_random(max_delay)
    await task
    print("Random delay:", task.result())

asyncio.run(main())
