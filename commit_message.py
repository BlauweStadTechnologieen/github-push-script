def commit_message_validation(package_name:str) -> str:
    """
    Prompts the user to enter a commit message and validates it according to specific rules.
    The commit message must:
        - Be longer than 10 characters.
        - Not be empty.
        - Not contain the substring "ghp" (to prevent accidental inclusion of sensitive tokens).
        - Not contain an email address.
    If the input fails any validation, an error message is displayed and the user is prompted again.
    Returns:
        str: A valid commit message entered by the user.
    """
    while True:

            try:

                commit_message = input(f"Please enter your commit message for {package_name}....")

                if not commit_message or len(commit_message) <= 10:

                    raise ValueError("Either the character length is too short, or you have not entered a commit message at all ")
                
                if "ghp" in commit_message:

                    raise ValueError("It looked like you are trying to include a commit message which includes a sensitive token. Don't do what, Silly Boy!")
                
                import re
                
                email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-zA-Z]{2,}\b"

                if re.search(email_pattern, commit_message):

                    raise ValueError("It looks like you are trying to enter an email address into the commit message. Don't do that, Silly Boy!")
            
                return commit_message

            except ValueError as e:

                print(f"Commit Message Formatting Error : {e}")