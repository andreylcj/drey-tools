""" 
This module was created to manage files and directories
of system.

"""

import os
from typing import List
import tools.utils as Utils
import json


def get_files_path(
    parent_path: str, 
    content_arr: List[str]=[],
    ignore_files: List[str]=[],
    ignore_folders: List[str]=[],
    ignore_if_contain_some_of_the_words: List[str]=[]
) -> List:
    """Return array containing all abs path of files inside directory.

    Parameters
    ----------
    parent_path : str
        Directory to search files.
    content_arr : List[str], optional
        Array of content of parent path directory, by default []
    ignore_files : List[str], optional
        Ignore files if name equal some of this list, by default []
    ignore_folders : List[str], optional
        Ignore folders if name equal some of this list, by default []
    ignore_if_contain_some_of_the_words : List[str], optional
        Ignore folders and files if name cotain some of 
        the names presented on this list, by default []

    Returns
    -------
    List
        List of files path inside parent path directory.
    """
    filesPathArr = []
    ignore_cuz_content_name_have_some_of_the_words = False
    for contentName in content_arr:
        ignore_words_len = len(ignore_if_contain_some_of_the_words)
        for index1, word in enumerate(ignore_if_contain_some_of_the_words):
            if word in contentName:
                ignore_cuz_content_name_have_some_of_the_words = True
                break
            elif index1 == ignore_words_len - 1:
                ignore_cuz_content_name_have_some_of_the_words = False
        if len(contentName.split(".")) > 1:
            if contentName not in ignore_files \
            and not ignore_cuz_content_name_have_some_of_the_words:
                filesPathArr.append(
                    Utils.join_path(parent_path, contentName)
                )
        elif contentName not in ignore_folders \
        and not ignore_cuz_content_name_have_some_of_the_words:
            nextParentPath = Utils.join_path(parent_path, contentName)
            nextContentArr = os.listdir(nextParentPath)
            filesPathArr = filesPathArr \
                + get_files_path(
                    nextParentPath, 
                    nextContentArr, 
                    ignore_files, 
                    ignore_folders, 
                    ignore_if_contain_some_of_the_words
                )
    return filesPathArr


def list_path_of_all_files_inside_directory(
    root_directory_path: str,
    ignore_files: List[str]=[],
    ignore_folders: List[str]=[],
    ignore_if_contain_some_of_the_words: List[str]=[]
) -> List:
    """Return array containing all abs path inside some directory.

    Parameters
    ----------
    root_directory_path : str
        Directory abs path. Search for files inside this directory
    ignore_files : List[str], optional
        Ignore files if name equal some of this list, by default []
    ignore_folders : List[str], optional
        Ignore folders if name equal some of this list, by default []
    ignore_if_contain_some_of_the_words : List[str], optional
        Ignore folders and files if name cotain some of 
        the names presented on this list, by default []

    Returns
    -------
    List
        List of files path inside parent path directory.
    """
    try:
      dataDirectoryContent = os.listdir(root_directory_path)
    except:
      dataDirectoryContent = []
    itemsPath = []
    if len(dataDirectoryContent) > 0:
      itemsPath = get_files_path(
            root_directory_path, 
            dataDirectoryContent, 
            ignore_files, 
            ignore_folders, 
            ignore_if_contain_some_of_the_words
        )
    return itemsPath


def search_by_name_on_directory(
    name: str, 
    directory: str,
) -> List[str]:
    """Search files that contain substring on name inside directory

    Parameters
    ----------
    name : str
        Name of file that will be searched
    dir : str
        Directory to search for file

    Returns
    -------
    List[str]
        All file names that was found
    """
    content = os.listdir(directory)
    result = [filename for filename in content if name in filename]
    return result
    
    
def create_directories_of_path(
    path: str
) -> None:
    """Create all directories of path.

    Parameters
    ----------
    path : str
        Desired path.
        
    Returns
    -----
    None
        None is returned
    """
    
    split_path = None
    
    if Utils.gs() == "Windows": 
        split_path = path.split("\\")
    elif Utils.gs() == "Linux": 
        split_path = path.split("/")
    elif Utils.gs() == "Darwin": 
        split_path = path.split("\\")
        
    temp_path = None
    
    for index, env_path in enumerate(split_path):
        if not env_path: 
            continue
        if len(env_path.split(".")) > 1 and index == len(split_path) - 1: 
            break
        if temp_path == None: 
            if Utils.gs() == "Windows": 
                temp_path = env_path + '\\'
                continue
            elif Utils.gs() == "Linux": 
                temp_path = "/"
        temp_path = Utils.join_path(temp_path, env_path)
        if not os.path.exists(temp_path): 
            try:
                os.mkdir(temp_path)
            except Exception as e:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(e).__name__, e.args)
                print("Error: " + e)
                print(message)


def save_json(
    data: any, 
    path: str,
    indent: int=4,
    sort_keys: bool=False
) -> None:
    """Save JSON file.

    Parameters
    ----------
    data : any
        Json data
    path : str
        Destination path of file that will be saved
    indent : int, optional
        Indentation of JSON, by default 4
    sort_keys : bool, optional
        If keys of JSON will be sorted, by default False
    
    Returns
    ------
    None
        None is returned
        
    Raises
    ------
    Exception
        If path already exists.
    """
    
    if os.path.exists(path):
        raise Exception('Path already exists.')
    
    create_directories_of_path(path)
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent, sort_keys=sort_keys)
    