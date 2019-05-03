from PyInquirer import prompt

from lib.api import login, signup
from lib.common import custom_style, validate_nonempty
from cli_flows.create_flow import run_create_flow
from cli_flows.read_flow import run_read_flow
from cli_flows.edit_flow import run_edit_flow
from cli_flows.delete_flow import run_delete_flow


def run_login_flow():
    """
    Command line interface questions for logging in or signing up.
    Asks whether to login or signup and then credentials.
    Attempts to login or signup.
    """
    questions = [
        {
            'type': 'list',
            'name': 'login_choice',
            'message': 'Welcome to Password Mangaer!',
            'choices': [
                'Login',
                'Sign up',
            ]
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter username:',
            'validate': validate_nonempty,
            'filter': lambda val: val.lower(),
        },
        {
            'type': 'password',
            'name': 'master_password',
            'message': 'Enter master password:',
            'validate': validate_nonempty,
        },
        {
            'type': 'password',
            'name': 'master_password_confirm',
            'message': 'Confirm master password:',
            'when': lambda answers: answers['login_choice'] == 'Sign up',
            'default': '',
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    session = None
    if answers['login_choice'] == 'Login':
        session = login(answers['username'], answers['master_password'])
    elif answers['login_choice'] == 'Sign up':
        if answers['master_password'] == answers['master_password_confirm']:
            session = signup(answers['username'], answers['master_password'])
        else:
            print('Passwords did not match. Exiting...')
            exit()


    print('Welcome ' + session.username + '!')
    return session


def run_main_flow(session):
    """
    Command line interface questions for what user wants to do now that they are logged in.
    """
    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'What do you want to do? Ctrl+C to exit.',
            'choices': [
                {
                    'name': 'Create a new account',
                    'value': run_create_flow,
                },
                {
                    'name': 'View an account',
                    'value': run_read_flow,
                },
                {
                    'name': 'Edit an account',
                    'value': run_edit_flow,
                },
                {
                    'name': 'Delete an account',
                    'value': run_delete_flow,
                },
            ]
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    answers['theme'](session)


def main():
    """
    Run login flow and then continuously run the main flow until user exits.
    """
    session = run_login_flow()
    while True:
        run_main_flow(session)


if __name__ == "__main__":
    main()
