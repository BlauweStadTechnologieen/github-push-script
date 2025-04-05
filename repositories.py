def local_repositories() -> set:
    """
    Cycles through all local repositories and push each local repo to their respective, pre-configured, remote repository.
    """
    repositories = {"Scripts", "Experts", "Include", "Images", "Files"}

    return repositories

def remote_repositories() -> set:
    """
    Used to make an API call to GitHub in order to retreieve the latest commits to each remote repo.
    """
    remote_repositories = {"Experts", "Include", "Screenshots", "Scripts"}

    return remote_repositories

def repository_list_test() -> set:
    """Not to be used in production"""
    repositories = {"version-management-system", "client_api"}

    return repositories

def local_repository_structure() -> set:
    
    directory_structure = {
        
        "Experts\\Advisors": ["bluecitycapitaltechnologies"],
        "Include\\Expert":["Signal", "PriceStats", "Money"],
        "Scripts":["CreateLicence", "Non-existent-directorys"]

    }

    return directory_structure