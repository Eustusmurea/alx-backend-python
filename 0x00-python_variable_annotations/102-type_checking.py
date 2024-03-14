#!/usr/bin/env python3

from typing import Tuple, Any

def zoom_array(lst: Tuple[Any, ...], factor: int = 2) -> Tuple[Any, ...]:
    """
    Zooms in on an array by repeating each element a certain number of times.

    Parameters:
        lst (Tuple[Any, ...]): The input tuple.
        factor (int): The factor by which each element will be repeated.

    Returns:
        Tuple[Any, ...]: The zoomed-in tuple.
    """
    zoomed_in = tuple(
        item for item in lst
        for _ in range(factor)
    )
    return zoomed_in

array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)  # Use an integer for the factor
