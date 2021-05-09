import requests
import sqlite3
import datetime
from bs4 import BeautifulSoup

# change this
database = "database.db"

###############
# USER SYSTEM #
###############

class User:

    def __init__(self, name="anonymous", preferences=""):
        """
        Constructor for User object. Will create a new binding between
        a name and a User object in users table
        """
        assert ';' not in name, "Usernames cannot include ';'"
        self._name = name
        self.preferences = preferences

    def __repr__(self):
        return f"User(\"{self._name}\",\"{self.preferences}\")"

    @property
    def preferences(self):
        """
        Getter function for preferences attribute
        """
        if self._preferences == None:
            return ""
        return self._preferences
    
    @preferences.setter
    def preferences(self, value):
        """
        Setter function for preferences attribute. Raises
        a TypeError if input is not a string
        """
        if not isinstance(value, str):
            raise TypeError("Preferences must be string")
        self._preferences = value

    def upload(self):
        """
        Uploads a user to the users table. Raises
        an AssertionError if name is taken
        """
        sqlite3.register_adapter(User, User.adapt_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            try:
                c.execute('''INSERT INTO users VALUES (?, ?);''', (self._name, self))
            except sqlite3.IntegrityError:
                raise AssertionError(f"The name '{self._name}' is already taken")

    def adapt_user(self):
        """
        Gets a string representation of a User object to store in
        SQL table. ONLY INTENDED FOR USE IN users TABLE
        """
        return f"{self._name};{self.preferences}"

    def __conform__(self, protocol):
        """
        Standard way to store a User in a table by storing
        only their name
        """
        if protocol is sqlite3.PrepareProtocol:
            return self._name
    
    def convert_user(s):
        """
        Converts a bytes response from an SQL table into
        a User object
        """
        name, prefs = map(lambda x: x.decode("utf-8"), s.split(b";"))
        return User(name, prefs)

    @staticmethod
    def validate(name, c):
        """
        Returns True if a user is in the database, raises
        KeyError otherwise
        """
        if c.execute('''SELECT u FROM users WHERE name=?;''', (name,)).fetchall() == []:
            raise KeyError(f"{name} is not a valid user")
        return True

################
# ROOMS SYSTEM #
################

def update_rooms(rooms=None):
    """
    Updates the database capacities and room names.
    If no parameter is provided, rooms are updated from
    https://now.mit.edu/latest-updates/touchdown-spaces-now-available/.
    """
    if rooms == None:
        rooms = {}
        rooms_html = requests.get("https://now.mit.edu/latest-updates/touchdown-spaces-now-available/")
        web_data = BeautifulSoup(rooms_html.text, 'html.parser')
        room_table = web_data.find('table')
        rows = room_table.findChildren('tr')
        for row in rows:
            try:
                room_num, capacity = map(lambda x: x.get_text(), row.find_all('td'))
                if "(" not in room_num: # assume that room nums with parens are out of use
                    rooms[room_num] = int(capacity)
            except:
                continue
    with sqlite3.connect(database) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity int);''')
            for room in rooms:
                try:
                    c.execute('''INSERT INTO rooms VALUES (?, ?);''', (room, rooms[room]))
                except sqlite3.IntegrityError:
                    c.execute('''UPDATE rooms SET capacity=? WHERE name=?;''', (rooms[room], room))

def add_occupant(room, occupant=None):
    """
    Adds an occupant to a room. Raises a TypeError if occupant 
    is not a User object and a KeyError if room does not exist
    """
    if occupant == None:
        occupant = User()
    if not isinstance(occupant, User):
        raise TypeError ("Occupants must be User")
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(occupant._name, c)
        if c.execute('''SELECT * FROM rooms WHERE name=?;''', (room,)).fetchone() == []:
            raise KeyError(f"{room} is not a valid room")
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, timing timestamp);''')
        c.execute('''INSERT INTO occupants VALUES (?, ?, ?);''', (occupant, room, datetime.datetime.now()))

def get_data(room):
    """
    Gets the data associated with a given room number. Raises
    a KeyError if the room does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        capacity = c.execute('''SELECT capacity FROM rooms WHERE name=?;''', (room,)).fetchone()
        if capacity == None:
            raise KeyError(f"{room} is not a valid room")
        occupants = c.execute('''SELECT users.u FROM occupants INNER JOIN users ON occupants.user = users.name;''')
    return {
        "room" : room,
        "capacity" : capacity,
        "occupants" : [occupant for occupant in occupants]
    }
        
##################
# FRIENDS SYSTEM #
##################

def send_request(sender, recipient):
    """
    Sends a friend request from the sender user to the 
    recipient user. Raises a KeyError if either user 
    does not exist and AssertionError if relationship
    is already in database
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        User.validate(sender, c)
        User.validate(recipient, c)
        # raices exception if friendship already exists
        if recipient in get_friends(sender):
            raise AssertionError(f"Already contacted {recipient}")
        c.execute('''INSERT INTO friends VALUES (?, ?, ?);''', (sender, recipient, "pending"))

def accept_request(user, sender):
    """
    Accepts a friend request from a given user
    """
    with sqlite3.connect(database) as c:
        User.validate(user, c)
        User.validate(sender, c)
        try:
            if c.execute('''SELECT status FROM friends WHERE sender=? AND recipient=?;''', (sender, user)).fetchone()[0] == "pending":
                c.execute('''UPDATE friends SET status=? WHERE sender=? AND recipient=?;''', ("accepted", sender, user))
            else:
                raise KeyError(f"No pending friend request from {sender} exists")
        except TypeError:
            raise KeyError(f"No friend request from {sender} exists")

def remove_friend(user, friend):
    """
    Accepts a friend request from a given user
    """
    with sqlite3.connect(database) as c:
        User.validate(user, c)
        User.validate(friend, c)
        if friend in [f._name for f in get_friends(user)]:
                c.execute('''DELETE FROM friends WHERE (sender=? AND recipient=?) OR (sender=? and recipient=?);''', (user, friend, friend, user))
        else:
            raise KeyError(f"Not friends with {friend}")

def get_friends(user):
    """
    Returns a dictionary containing all friends
    and friend requests, along with status. Raises
    a KeyError if user does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        if not c.execute('''SELECT u FROM users WHERE name=?;''', (user,)).fetchone():
            raise KeyError(f"{user} is not a valid user")
        sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users WHERE friends.sender=? AND users.name=friends.recipient;''', (user,)).fetchall()
        received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users WHERE friends.recipient=? AND users.name=friends.sender;''', (user,)).fetchall()
        friends = sent + received
        return {friend[0] : friend[1] for friend in friends}


if __name__ == '__main__':
    pass