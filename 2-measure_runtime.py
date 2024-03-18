#!/usr/bin/env python3

import asyncio
import time
from basic_async_syntax import wait_n

async def measure_time(n: int, max_delay: int) -> float:
    start_time = time.time()
    await wait_n(n, max_delay)
    end_time = time.time()
    total_time = end_time - start_time
    return total_time / n

# Example usage:
async def main():
    n = 5  # Number of times to spawn wait_random
    max_delay = 10  # Maximum delay
    average_time = await measure_time(n, max_delay)
    print("Average time per iteration:", average_time)

asyncio.run(main())
