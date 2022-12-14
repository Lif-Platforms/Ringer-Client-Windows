# -----------------------
# package info: this package is for logging into the server
# author: Superior126
#------------------------
import Packages.passwordHasher as passwordHasher

def login(username, password, client):
    while True:
        Message = client.recv(1024).decode('ascii')
        print(Message)
        
        if Message == 'LOGIN':
            client.send("LIF_LOGIN".encode('ascii'))
            print('lif login')

        if Message == 'USERNAME':
            client.send(username.encode('ascii'))

        if Message == 'PASSWORD':
            
            client.send(passwordHasher.get_initial_hash(password).encode('ascii')) 

        if Message == 'LOGIN_GOOD':
            return "Success"

        if Message == 'BAD_LOGIN_ERROR':
            return "Bad_Login"
            
        if Message == "BANNED!":
            return "Banned"