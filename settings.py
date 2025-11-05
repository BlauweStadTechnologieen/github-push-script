def repositories_to_bypass_commit_messages():
    
    repos_to_auto_generate_commit_messages = [
        
        "Screenshots",
        "Pycache",
        "eDocuments",

    ]

    return repos_to_auto_generate_commit_messages

if __name__ == "__main__":
    
    print(repositories_to_bypass_commit_messages())