def local_repositories() -> set:
    
    """
    Cycles through all local repositories and pushes each local repo to their respective, pre-configured, remote repository.

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
    remote_repositories = {"Experts", "Include", "Screenshots", "Scripts"}

    return remote_repositories

def repository_list_test() -> set:
    """Not to be used in production"""
    repositories = {"version-management-system", "client_api"}

    return repositories

def local_repository_structure() -> set:
    
    """
    Cycles through all local repositoroes after checking:
    - that all directories are calid,
    - each directory is a git repoo by the presence of a `.git` folder.
    
    Returns:
        directory_structure(set) : Returns a `set` of directories. 

    Notes:
    -
        All errore are handled by the calling function.

    """
    directory_structure = {
        
        "Experts\\Advisors": ["bluecitycapitaltechnologies"],
        "Include\\Expert":["Signal", "PriceStats", "Money"],
        "Scripts":["CreateLicence", "Non-existent-directorys"]

    }

    return directory_structure