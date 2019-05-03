from PyInquirer import prompt

from cli_flows.gen_pwd_flow import run_generate_password_flow
from lib.api import update_vault
from lib.common import custom_style, validate_nonempty
from model.account import Account

def run_create_flow(session):
    """
    Command line interface questions for creating a new account.
    Asks details of account to create, adds account to vault locally and then updates vault in cloud.
    """
    questions = [
    {
            'type': 'input',
            'name': 'name',
            'message': 'What is the name of your new account?',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'What is the username for your new account?',
            'validate': validate_nonempty,
        },
        {
            'type': 'list',
            'name': 'password_method',
            'message': 'How would you like to create your password?',
            'choices': [
                'Input password myself',
                'Generate a password for me',
            ]
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'What is the password?',
            'when': lambda answers: answers.get('password_method', '') == 'Input password myself',
            'validate': validate_nonempty,
        },
        {
            'type': 'password',
            'name': 'confirm_password',
            'message': 'Please confirm your password:',
            'when': lambda answers: answers.get('password', False),
            'default': '',
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    if answers['password_method']  == 'Input password myself':
        if answers['password'] == answers['confirm_password']:
            print("Password confirmed.")
        else:
            print("Passwords do not match. Nothing will be created.")
            return
    elif answers['password_method']  == 'Generate a password for me':
        answers['password'] = run_generate_password_flow()

    if not session.account_exists(answers['name']):
        new_account = Account(answers['name'], answers['username'], answers['password'])
        session.vault.append(new_account)
        print('Account created.')
        update_vault(session)
    else:
        print('An account already exists with this name in the vault.')
        print('Nothing created.')
