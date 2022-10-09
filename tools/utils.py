""" 
This module was created to define utils functions that can be used
in many situations.

"""

import os
import re
import platform
from types import FunctionType
from typing import List, Tuple, Union
from pandas.core.frame import DataFrame
import pandas as pd
import json


def is_float(
    my_str: str
) -> bool:
    """Verify if string is float format.

    Parameters
    ----------
    my_str : str
        Input string

    Returns
    -------
    bool
        True if string is float, else, False
    """
    
    resp = False
    try:
        float(my_str)
        resp = True
    except ValueError:
        resp = False
    return resp


def is_int(
    my_str: str
) -> bool:
    """Verify if string is int format.

    Parameters
    ----------
    my_str : str
        Input string

    Returns
    -------
    bool
        True if string is int, else, False
    """
    
    resp = False
    try:
        int(my_str)
        resp = True
    except ValueError:
        resp = False
    return resp


List1 = int
List2 = int
def list_difference(
    list1: List,
    list2: List,
    list_return_index: Union[List1, List2]=1
) -> List:
    """Get element which exists in 'list1' but not exist in 'list2' and
    get elements which exists in 'list1' but not exist in 'list2'.

    Parameters
    ----------
    list1 : List
        List one.
    list2 : List
        List two. 
    list_return_index : Union[List1, List2], optional
        Can be only 1 or 2. 
        If 1, return values that is only in list 1,
        if 2, return values that is only in list 2,
        by default 1

    Returns
    -------
    ListDifference
        Returns the elements which exists in 'list1' and not exists 
        in 'list2' and elements which exists in 'list1' and not exists 
        in 'list2'
    """
    
    d1 = list(set(list1) - set(list2))
    d2 = list(set(list2) - set(list1))
    
    list_difference_dict = {
        1: d1,
        2: d2,
    }
    
    return list_difference_dict[list_return_index]


And = str
Or = str
def pick_first_satisfy_conditions_else_get_last(
    *args, 
    conditions: List[FunctionType],
    conditions_type: Union[And, Or]='and',
) -> any:
    """Pick first value which satisfies conditions, else get last 
    value of args.

    Parameters
    ----------
    conditions : List[FunctionType]
        Conditions to verify the values, must return 
        boolean value (Union[True, False])
    conditions_type : Union[And, Or], optional
        Type of conditions will be applied, by default 'and'

    Returns
    -------
    any
        Return value which satisfies all conditions or last value of args

    Raises
    ------
    Exception
        If conditions_type is invalid
    """
    conditions_len = len(conditions)
    for value in args[:-1]:
        is_conditions_valid = []
        for index2, is_condition_satisfied in enumerate(conditions):
            is_conditions_valid.append(is_condition_satisfied(value))
            if conditions_type == 'and':
                if not is_conditions_valid[-1]:
                    continue
                elif index2 == conditions_len - 1 \
                and False not in is_conditions_valid:
                    return value
            elif conditions_type == 'or':
                if is_conditions_valid[-1]:
                    return value
            else:
                raise Exception('Variable "conditions_type" must be Union["and", "or"]')
    return args[-1]


def camel_to_snake(
    name: str
) -> str:
    """Transform camel case to snake case

    Parameters
    ----------
    name : str
        Camel case name

    Returns
    -------
    str
        Snake case name
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def to_title(
    text: str
) -> str:
    """Transforms text to title
    
    Title remains first letter in capslock and lower for the remaining. 
    Replaces '_' by ' '. If in camel case, add space.

    Parameters
    ----------
    text : str
        Text to be transformed in title

    Returns
    -------
    str
        Title text
    """
    text = camel_to_snake(text)
    text = text.replace('_', ' ')
    return text[0].upper() + text[1:]
    

def hightlight_header(
    title: str,
    break_line_after: int=1
) -> str:
    """Generate hightlight title to print in console

    Parameters
    ----------
    title : str
        Text on header
    break_line_after : int, optional
        Num of break lines to separe title from text, by default 1

    Returns
    -------
    str
        Hightlighted header
    """
    real_title = f'!*** {title} ***!'
    hightlight = f'!{"*" * (len(real_title) - 2)}!'
    return f'{hightlight}\n{real_title}\n{hightlight}' + ("\n" * break_line_after)


def json_pp_message(
    dict_data: dict, 
    sort_keys: bool=True, 
    indent: int=4
) -> str:
    """Get json in a pretty format

    Parameters
    ----------
    dict_data : dict
        Raw data
    sort_keys : bool, optional
        Sort keys of dict, by default True
    indent : int, optional
        Indent desired in message, by default 4

    Returns
    -------
    str
        Json message with pretty format
    """
    return json.dumps(dict_data, sort_keys = sort_keys, indent = indent)


def json_pp(
    dict_data: dict,
    sort_keys: bool=False,
    indent: int=4
) -> None:
    """Pretty print of json data

    Parameters
    ----------
    dict_data : dict
        Raw json data
    sort_keys : bool, optional
        Sort keys of json, by default True
    indent : int, optional
        Indentation of json message, by default 4
    """
    print(
        json_pp_message(
            dict_data=dict_data,
            sort_keys=sort_keys,
            indent=indent,
        )
    )
    
    
def gs() -> str:
    """Get operational system

    Returns
    -------
    str
        Name of operational system
    """
    return platform.system()
    
    
def join_path(
    *args: Tuple[str],
) -> str:
    """Join multiple paths.
    
    Consider special cases, like when one of the paths
    starts with '/'.

    Returns
    -------
    str
        Joined path.
    """
    path = None
    for index, arg in enumerate(args):
        if index != 0 and arg and arg[0] == "/":
            arg = arg[1:]
        if index == 0: 
            path = os.path.abspath(os.path.join(arg))
        else: 
            path = os.path.abspath(os.path.join(path, arg))
    return path
