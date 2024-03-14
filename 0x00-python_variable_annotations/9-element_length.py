#!/usr/bin/env python3
from typing import List, Tuple

def element_length(lst: List[str]) -> List[Tuple[str, int]]: 
    """
    Calculate the length of each element in the given list.

    Args:
        lst (List[str]): The list of strings.

    Returns:
        List[Tuple[str, int]]: A list of tuples where each tuple contains a string from the input list and its corresponding length.

    """
    return[(i, len(i)) for i in lst]
