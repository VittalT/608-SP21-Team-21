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

def generateToken():
    token = ''
    token_length = random.randint(50, 100)
    for i in range(token_length):
        index = random.randint(33, 126)
        token += chr(index)
    return token

def correct_password(name, password):
    if not User.created(name):
        return False
    user = User.get_user(name)
    return user['password'] == password

def correct_token(name, token):
    if not User.created(name):
        return False
    user = User.get_user(name)
    return user['token'] == token