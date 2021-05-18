import sys, os
# sys.path.append(os.path.abspath(__file__))
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
    token = ''
    token_length = random.randint(MIN_TOKEN_LEN, MAX_TOKEN_LEN)
    for i in range(token_length):
        index = random.choice(POSS_TOKEN_CHARS)
        token += chr(index)
    return token

def correct_password(name, password):
    if not User.created(name):
        return False
    user = User.get_user(name)
    return user.info['password'] == password

def correct_token(name, token = None):
    if not User.created(name):
        return False
    user = User.get_user(name)
    return user.info['token'] == token