import requests
import sqlite3
import datetime
from bs4 import BeautifulSoup
from enum import Enum

# change this
database = "database.db"

###############
# NOISE PREF #
###############

class Noise(Enum):
    no_pref = 0
    quiet = 1
    moderate = 2
    loud = 3

    def str_form(self):
        if self == Noise.no_pref:
            return 'has no noise preference'
        elif self == Noise.quiet:
            return 'prefers quiet noise levels'
        elif self == Noise.moderate:
            return 'prefers moderate noise levels'
        elif self == Noise.loud:
            return 'prefers loud noise levels'
        else:
            return 'has an unknown preference'

def str_to_enum(noise):
    if noise == 'no_pref':
        return Noise.no_pref
    elif noise == 'quiet':
        return Noise.quiet
    elif noise == 'moderate':
        return Noise.moderate
    elif noise == 'loud':
        return Noise.loud
###############
# USER SYSTEM #
###############

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
        if self._name == None:
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
        if self._preferences == None:
            self._preferences = {'noise' : Noise.no_pref}
        return self._preferences

    def get_noise_pref(self):
        return self.preferences['noise']

    @preferences.setter
    def preferences(self, value):
        """
        Setter function for preferences attribute. Raises
        a TypeError if input is not a string
        """
        if value == None:
            value = {'noise' : Noise.no_pref}

        if not (isinstance(value, dict) and isinstance(value['noise'], Noise)):
            raise TypeError("Noise preferences must be a noise enum")
        self._preferences = value

    def update_noise_pref(self, new_noise_pref):
        self.preferences['noise'] = new_noise_pref

    def upload(self):
        """
        Uploads a user to the users table. Raises
        an AssertionError if name is taken
        """
        sqlite3.register_adapter(User, User.adapt_user)
        with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
            if not user_created(self.name, c):
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

    def convert_user(s):
        """
        Converts a bytes response from an SQL table into
        a User object
        """
        name, prefs = map(lambda x: x.decode("utf-8"), s.split(b";"))
        return User(name, {'noise': Noise(int(prefs))})

    @staticmethod
    def validate(name, c):
        """
        Returns True if a user is in the database, raises
        KeyError otherwise
        """
        if not user_created(name, c):
            raise KeyError(f"{name} is not a valid user")
        return True


def user_created(name, c):
    return c.execute('''SELECT EXISTS (SELECT 1 FROM users WHERE name = ?);''', (name,)).fetchone()[0]

def get_user(name):
    """
    Gets the data associated with the given user. Raises
    a KeyError if the user does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(name, c)
        return c.execute('''SELECT u FROM users WHERE name = ?''', (name,)).fetchone()[0]

def get_all_users():
    """
    Gets the data associated with the given user. Raises
    a KeyError if the user does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        users = c.execute('''SELECT * FROM users''').fetchall()
        return {user[0] : str(user[1]) for user in users}

def update_users(user):
    """
    Updates the user preferences associated with the given user. Raises
    a KeyError if the user does not exist
    """
    sqlite3.register_adapter(User, User.adapt_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        if user_created(user.name, c):
            c.execute('''UPDATE users SET u = ? WHERE name = ?;''', (user, user.name))
            return f'User {user.name} updated.'
        else:
            raise KeyError(f'User {user.name} does not exist!')

def update_preferences(name, prefs):
    return update_users(User(name, prefs))

def update_noise_pref(name, noise_pref):
    return update_preferences(name, {'noise': noise_pref})

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

def add_occupant(room, occupant=User()):
    """
    Adds an occupant to a room. Raises a TypeError if occupant
    is not a User object and a KeyError if room does not exist
    """
    if not isinstance(occupant, User):
        raise TypeError ("Occupants must be User")
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(occupant.name, c)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, timing timestamp);''')
        c.execute('''INSERT INTO occupants VALUES (?, ?, ?);''', (occupant, room, datetime.datetime.now()))

def user_in_rooms(name, c):
    return c.execute('''SELECT EXISTS (SELECT 1 FROM occupants WHERE user = ?);''', (name,)).fetchone()[0]

def get_data(room):
    """
    Gets the data associated with a given room number. Raises
    a KeyError if the room does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity int);''')
        capacity = c.execute('''SELECT capacity FROM rooms WHERE name=?;''', (room,)).fetchone()[0]
        if capacity == None:
            raise KeyError(f"{room} is not a valid room")
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, timing timestamp);''')
        occupants = c.execute('''SELECT users.u FROM occupants INNER JOIN users ON occupants.user = users.name WHERE occupants.room = ?;''', (room,)).fetchall()
    return {
        "room" : room,
        "capacity" : capacity,
        "occupants" : [occupant[0] for occupant in occupants]
    }

def get_all_data():
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity int);''')
        rooms = c.execute('''SELECT name from rooms''').fetchall()
        rooms = [room[0] for room in rooms]
        return [get_data(room) for room in rooms]

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
        if recipient in get_friend_requests(sender):
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
        if friend in get_friends(user):
            c.execute('''DELETE FROM friends WHERE (sender=? AND recipient=?) OR (sender=? and recipient=?);''', (user, friend, friend, user))
        else:
            raise KeyError(f"Not friends with {friend}")

def get_friend_requests(name):
    """
    Returns a dictionary containing all friends
    and friend requests, along with status. Raises
    a KeyError if user does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        User.validate(name, c)
        #sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.recipient=users.name WHERE friends.sender=?;''', (name,)).fetchall()
        #received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.sender=users.name WHERE friends.recipient=?;''', (name,)).fetchall()
        sent = c.execute('''SELECT friends.recipient, friends.status FROM friends WHERE friends.sender=?;''', (name,)).fetchall()
        received = c.execute('''SELECT friends.sender, friends.status FROM friends WHERE friends.recipient=?;''', (name,)).fetchall()
        return f'Sent: { {friend[0] : friend[1] for friend in sent} }\nReceived: { {friend[0] : friend[1] for friend in received} }'

def get_friends(name):
    """
    Returns a dictionary containing all friends
    and friend requests, along with status. Raises
    a KeyError if user does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        User.validate(name, c)
        #sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.recipient=users.name WHERE friends.sender=?;''', (name,)).fetchall()
        #received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.sender=users.name WHERE friends.recipient=?;''', (name,)).fetchall()
        sent = c.execute('''SELECT friends.recipient FROM friends WHERE friends.sender=? AND friends.status = ?;''', (name, "accepted")).fetchall()
        received = c.execute('''SELECT friends.sender FROM friends WHERE friends.recipient=? AND friends.status = ?;''', (name, "accepted")).fetchall()
        friends = set(sent + received)
        return [friend[0] for friend in friends]

# WEEK 2 Deliverable - request handler


def request_handler(request):
    '''
	Function executes get and post requests by interfacing with other functions that have been written.
	Checks that the inputs provided are valid, and, if they are, returns the correct outputs
	GET requests to get rooms, friend data or preferences
	POST request to pref, checkin, login, addfriend, requestfriend, removefriend

	GET rooms: provide all rooms, capacities, num_occupied, #TODO: checkin option
	GET pref: provide user
	GET friends: provide user
	GET friend_requests: provide user
	#TODO: GET login: to be figured out using google - will be integrated and updated later

	POST pref: provide user, noise
	POST request_friend: provide user, friend
	POST accept_friend: provide user, friend
	POST remove_friend: provide user, friend
	#TODO: POST checkin: provide user, room, (opt) noise
	#TODO: POST login: to be figured out using google - will be integrated and updated later
	'''

    try:
        if request["method"] == "GET":
            if request["values"]["task"]=="rooms":
                all_rooms = get_all_data()
                for room in all_rooms:
                    room['num_occupants'] = len(room['occupants'])
                    del room['occupants']
                return all_rooms

            elif request["values"]["task"] == "pref":
                name = request["values"]["user"]
                return get_user(name)

            elif request["values"]["task"] == "friend_requests":
                name = request["values"]["user"]
                return get_friend_requests(name)

            elif request["values"]["task"] == "friends":
                name = request["values"]["user"]
                return get_friends(name)


        elif request["method"] == "POST":
            if request["form"]["task"] == "create_account":
                name = request["values"]["user"]
                noise_pref = str_to_enum(request["form"]["noise"])
                #user = User(name, {'noise': noise_pref})
                user.upload()

            elif request["form"]["task"] == "pref":
                name = request["form"]["user"]
                noise_pref = str_to_enum(request["form"]["noise"])
                return update_noise_pref(name, noise_pref)

            elif request["form"]["task"] == "request_friend":
                sender = request["form"]["user"]
                recipient = request["form"]["friend"]
                return send_request(sender, recipient)

            elif request["form"]["task"] == "accept_friend":
                sender = request["form"]["user"]
                recipient = request["form"]["friend"]
                return accept_request(sender, recipient)

            elif request["form"]["task"] == "remove_friend":
                sender = request["form"]["user"]
                recipient = request["form"]["friend"]
                return remove_friend(sender, recipient)

            elif request["form"]["task"] == "checkin":
                name = request["form"]["user"]
                user = get_user(name)
                room = request["form"]["room"]
                print(user, room)
                return add_occupant(room, user)

            elif request["form"]["task"] == "login": #TODO
                User = get_user(request["form"]["user"])
                return "Code to be called not yet complete. Input valid."
    except Exception as e:
        return e

if __name__ == '__main__':
    print("\n\nWeek 1")
    me = User('Vittal', {'noise': Noise.loud})
    print(repr(me))
    print(me)
    me.update_noise_pref(Noise.moderate)
    print(me)
    print()

    Ricardo = User('Ricardo', {'noise': Noise.no_pref})
    print(Ricardo.upload())
    print(get_user('Ricardo'))
    print(update_noise_pref('Ricardo', Noise.quiet))
    print(get_user('Ricardo'))
    print(get_all_users())
    print()

    print(me.upload())
    try:
        me.upload()
    except Exception as e:
        print(e)
    print(get_user('Vittal'))
    print(update_noise_pref('Vittal', Noise.loud))
    print(get_user('Vittal'))
    try:
        get_user('RandomUnknown')
    except Exception as e:
        print(e)
    print(get_all_users())

    print("\n\nWeek 2")
    update_rooms()

    print(request_handler({"method":"GET", "values":{"task":"rooms"}}))
    print(request_handler({"method":"POST", "form":{"user":"Vittal", "task":"pref", "noise":"quiet"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "pref"}}))
    print(request_handler({"method":"POST", "form":{"user":"Vittal", "task":"pref", "noise":"moderate"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "pref"}}))
    print()

    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "pref"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "friends"}}))
    print()

    requests = [
        {"method": "POST", "form": {"user": "Vittal", "friend": "Ricardo", "task": "request_friend"}},
        {"method": "POST", "form": {"user": "Ricardo", "friend": "Vittal", "task": "accept_friend"}},
        {"method": "POST", "form": {"user": "Ricardo", "friend": "Vittal", "task": "remove_friend"}}
    ]

    for request in requests:
        print(request)
        print(request_handler(request))
        for user in ['Vittal', 'Ricardo']:
            for task in ['friends', 'friend_requests']:
                print(user, task)
                print(request_handler({"method": "GET", "values": {"user": user, "task": task}}))
        print()

