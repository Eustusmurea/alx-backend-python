#!/usr/bin/env python3
from typing import List, Tuple, Union
def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Takes a string k and an int or float v as arguments,
    and returns a tuple with the string k and the square of v as a float.
    """
    return k, v ** 2.0
