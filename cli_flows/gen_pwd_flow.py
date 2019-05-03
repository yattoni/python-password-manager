from PyInquirer import prompt

from lib.common import custom_style, validate_password_length
from lib.crypto import generate_password

def run_generate_password_flow():
    """
    Command line interface questions for using password generator.
    Asks questions about options for password generator then calls password generator.
    """
    questions = [
        {
            'type': 'input',
            'name': 'new_password_length',
            'message': 'Specify length for generated password:',
            'validate': validate_password_length,
            'default': '16',
            'filter': lambda val: int(val),
        },
        {
            'type': 'checkbox',
            'name': 'generator_options',
            'message': 'Select options for generator: (all are selected by default)',
            'choices': [
                {
                    'name': 'Uppercase',
                    'checked': True,
                },
                {
                    'name': 'Numbers',
                    'checked': True,
                },
                {
                    'name': 'Symbols',
                    'checked': True,
                },
            ]
        },
    ]

    answers = prompt(questions, style=custom_style)

    if len(answers) == 0:
        exit()

    password_confirmed = False
    new_password = ''
    while not password_confirmed:
        new_password = generate_password(int(answers['new_password_length']), answers['generator_options'])
        print('Generated password is: ' + new_password)

        confirm_question = [
            {
                'type': 'confirm',
                'name': 'isConfirmed',
                'message': 'Is this password ok?',
            }
        ]

        confirmed_answer = prompt(confirm_question, style=custom_style)

        if len(confirmed_answer) == 0:
            exit()

        password_confirmed = confirmed_answer['isConfirmed']
    return new_password
