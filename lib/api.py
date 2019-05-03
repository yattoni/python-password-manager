import base64
import json
import requests

from lib.config import api_base_url
from lib.crypto import get_auth_hash, get_key, encrypt_vault, decrypt_vault
from model.account import Account
from model.session import Session


def login(username, master_password):
    print('Logging in...')
    url = api_base_url + '/login'

    auth_hash = get_auth_hash(username, master_password)
    body = {
        'username': username,
        'auth_hash': base64.b64encode(auth_hash).decode(),
    }

    response = requests.post(url, data=json.dumps(body))

    if response.status_code != requests.codes.ok:
        print('Login attempt failed with status code: ' + str(response.status_code))
        exit()

    response_body = response.json()
    cipher_text = base64.b64decode(response_body['vault'].encode())
    key = get_key(username, master_password)
    vault_str = decrypt_vault(cipher_text, key)
    vault_dict = json.loads(vault_str)

    session = Session(username, auth_hash, key)
    session.dict_to_vault(vault_dict)

    return session

def signup(username, master_password):
    print('Signing up...')
    url = api_base_url + '/signup'

    auth_hash = get_auth_hash(username, master_password)
    body = {
        'username': username,
        'auth_hash': base64.b64encode(auth_hash).decode(),
    }

    response = requests.post(url, data=json.dumps(body))

    if response.status_code != requests.codes.ok:
        print('Signup attempt failed with status code: ' + str(response.status_code))
        exit()

    key = get_key(username, master_password)
    vault = []
    session = Session(username, auth_hash, key, vault)
    update_vault(session)
    return session


def update_vault(session):
    print('Updating vault in cloud...')
    url = api_base_url + '/update'

    vault_dict = session.vault_to_dict()
    encrypted_vault = encrypt_vault(json.dumps(vault_dict), session.key)

    body = {
        'username': session.username,
        'auth_hash': base64.b64encode(session.auth_hash).decode(),
        'vault': base64.b64encode(encrypted_vault).decode(),
    }

    response = requests.post(url, data=json.dumps(body))

    if response.status_code != requests.codes.ok:
        print('Updating vault attempt failed with status code: ' + str(response.status_code))
        exit()
