#!/usr/bin/env python3

import asyncio
import random

import random
import asyncio

async def wait_random(max_delay: int = 10) -> float:
    """
    Asynchronously waits for a random amount of time.

    Args:
        max_delay (int): The maximum delay in seconds (default is 10).

    Returns:
        float: The actual delay time in seconds.
    """
    """
    Asynchronously waits for a random amount of time between 0 and the specified max_delay.

    Args:
        max_delay (int): The maximum delay in seconds (default is 10).

    Returns:
        float: The actual delay that was used.

    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay

async def main():
    result = await wait_random()
    print("Random delay:", result)

asyncio.run(main())
