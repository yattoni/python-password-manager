from model.account import Account

class Session(object):

    def __init__(self, username, auth_hash, key, vault=[]):
        self.username = username
        self.auth_hash = auth_hash
        self.key = key
        self.vault = vault

    def get_account(self, name):
        return next((a for a in self.vault if a.name == name), None)

    def account_exists(self, name):
        return name in self.get_account_names()

    def get_account_names(self):
        return sorted([a.name for a in self.vault])

    def display_account(self, name):
        self.get_account(name).display()

    def delete_account(self, name):
        self.vault.remove(self.get_account(name))

    def vault_to_dict(self):
        return [a.__dict__ for a in self.vault]

    def dict_to_vault(self, dct):
        for acc in dct:
            self.vault.append(Account(acc['name'], acc['username'], acc['password']))
