import sqlite3
from noise import *

database = "database.db"


class User:
    def __init__(self, name="anonymous", preferences=None):
        """
        Constructor for User object. Will create a new binding between
        a name and a User object in users table
        """
        assert ';' not in name, "Usernames cannot include ';'"
        self.name = name
        self.preferences = preferences

    # def __repr__(self):
    #     return f"User(\"{self.name}\",\"{self.preferences}\")"

    def __repr__(self):
        return f"User(\'{self.name}\', {{'noise' : {self.preferences['noise']}}})"

    def __str__(self):
        return f"{self.name} {Noise.str_form(self.preferences['noise'])}."

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
    def preferences(self):
        """
        Getter function for preferences attribute
        """
        if self._preferences is None:
            self._preferences = {'noise': Noise.no_pref}
        return self._preferences

    def get_noise_pref(self):
        return self.preferences['noise']

    @preferences.setter
    def preferences(self, value):
        """
        Setter function for preferences attribute. Raises
        a TypeError if input is not a string
        """
        if value is None:
            value = {'noise': Noise.no_pref}

        if not (isinstance(value, dict) and isinstance(value['noise'], Noise)):
            raise TypeError("Noise preferences must be a noise enum")
        self._preferences = value

    def upload(self):
        """
        Uploads a user to the users table. Raises
        an AssertionError if name is taken
        """
        sqlite3.register_adapter(User, User.adapt_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            if not User.created(self.name, c):
                c.execute('''INSERT INTO users VALUES (?, ?);''', (self.name, self))
                return f'Account {self.name} created.'
            else:
                raise AssertionError(f"The name '{self.name}' is already taken")

    def adapt_user(self):
        """
        Gets a string representation of a User object to store in
        SQL table. ONLY INTENDED FOR USE IN users TABLE
        """
        return f"{self.name};{self.preferences['noise'].value}"

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
        name, prefs = map(lambda x: x.decode("utf-8"), self.split(b";"))
        return User(name, {'noise': Noise(int(prefs))})

    @staticmethod
    def created(name, c):
        c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
        return c.execute('''SELECT EXISTS (SELECT 1 FROM users WHERE name = ?);''', (name,)).fetchone()[0]

    @staticmethod
    def validate(name, c):
        """
        Returns True if a user is in the database, raises
        KeyError otherwise
        """
        if not User.created(name, c):
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
            User.validate(name, c)
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
            if User.created(self.name, c):
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
        user.preferences['noise'] = new_noise_pref
        return User.update(user)