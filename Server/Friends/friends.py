import sys, os

os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Accounts')

from accounts import *

database = '../database.db'

def send_request(sender, recipient):
    """
    Sends a friend request from the sender user to the recipient user.
    """

    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        User.validate(sender)
        User.validate(recipient)
        if sender == recipient:
            raise AssertionError("Cannot friend yourself :P")
        # raices exception if friendship already exists
        if c.execute('''SELECT EXISTS (SELECT 1 FROM friends WHERE sender=? AND recipient=?);''', (sender, recipient)).fetchone()[0]:
            raise AssertionError(f"Already contacted {recipient}")
        c.execute('''INSERT INTO friends VALUES (?, ?, ?);''', (sender, recipient, "pending"))


def accept_request(user, sender):
    """
    Accepts a friend request from the sender user to the current user.
    """
    with sqlite3.connect(database) as c:
        User.validate(user)
        User.validate(sender)
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        try:
            if c.execute('''SELECT status FROM friends WHERE sender=? AND recipient=?;''', (sender, user)).fetchone()[0] == "pending":
                c.execute('''UPDATE friends SET status=? WHERE sender=? AND recipient=?;''', ("accepted", sender, user))
            else:
                raise KeyError(f"No pending friend request from {sender} exists")
        except TypeError:
            raise KeyError(f"No friend request from {sender} exists")

def remove_request(user, sender):
    """
    Ignores / removes a friend request from the sender user to the current user.
    """
    with sqlite3.connect(database) as c:
        User.validate(user)
        User.validate(sender)
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        try:
            if c.execute('''SELECT status FROM friends WHERE sender=? AND recipient=?;''', (sender, user)).fetchone()[0] == "pending":
                c.execute('''DELETE FROM friends WHERE sender=? AND recipient=?;''', (sender, user))
            else:
                raise KeyError(f"No pending friend request from {sender} exists")
        except TypeError:
            raise KeyError(f"No friend request from {sender} exists")

def remove_friend(user, friend):
    """
    Removes the friends status of current user and friend user.
    """
    with sqlite3.connect(database) as c:
        User.validate(user)
        User.validate(friend)
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        if friend in get_friends(user):
            c.execute('''DELETE FROM friends WHERE (sender=? AND recipient=?) OR (sender=? and recipient=?);''', (user, friend, friend, user))
        else:
            raise KeyError(f"Not friends with {friend}")

def all_friend_requests(name):
    """
    Returns a dictionary containing all friend requests (both sent and received), along with status.
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        User.validate(name)
        # sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.recipient=users.name WHERE friends.sender=?;''', (name,)).fetchall()
        # received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.sender=users.name WHERE friends.recipient=?;''', (name,)).fetchall()
        sent = c.execute('''SELECT friends.recipient, friends.status FROM friends WHERE friends.sender=?;''', (name,)).fetchall()
        received = c.execute('''SELECT friends.sender, friends.status FROM friends WHERE friends.recipient=?;''', (name,)).fetchall()
        all_requests = {'sent': [{'name': friend[0], 'status': friend[1]} for friend in sent],
                        'received': [{'name': friend[0], 'status': friend[1]} for friend in received]}
        return all_requests

def pending_friend_requests(name):
    """
    Returns a dictionary containing all pending friend requests (both sent and received), along with status.
    """
    all_requests = all_friend_requests(name)
    return {'sent': [friend_request for friend_request in all_requests['sent'] if friend_request['status'] == 'pending'],
            'received': [friend_request for friend_request in all_requests['received'] if friend_request['status'] == 'pending']}

def get_friends(name):
    """
    Returns a list containing all friends of the user with the given name.
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS friends (sender text, recipient text, status text);''')
        User.validate(name)
        # sent = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.recipient=users.name WHERE friends.sender=?;''', (name,)).fetchall()
        # received = c.execute('''SELECT users.u, friends.status FROM friends INNER JOIN users ON friends.sender=users.name WHERE friends.recipient=?;''', (name,)).fetchall()
        sent = c.execute('''SELECT friends.recipient FROM friends WHERE friends.sender=? AND friends.status = ?;''', (name, "accepted")).fetchall()
        received = c.execute('''SELECT friends.sender FROM friends WHERE friends.recipient=? AND friends.status = ?;''', (name, "accepted")).fetchall()
        friends = [friend[0] for friend in set(sent + received)]
        return friends