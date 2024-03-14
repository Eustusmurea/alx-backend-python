#!/usr/bin/env python3

from typing import TypeVar, Dict, Any

KT= TypeVar('KT')
VT = TypeVar('VT')
from typing import Dict, Any, TypeVar

KT = TypeVar('KT')
VT = TypeVar('VT')

def safely_get_value(dct: Dict[KT, VT], key: KT, default: Any = None):
    """
    Safely retrieves the value associated with the given key from a dictionary.

    Args:
        dct (Dict[KT, VT]): The dictionary to retrieve the value from.
        key (KT): The key to look for in the dictionary.
        default (Any, optional): The default value to return if the key is not found. Defaults to None.

    Returns:
        VT: The value associated with the key if found, otherwise the default value.
    """
    if key in dct:
        return dct[key]
    else:
        return default
    