from PyInquirer import prompt

from lib.common import custom_style

def run_read_flow(session):
    """
    Command line interface questions for viewing an account.
    Asks which account to view and then prints attributes to console.
    """
    account_names = session.get_account_names()

    if len(account_names) == 0:
        print('No accounts.')
        return

    questions = [
        {
            'type': 'list',
            'name': 'selected_account',
            'message': 'Choose an account:',
            'choices': account_names,
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    session.display_account(answers['selected_account'])

def get_names_from_vault(vault):
    return list(vault.keys())