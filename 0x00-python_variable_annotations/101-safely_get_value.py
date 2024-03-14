#!/usr/bin/env python3

from typing import Mapping, Any, Union, TypeVar

# Define a TypeVar for the return type to allow flexible typing
T = TypeVar('T')

def safely_get_value(dct: Mapping, key: Any, default: Union[T, None] = None) -> Union[Any, T]:
    """
    Safely gets a value from a dictionary.

    Parameters:
        dct (Mapping): The input dictionary.
        key (Any): The key to lookup in the dictionary.
        default (Optional[Union[T, None]]): The default value to return if the key is not found.

    Returns:
        Union[Any, T]: The value corresponding to the key if it exists, otherwise the default value.
    """
    if key in dct:
        return dct[key]
    else:
        return default
    