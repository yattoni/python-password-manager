from PyInquirer import prompt

from cli_flows.gen_pwd_flow import run_generate_password_flow
from lib.api import update_vault
from lib.common import custom_style, validate_nonempty

def run_edit_flow(session):
    """
    Command line interface questions for editing an account.
    Asks what attributes to edit, edits accoutn in vault locally and then updates vault in cloud.
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
        {
            'type': 'list',
            'name': 'edit_choice',
            'message': 'What would you like to change?',
            'choices': [
                'Account name',
                'Username',
                'Password',
            ]
        },
        {
            'type': 'input',
            'name': 'name',
            'message': 'Enter a new account name:',
            'when': lambda answers: answers['edit_choice'] == 'Account name',
            'validate': validate_nonempty,
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter a new username:',
            'when': lambda answers: answers['edit_choice'] == 'Username',
            'validate': validate_nonempty,
        },
        {
            'type': 'list',
            'name': 'password_method',
            'message': 'How would you like to create your password?',
            'when': lambda answers: answers['edit_choice'] == 'Password',
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

    account = session.get_account(answers['selected_account'])

    if answers['edit_choice'] == 'Account name':
        account.name = answers['name']
    elif answers['edit_choice'] == 'Username':
        account.username = answers['username']
    elif answers['edit_choice'] == 'Password':
        if answers['password_method'] == 'Input password myself':
            if answers['password'] == answers['confirm_password']:
                account.password = answers['password']
            else:
                print('Passwords do not match. Nothing updated.')
                return
        else:
            answers['password'] = run_generate_password_flow()
            account.password = answers['password']

    update_vault(session)
