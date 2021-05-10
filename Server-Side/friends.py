import sqlite3
from users import *

database = "database.db"


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
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
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
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
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
        # sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.recipient=users.name WHERE friends.sender=?;''', (name,)).fetchall()
        # received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.sender=users.name WHERE friends.recipient=?;''', (name,)).fetchall()
        sent = c.execute('''SELECT friends.recipient, friends.status FROM friends WHERE friends.sender=?;''', (name,)).fetchall()
        received = c.execute('''SELECT friends.sender, friends.status FROM friends WHERE friends.recipient=?;''', (name,)).fetchall()
        all_requests = {'Sent': {friend[0] : friend[1] for friend in sent},
                        'Received': {friend[0] : friend[1] for friend in received}}
        return all_requests


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
        # sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.recipient=users.name WHERE friends.sender=?;''', (name,)).fetchall()
        # received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.sender=users.name WHERE friends.recipient=?;''', (name,)).fetchall()
        sent = c.execute('''SELECT friends.recipient FROM friends WHERE friends.sender=? AND friends.status = ?;''', (name, "accepted")).fetchall()
        received = c.execute('''SELECT friends.sender FROM friends WHERE friends.recipient=? AND friends.status = ?;''', (name, "accepted")).fetchall()
        friends = [friend[0] for friend in set(sent + received)]
        return friends