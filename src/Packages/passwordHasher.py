import hashlib

def get_initial_hash(password):
    salt = "5gz"
  
    # Adding salt at the last of the password
    dataBase_password = password+salt
    # Encoding the password
    hashed = hashlib.md5(dataBase_password.encode())
  
    return hashed.hexdigest()