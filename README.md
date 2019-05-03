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

### Things I Learned
I learned its not just important that your data is encrypted but how it is encrypted.
The hashes used to generate the key for encryption and authentication key are one way meaning they can't be looked up or reversed to find the original value.
Salt needs to be added to hashes to make them stronger and allow the same original text to be hashed to something different.
Without salt, if a hash is leaked and the password for it is figured out, this hash can be compared with the unsalted hash to see if we know its password.
Privacy is also a concern with these password managers as well as security.
Since it uses client side encryption and decryption, what is stored on the server can't be read if it is leaked.
Since the master password is not sent to login to the service, if what is sent gets leaked, the vault can still not be decrypted.
Password generators can generate crypro random passwords that can be strenghened by adding numbers and symbols, increasing the domain for which to use for a brute force attack.
Since these passwords are so random, a password manager is a good way to keep track of them all, and only need to remember one master password.
All of these work together to make cloud based password managers secure.
