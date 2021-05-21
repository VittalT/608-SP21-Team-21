import sys, os

os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Accounts')
sys.path.append(server_path + '/Rooms')

from accounts import *
from rooms import *

database = '../database.db'

import random
import string
POSS_TOKEN_CHARS = string.ascii_letters + string.digits

MIN_TOKEN_LEN = 50
MAX_TOKEN_LEN = 100
def generateToken():
    """
    Generates a random token of length 50 - 100, consisting of letters and numbers.
    """
    token_length = random.randint(MIN_TOKEN_LEN, MAX_TOKEN_LEN)
    token = ''.join(random.choice(POSS_TOKEN_CHARS) for _ in range(token_length))
    return token

def correct_password(name, password):
    """
    Checks if the given password matches the stored password in the database for the given user name.
    """
    if not User.created(name):
        return False
    user = User.get_user(name)
    return user.info['password'] == password

def correct_token(name, token):
    """
    Checks if the given token matches the stored token in the database for the given user name.
    """
    if not User.created(name):
        return False
    user = User.get_user(name)
    return user.info['token'] == token