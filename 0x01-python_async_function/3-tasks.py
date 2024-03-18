#!/usr/bin/env python3

import asyncio
import random
import importlib

basic_async_syntax = importlib.import_module("0-basic_async_syntax")

def task_wait_random(max_delay: int) -> asyncio.Task:
    return asyncio.create_task(wait_random(max_delay))

# Example usage:
async def main():
    max_delay = 10  # Maximum delay
    task = task_wait_random(max_delay)
    await task
    print("Random delay:", task.result())

asyncio.run(main())
