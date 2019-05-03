from PyInquirer import style_from_dict, Token, ValidationError

custom_style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    #Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D',
    Token.Question: '',
})

validate_nonempty = lambda val: True if len(val) > 0 else 'Value cannot be empty'

validate_password_length = lambda val: True if val.isdecimal() and int(val) >= 8 and int(val) <= 32 else 'Length must be between 8 and 32'
