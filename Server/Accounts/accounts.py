import sys, os
# sys.path.append(os.path.abspath(__file__))
os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Preferences')

import sqlite3
from noise import *

database = '../database.db'


class User:
    def __init__(self, name="anonymous", info=None):
        """
        Constructor for User object. Will create a new binding between
        a name and a User object in users table
        """
        assert ';' not in name, "Usernames cannot include ';'"
        self.name = name
        self.info = info

    def __repr__(self):
        return f"User(\'{self.name}\', {self.info})"

    def __str__(self):
        return f"{self.name} {Noise.str_form(self.info['volumePref'])}."

    @property
    def name(self):
        """
        Getter function for preferences attribute
        """
        if self._name is None:
            return ""
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter function for preferences attribute. Raises
        a TypeError if input is not a string
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

    @property
    def info(self):
        """
        Getter function for info attribute
        """
        if self._info is None:
            self._info = {'password': '', 'token': '', 'volumePref': Noise.no_pref}
        return self._info

    def get_volume_pref(self):
        return self.info['volumePref']

    @info.setter
    def info(self, value):
        """
        Setter function for preferences attribute. Raises
        a TypeError if input is not a string
        """
        if value is None:
            value = {'password': '', 'token': '', 'volumePref': Noise.no_pref}

        if not (isinstance(value, dict) and isinstance(value['volumePref'], Noise)
                and isinstance(value['password'], str) and isinstance(value['token'], str)):
            raise TypeError("Info has invalid password, token, or volumePref")
        self._preferences = value

    def upload(self):
        """
        Uploads a user to the users table. Raises
        an AssertionError if name is taken
        """
        sqlite3.register_adapter(User, User.adapt_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            if not User.created(self.name):
                c.execute('''INSERT INTO users VALUES (?, ?);''', (self.name, self))
                return f'Account {self.name} created.'
            else:
                raise AssertionError(f"The name '{self.name}' is already taken")

    def adapt_user(self):
        """
        Gets a string representation of a User object to store in
        SQL table. ONLY INTENDED FOR USE IN users TABLE
        """
        return f"{self.name};{self.info['password']};{self.info['token']};{self.info['volumePref'].value}"

    def __conform__(self, protocol):
        """
        Standard way to store a User in a table by storing
        only their name
        """
        if protocol is sqlite3.PrepareProtocol:
            return self.name

    def convert_user(self):
        """
        Converts a bytes response from an SQL table into
        a User object
        """
        name, password, token, volumePref = map(lambda x: x.decode("utf-8"), self.split(b";"))
        return User(name, {'password': password, 'token': token, 'volumePref': Noise(int(volumePref))})

    @staticmethod
    def created(name):
        with sqlite3.connect(database) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            return c.execute('''SELECT EXISTS (SELECT 1 FROM users WHERE name = ?);''', (name,)).fetchone()[0]

    @staticmethod
    def validate(name):
        """
        Returns True if a user is in the database, raises
        KeyError otherwise
        """
        with sqlite3.connect(database) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            if not User.created(name):
                raise KeyError(f"{name} is not a valid user")
            return True

    @staticmethod
    def get_user(name):
        """
        Gets the user associated with the given name. Raises
        a KeyError if the user does not exist
        """
        sqlite3.register_converter("user", User.convert_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            User.validate(name)
            return c.execute('''SELECT u FROM users WHERE name = ?''', (name,)).fetchone()[0]

    @staticmethod
    def get_all_users():
        """
        Gets the data associated with the given user. Raises
        a KeyError if the user does not exist
        """
        sqlite3.register_converter("user", User.convert_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            users = c.execute('''SELECT * FROM users''').fetchall()
            return {user[0]: str(user[1]) for user in users}

    def update(self):
        """
        Updates the user preferences associated with the given user. Raises
        a KeyError if the user does not exist
        """
        sqlite3.register_adapter(User, User.adapt_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            if User.created(self.name):
                c.execute('''UPDATE users SET u = ? WHERE name = ?;''', (self, self.name))
                return f'User {self.name} updated.'
            else:
                raise KeyError(f'User {self.name} does not exist!')

    @staticmethod
    def update_preferences(name, new_prefs):
        user = User.get_user(name)
        user.preferences = new_prefs
        return User.update(user)

    @staticmethod
    def update_noise_pref(name, new_noise_pref):
        user = User.get_user(name)
        user.preferences['volumePref'] = new_noise_pref
        return User.update(user)