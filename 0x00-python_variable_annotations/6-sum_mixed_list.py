#!/usr/bin/env python3
from typing import List, Union
def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Sums a list of floats and returns the result.

    Args:
        mxd_lst (List[Union[int, float]]): A list of floats.

    Returns:
        float: The sum of the list of floats.
    """
    return sum(mxd_lst)
