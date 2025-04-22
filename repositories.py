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

def local_repository_structure(version_folder:str) -> set:
    
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
        
        f"{version_folder}\\Experts\\Advisors": ["BlueCityCapital"],
        f"{version_folder}\\Include\\Expert":["BlueCityCapital"],
        f"{version_folder}\\Scripts":["BlueCityCapital"],
        f"{version_folder}":["Files"]

    }

    return directory_structure