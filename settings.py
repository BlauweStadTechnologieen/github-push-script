from error_handler import status_logger



def repositories_to_bypass_commit_messages():
    
    repos_to_auto_generate_commit_messages = [
        
        "Screenshots",

    ]

    return repos_to_auto_generate_commit_messages

if __name__ == "__main__":
    
    if "Screenshots" in repositories_to_bypass_commit_messages():
        status_logger("Package in repositors to bypass commit messages","The 'Screenshots' repository is set to bypass commit messages.")
    
    status_logger("Package not on list to bypass commit messages","The package is not set to bypass commit messages.")