import sys, os

os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Accounts')
sys.path.append(server_path + '/Friends')

import requests
from datetime import datetime, timedelta
from dateutil import tz
from bs4 import BeautifulSoup

from accounts import *
from friends import *

database = '../database.db'

def currentEasternTime():
    """
    Returns the current Eastern Time.
    """
    UTC = tz.gettz('UTC')
    ET = tz.gettz('America/New_York')
    dt_utc = datetime.utcnow().replace(tzinfo=UTC)
    dt_est = dt_utc.astimezone(ET)
    return dt_est

def update_rooms(rooms=None):
    """
    Updates the database capacities and room names.
    If no parameter is provided, rooms are updated from
    https://now.mit.edu/latest-updates/touchdown-spaces-now-available/.
    """
    if rooms is None:
        rooms = {}
        rooms_html = requests.get("https://now.mit.edu/latest-updates/touchdown-spaces-now-available/")
        web_data = BeautifulSoup(rooms_html.text, 'html.parser')
        room_table = web_data.find('table')
        rows = room_table.findChildren('tr')
        for row in rows:
            try:
                room_num, capacity = map(lambda x: x.get_text(), row.find_all('td'))
                if "(" not in room_num:  # assume that room nums with parens are out of use
                    rooms[room_num] = int(capacity)
            except:
                continue
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        for room in rooms:
            try:
                c.execute('''INSERT INTO rooms VALUES (?, ?, ?, ?);''', (room, rooms[room], 0, 1))
            except sqlite3.IntegrityError:
                c.execute('''UPDATE rooms SET capacity=? WHERE name=?;''', (rooms[room], room))

def exists_room(room):
    """
    Checks if a room with the given name exists within the database.
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        return c.execute('''SELECT EXISTS (SELECT 1 FROM rooms WHERE name = ?);''', (room,)).fetchone()[0]

def validate_room(room):
    """
    Validates if a room with the given name exists within the database.
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        if not exists_room(room):
            raise KeyError(f"{room} is not a valid room")
        return True

def add_occupant(name, room, duration, volumePref):
    """
    Adds / checks in an occupant to a room, storing it in the database
    along with volume preference and start/end times.
    """
    with sqlite3.connect(database) as c:
        User.validate(name)
        validate_room(room)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text UNIQUE, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        startTime = currentEasternTime()
        endTime = startTime + timedelta(hours = duration)
        c.execute('''INSERT INTO occupants VALUES (?, ?, ?, ?, ?);''', (name, room, volumePref.value, startTime, endTime))

def remove_occupant(name, room):
    """
    Removes / checks out an occupant from a room.
    """
    with sqlite3.connect(database) as c:
        User.validate(name)
        validate_room(room)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text UNIQUE, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        c.execute('''DELETE FROM occupants WHERE user = ? AND room = ?;''', (name, room))

def user_in_rooms(name):
    """
    Checks if the given user name is checked in to a room.
    """
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text UNIQUE, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        return c.execute('''SELECT EXISTS (SELECT 1 FROM occupants WHERE user = ?);''', (name,)).fetchone()[0]

def get_room(name):
    """
    Returns the room that the user name is in, and returns None if not checked in.
    """
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(name)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text UNIQUE, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        if user_in_rooms(name):
            room, endTime = c.execute('''SELECT room, endTime FROM occupants WHERE user = ? ORDER BY startTime DESC;''', (name,)).fetchone()
            endTimeFormatted = endTime.strftime("%I:%M %p Eastern Time")
            return room, endTimeFormatted
        else:
            return None


def update_room_occupancy(room, occupancy):
    """
    Updates the room occupancy of a given room.
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        validate_room(room)
        c.execute('''UPDATE rooms SET occupancy=? WHERE name=?;''', (occupancy, room))


def increment_room_occupancy(room, occupancy_additional):
    """
    Increments the room occupancy of a given room.
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        validate_room(room)
        current_occupancy = c.execute('''SELECT occupancy FROM rooms WHERE name=?;''', (room,)).fetchone()[0]
        new_occupancy = current_occupancy + occupancy_additional
        c.execute('''UPDATE rooms SET occupancy=? WHERE name=?;''', (new_occupancy, room))


def update_room_noiseLevel(room, noiseLevel):
    """
    Updates the room noise level of a given room.
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        validate_room(room)
        c.execute('''UPDATE rooms SET noiseLevel=? WHERE name=?;''', (noiseLevel.value, room))

def get_friends_with_rooms(name):
    """
    Gets all friends of a given user name, along with the room (if any) that they are in.
    """
    friends = get_friends(name)
    friends_with_rooms = []
    for friend in friends:
        friend_info = {'name': friend, 'inRoom': False, 'room': None, 'until': None}
        info = get_room(friend)
        if info is not None:
            room, until = info
            friend_info = {'name': friend, 'inRoom': True, 'room': room, 'until': until}
        friends_with_rooms.append(friend_info)
    return friends_with_rooms

def get_room_info(room, name = None):
    """
    Gets the capacity, occupancy, noise level, and minimal volume preference of a given room number,
    along with friends in that room if a name is specified.
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        validate_room(room)
        info = c.execute('''SELECT capacity, occupancy, noiseLevel FROM rooms WHERE name=?;''', (room,)).fetchone()
        capacity, occupancy, noiseLevel = [int(data) for data in info]
        if capacity is None:
            raise KeyError(f"{room} is not a valid room")

        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text UNIQUE, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
        occupants = c.execute('''SELECT users.u, volumePref FROM occupants INNER JOIN users ON occupants.user = users.name WHERE occupants.room = ?;''', (room,)).fetchall()

    if len(occupants) != occupancy:
        # Someone didn't checkin / checkout properly!
        pass

    all_friends = []
    if name is not None:
        all_friends = get_friends(name)
    this_room_friends = list(set(all_friends) & {occupant[0].name for occupant in occupants})

    volumePrefFeq = {4: 0}
    for occupant in occupants:
        volumePref = int(occupant[1])
        volumePrefFeq[volumePref] = volumePrefFeq.get(volumePref, 0) + 1
    minVolumePref = min(volumePref for volumePref in volumePrefFeq)

    return {
        "roomNum": room,
        "capacity": capacity,
        "occupancy": occupancy,
        "numCheckedIn": len(occupants),
        # "occupants": [occupant[0] for occupant in occupants],
        "noiseLevel": Noise(noiseLevel).str_form(),
        "volumePref": {'volume': Noise(minVolumePref).str_form(), 'numPeople': volumePrefFeq[minVolumePref]},
        "friends": this_room_friends
    }

def get_all_rooms_info(name = None):
    """
    Gets the capacity, occupancy, noise level, and minimal volume preference of all rooms
    along with friends for each room if a name is specified.
    """
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        rooms = c.execute('''SELECT name from rooms''').fetchall()
        rooms = [room[0] for room in rooms]
        return [get_room_info(room, name) for room in rooms]

def auto_checkout():
    """
    Auto checkout any user that has not manually checked out after their end time.
    """
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text UNIQUE, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        c.execute('''DELETE FROM occupants WHERE endTime < ?;''', (currentEasternTime(),))