""" 
This module was created to manage logs of executions
of any .py or .ipynb file

"""

import logging
from logging import Logger
import os
from types import FunctionType
from typing import Any, Union
import tools.utils as Utils
import tools.file_manager as FileManager
from functools import wraps
    

def default_start(
    root_path: str,
    namespace: str,
    filename: str,
    logger: Logger=logging
) -> None:
    """Logs default start of execution

    Parameters
    ----------
    root_path : str
        The root path of project
    namespace : str
        The namespace of file that is being executed
    filename : str
        The name of file
    logger : Logger, optional
        Already instanciated logger, by default logging
        
    Returns
    --------
    None
        None is returned
    """
    log_save_path = os.path.abspath(
        Utils.join_path(
            root_path, 
            'logs',
            namespace.replace(root_path, ''), 
            f'[{filename}].log'
        )
    )
    already_exists = None
    if os.path.exists(log_save_path):
        already_exists = True
    else:
        already_exists = False
    
    FileManager.create_directories_of_path(log_save_path)
        
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d : %(levelname)s : %(name)s : %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=log_save_path,
        level=logging.DEBUG
    )
    
    if already_exists:
        logger.info('')
    logger.info('!*************** START ***************!')
    

def function_name_start_and_end(
    func: FunctionType,
    logger: Logger=logging
) -> FunctionType:
    """Log name of function.
    
    Logs the name of function on start and end of execution.
    Logs error too.

    Parameters
    ----------
    func : FunctionType
        Function that will be executed
    logger : Logger, optional
        Specific logger, by default logging

    Returns
    -------
    FunctionType
        The wrapper function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Union[Any, None]:
        logger.debug(f'FunctionExecution : Start : {func.__name__}()')
        # logger.debug(f'FunctionExecution : Arguments : args={args}, kwargs={kwargs}')
        response = None
        try:
            response = func(*args, **kwargs)
        except Exception as exc:
            logger.error(exc)
        logger.debug(f'FunctionExecution : End : {func.__name__}')
        return response
    return wrapper
    
    