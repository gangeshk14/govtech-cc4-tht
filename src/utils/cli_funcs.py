from rich.prompt import Confirm

def prompt_user_yes_no(message):
    """Prompt the user with a yes/no question and return True if they answer 'yes'."""
    return Confirm.ask(message)