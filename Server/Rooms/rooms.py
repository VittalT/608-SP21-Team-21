import sys, os
# sys.path.append(os.path.abspath(__file__))
os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Accounts')
sys.path.append(server_path + '/Friends')

import requests
import datetime
from bs4 import BeautifulSoup

from accounts import *
from friends import *

database = '../database.db'

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
                c.execute('''INSERT INTO rooms VALUES (?, ?, ?, ?);''', (room, rooms[room], 0, 4))
            except sqlite3.IntegrityError:
                c.execute('''UPDATE rooms SET capacity=? WHERE name=?;''', (rooms[room], room))


def add_occupant(name, room, duration, volumePref):
    """
    Adds an occupant to a room. Raises a TypeError if occupant
    is not a User object and a KeyError if room does not exist
    """

    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(name)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        startTime = datetime.datetime.now()
        endTime = startTime + datetime.timedelta(hours = duration)
        c.execute('''INSERT INTO occupants VALUES (?, ?, ?, ?, ?);''', (name, room, volumePref.value, startTime, endTime))

def remove_occupant(name, room):
    """
    Adds an occupant to a room. Raises a TypeError if occupant
    is not a User object and a KeyError if room does not exist
    """
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(name)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        c.execute('''DELETE FROM occupants WHERE user = ? AND room = ?;''', (name, room))

def user_in_rooms(name):
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        return c.execute('''SELECT EXISTS (SELECT 1 FROM occupants WHERE user = ?);''', (name,)).fetchone()[0]

def get_room(name):
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        User.validate(name)
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        if user_in_rooms(name):
            return c.execute('''SELECT room, endTime FROM occupants WHERE user = ? ORDER BY startTime DESC;''', (name,)).fetchone()
        else:
            return None

def get_room_info(room, name = None):
    """
    Gets the data associated with a given room number. Raises
    a KeyError if the room does not exist
    """
    sqlite3.register_converter("user", User.convert_user)
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        info = c.execute('''SELECT capacity, occupancy, noiseLevel FROM rooms WHERE name=?;''', (room,)).fetchone()
        capacity, occupancy, noiseLevel = [int(data) for data in info]
        if capacity is None:
            raise KeyError(f"{room} is not a valid room")

        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (name text UNIQUE, u user);''')
        occupants = c.execute('''SELECT users.u, volumePref FROM occupants INNER JOIN users ON occupants.user = users.name WHERE occupants.room = ?;''', (room,)).fetchall()

    if len(occupants) != occupancy:
        # Someone didn't checkin / checkout properly!
        pass

    all_friends = []
    if name is not None:
        all_friends = get_friends(name)
    this_room_friends = list(set(all_friends) & {occupant[0] for occupant in occupants})

    volumePrefFeq = {4: 0}
    for occupant in occupants:
        volumePref = int(occupant[1])
        volumePrefFeq[volumePref] = volumePrefFeq.get(volumePref, 0) + 1
    minVolumePref = min(volumePref for volumePref in volumePrefFeq)

    return {
        "roomNum": room,
        "capacity": capacity,
        "occupancy": occupancy,
        # "occupants": [occupant[0] for occupant in occupants],
        "noiseLevel": Noise(noiseLevel).str_form(),
        "volumePref": {'volume': Noise(minVolumePref).str_form(), 'numPeople': volumePrefFeq[minVolumePref]},
        "friends": this_room_friends
    }

# def get_room_info(room):
#     room_info = get_room_info_with_occupants(room)
#     del room_info["occupants"]
#     return room_info

def get_all_rooms_info(name = None):
    with sqlite3.connect(database) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS rooms (name text UNIQUE, capacity integer, occupancy integer, noiseLevel integer);''')
        rooms = c.execute('''SELECT name from rooms''').fetchall()
        rooms = [room[0] for room in rooms]
        return [get_room_info(room, name) for room in rooms]

def auto_checkout():
    """
    Auto checkout if time is after endTime
    """
    with sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS occupants (user text, room text, volumePref integer, startTime timestamp, endTime timestamp);''')
        c.execute('''DELETE FROM occupants WHERE endTime > ?;''', (datetime.datetime.now(),))