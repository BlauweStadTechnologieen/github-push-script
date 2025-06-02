import settings_mapper

def local_repositories() -> set:
    
    """
    Contains the list of the local repositories to cycle through.

    Notes
    -----
    This is to be deprecated when we migrate to MT5.
    """
    repositories = {"Scripts", "Experts", "Include", "Images", "Files"}

    return repositories

def remote_repositories() -> set:
    """
    Used to make an API call to GitHub in order to retreieve the latest commits to each remote repo.
    
    Returns:
        set: `remote_repositories`
    """
    remote_repositories = {"MQL5Experts", "MQL5Include", "Screenshots", "MQL5Scripts"}

    return remote_repositories

def repository_list_test() -> set:
    """Not to be used in production"""
    repositories = {"version-management-system", "client_api"}

    return repositories

def local_repository_structure() -> set:
    
    """
    Cycles through all local repositoroes after checking:
    - that all directories are valid,
    - each local directory is a valid local repository.
    
    Returns:
        directory_structure(set) : Returns a `set` of directories. 

    Notes:
    -
        All errors or exceptions are handler by the calling function.

    """
    directory_structure = {
        
        f"{settings_mapper.DIRECTORY_CONSTANTS["VERSION_FOLDER"]}\\Experts\\Advisors": ["BlueCityCapital"],
        f"{settings_mapper.DIRECTORY_CONSTANTS["VERSION_FOLDER"]}\\Include\\Expert":["BlueCityCapital"],
        f"{settings_mapper.DIRECTORY_CONSTANTS["VERSION_FOLDER"]}\\Scripts":["BlueCityCapital"],
        f"{settings_mapper.DIRECTORY_CONSTANTS["VERSION_FOLDER"]}":["Files"]

    }

    return directory_structure

def tester_directory() -> set:
    """
    Provides a mock directory structure for testing purposes.

    Returns:
        set: A dictionary where keys are base folder paths and values are lists of subdirectories or files.
    """
    directory_list = {

        "nbc\\friends": ["Ross", "Rachel", "Chandler", "Monica", "Joey", "Phoebe"],
        "paramount\\fraiser": ["Fraiser", "Daphanie", "Martin", "Niles", "Roz"],
        "nbc\\will&grace": ["Will", "Grace", "Jack", "Karen"],
        "channel4\\coupling": ["Steve", "Susan", "Jeff", "Sally", "Patrick"],
        "channel4\\peep-show": ["Mark", "Jeremy", "SuperHans", "Dobby"],
        "channel4\\black-mirror": ["Charlie", "Brooker", "Annabel", "Jones"],

    }

    return directory_list

local = tester_directory()

import os

for base_folder, local_dirs in local.items():

    for local_dir in local_dirs:

        cwd = os.path.join(base_folder,local_dir)

        #print(cwd)