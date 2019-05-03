# python-password-manager
Password manager using PyInquirer for a CLI and AWS Lambda for backend.

Youtube Video Demo : https://youtu.be/kAvsGmNqUAU 

## Installation
```bash
python3 -m pip install PyInquirer pycrypto
```

## Usage
```bash
python3 main.py
```
This will greet you with the options to login or signup.
Following that it will invoke an AWS Lambda function to pull the password encrypted vault saved in AWS DynamoDB.
You can then create, view, edit, and delete the accounts and passwords saved in the vault.
Any changes made to the vault will be uploaded back to DynamoDB after they are made locally.
Press Ctrl+C anytime to exit the password manager.

## Security Details
The password vault is encrypted and decrypted locally using AES-256.
The key is created using 100,000 rounds of PBKDF2-SHA256.
This key never leaves your computer.
To authenticate requests with the backend AWS Lambda functions, the key is hashed for one more round before sent to the server.
The server then applies a salt generated when the account was created before hashing it again to compare with the hash stored in DynamoDB to authenticate you.
Finally, the encrypted vault is sent back to your computer.
These requests are sent using over HTTPS using TLS to prevent man in the middle attacks.

A password generator is also included when creating new or editing existing passwords for accounts.
