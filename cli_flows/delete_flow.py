from PyInquirer import prompt

from lib.api import update_vault
from lib.common import custom_style

def run_delete_flow(session):
    """
    Command line interface questions for deleting an account.
    Asks which account to delete, deletes from vault locally and then updates vault in cloud.
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

    session.delete_account(answers['selected_account'])

    print(answers['selected_account'] + ' deleted.')

    update_vault(session)
