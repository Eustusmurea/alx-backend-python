#!/usr/bin/env python3

from typing import Tuple, Any

def zoom_array(lst: Tuple[Any, ...], factor: int = 2) -> Tuple[Any, ...]:
    """
    Zooms in on the elements of the input list by repeating each element a certain number of times.

    Args:
        lst (Tuple[Any, ...]): The input list to be zoomed in on.
        factor (int, optional): The number of times each element should be repeated. Defaults to 2.

    Returns:
        Tuple[Any, ...]: The zoomed-in list, where each element is repeated `factor` times.
    """
    zoomed_in = tuple(item for item in lst for _ in range(factor))
    return zoomed_in

array = (12, 72, 91)  # Using a tuple instead of a list

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)  # Passing an integer instead of a float
