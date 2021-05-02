import sqlite3
from bs4 import BeautifulSoup
import datetime
from enum import Enum

accounts_server = 'accounts.py'
accounts_db = 'accounts_data.db'
#accounts_db = '/var/jail/home/vittalt/FinalProject/accounts_data.db'

with sqlite3.connect(accounts_db) as c:
    c.execute('''CREATE TABLE IF NOT EXISTS accounts_db (username text, noise_pref integer);''')


class Noise(Enum):
    no_pref = 0
    quiet = 1
    moderate = 2
    loud = 3

    def str_form(type):
        if type == Noise.no_pref:
            return 'has no noise preference'
        elif type == Noise.quiet:
            return 'prefers quiet noise levels'
        elif type == Noise.moderate:
            return 'prefers moderate noise levels'
        elif type == Noise.loud:
            return 'prefers loud noise levels'
        else:
            return 'has an unknown preference'


class User:
    def __init__(self, name="anonymous", prefs = None):
        self.name = name
        if prefs is None:
            prefs = {'noise' : Noise.no_pref}
        self.prefs = prefs

    def __repr__(self):
        return f"User(\'{self.name}\', {{'noise' : {self.prefs['noise']}}})"

    def __str__(self):
        return f"{self.name} {Noise.str_form(self.prefs['noise'])}."

    def update_name(self, new_name):
        self.name = new_name

    def update_prefs(self, new_prefs):
        self.prefs = new_prefs

    def update_noise_pref(self, new_noise_pref):
        self.prefs['noise'] = new_noise_pref

    def get_name(self):
        return self.name

    def get_prefs(self):
        return self.prefs

    def get_noise_pref(self):
        return self.get_prefs()['noise']


def user_to_db(user):
    return user.get_name(), user.get_noise_pref().value

def db_to_user(db_entry):
    name, noise_pref_id = db_entry
    return User(name, {'noise' : Noise(noise_pref_id)})


def user_in_db(c, user):
    return username_in_db(c, user_to_db(user)[0])

def username_in_db(c, username):
    return c.execute('''SELECT EXISTS (SELECT 1 FROM accounts_db WHERE username = ?);''', (username,)).fetchone()[0]


def create_account(user):
    with sqlite3.connect(accounts_db) as c:
        if user_in_db(c, user):
            return f'Account {user.get_name()} already exists!'
        else:
            c.execute('''INSERT INTO accounts_db VALUES (?, ?);''', user_to_db(user))
            return f'Account {user.get_name()} created.'

def create_user_account(username, noise_pref):
    return create_account(db_to_user((username, noise_pref)))


def update_prefs(user):
    with sqlite3.connect(accounts_db) as c:
        if user_in_db(c, user):
            c.execute('''UPDATE accounts_db SET noise_pref = ? WHERE username = ?;''', user_to_db(user)[::-1])
            return f'Account {user.get_name()} updated.'
        else:
            return f'Account {user.get_name()} does not exist!'

def update_noise_pref(username, noise_pref):
    return update_prefs(db_to_user((username, noise_pref)))


def get_account(username):
    with sqlite3.connect(accounts_db) as c:
        if username_in_db(c, username):
            return db_to_user(c.execute('''SELECT * FROM accounts_db WHERE username = ?''', (username,)).fetchone())
        else:
            return f'Account {username} does not exist!'

def get_all_accounts():
    with sqlite3.connect(accounts_db) as c:
        return [db_to_user(db_entry) for db_entry in c.execute('''SELECT * FROM accounts_db''').fetchall()]


if __name__ == '__main__':
    me = User('Vittal', {'noise' : Noise.loud})
    print(repr(me))
    print(me)
    me.update_noise_pref(Noise.moderate)
    print(me)
    print()

    print(create_user_account('Ricardo', Noise.no_pref))
    print(get_account('Ricardo'))
    print(update_noise_pref('Ricardo', Noise.quiet))
    print(get_account('Ricardo'))
    print(get_all_accounts())
    print()

    print(create_account(me))
    print(create_account(me))
    print(get_account('Vittal'))
    print(update_noise_pref('Vittal', Noise.loud))
    print(get_account('Vittal'))
    print(get_account('RandomUnknown'))
    print(get_all_accounts())