class Account(object):
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def display(self):
        print('Name: ' + self.name)
        print('Username: ' + self.username)
        print('Password: ' + self.password)
