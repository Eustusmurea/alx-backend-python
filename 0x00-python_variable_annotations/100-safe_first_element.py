#!/usr/bin/env python3

from typing import List, Union, Any

def safe_first_elements(lst: List[Any]) -> Union[Any, None]:
    """
    Returns the first element of a list if it exists, otherwise returns None.

    Args:
        lst (List[Any]): The list from which to retrieve the first element.

    Returns:
        Union[Any, None]: The first element of the list if it exists, otherwise None.
    """
    if lst:
        return lst[0]
    else:
        return None
def safe_first_elements(lst: List[any]) -> Union[Any, None]:
    if lst:
        return lst[0]
    
    else:
        return None
