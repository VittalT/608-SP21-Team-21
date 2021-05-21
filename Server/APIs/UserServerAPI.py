import json
import sys, os

os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Friends')
sys.path.append(server_path + '/Rooms')
sys.path.append(server_path + '/Login')

from friends import *
from rooms import *
from login import *

database = '../database.db'

def request_handler(request):
    """
	Function that executes GET and POST requests from the user webpage, by interfacing with functions from friends, rooms, and login.py.
	Checks that the inputs provided are valid, and, if they are, updates the database and returns the correct outputs.
	GET: loginPage, checkinPage, dashboardPage, friendsPage, friends, friendRequests, rooms, isCheckedIn, preferences
	POST: createAccount, login, preferences, requestFriend, acceptFriend, removeFriend, checkin, checkout, updateRooms, autoCheckout

    GET
    - loginPage:
        - Returns: everything between <html> tags of login page html file
    - checkinPage:
        - Returns: everything between <html> tags of checkin page html file
    - dashboardPage:
        - Returns: everything between <html> tags of dashboard page html file
    - friendsPage:
        Returns: everything between <html> tags of the friends page html file
    - friends: user, token
        - Returns: A JSON dictionary containing keys requestFriendsSuccess, status, and friends
        - friends key: JSON list, where each entry denotes a friend containing the keys “name”, “inRoom”, “room”, “until”. “inRoom” will be true if this friend is currently in a room.
    - friendRequests: user, token
        - Returns: A JSON dictionary containing keys requestFriendRequestsSuccess, status, and friendRequests
            - friendRequests key: A JSON dictionary containing keys ‘sent’ and ‘received’, each containing a dictionary of key name and value ‘pending’ or ‘accepted’
    - rooms: optional: user, token
        - Returns: A JSON dictionary containing keys requestRoomsSuccess, status, and rooms.
            - rooms key: List of dictionaries, where each dictionary denotes a room and takes the following format:
            { roomNum: string,
            capacity: string or number,
            occupancy: string or number,
            noiseLevel: string,
            volumePref: dictionary containing keys volume and numPeople,
            friends: list (empty if no name/token provided, or if no friends
                checked in) }
    - isCheckedIn: user, token
        - Returns:
        { isCheckedInSuccess: string
          status: string
          isCheckedIn: bool
         roomNum: string
         until: string }
     - preferences: user, token
        - Returns:
        { requestPreferencesSuccess: bool
          status: string
        }

    POST
    - createAccount: user, password
        - Returns:
        { createAccountSuccess: bool
          token: string
        }
    - login: user, password
        - Returns:
        { loginSuccess: bool
          token: string
        }
    - preferences: user, token, volumePref
    - requestFriend: user, token, friend
        - Returns:
        { requestFriendSuccess: bool, status: string }
    - acceptFriend: user, token, friend
        - Returns:
        { addFriendSuccess: bool, status: string }
    - ignoreFriend: user, token, friend
        - Returns:
        { ignoreFriendSuccess: bool, status: string }
    - removeFriend: user, token, friend
        - Returns:
        { removeFriendSuccess: bool, status: string }
    - checkin: user, token, roomNum, duration, volumePref
        - volumePref can be either “quiet”, “moderate”, “loud”, or “noPref”
        - Returns:
        { checkinSuccess: bool, status: string }
    - checkout: user, token, roomNum
        - Returns:
        { checkoutSuccess: bool, status: string }
    - updateRooms:
        - Updates list of rooms and capacities from Atlas
        - Returns:
        { updateRoomsSuccess: bool, status: string }
    - autoCheckout:
        - Auto checkout when endTime has passed
        - Returns:
        { autoCheckoutSuccess: bool, status: string }
	"""

    if request["method"] == "GET":
        if request["values"]["task"] == "loginPage":
            with open("../UI/Login/login.html") as f:
                body = f.read()
                return body

        elif request["values"]["task"] == "checkinPage":
            with open("../UI/Checkin/checkin.html") as f:
                body = f.read()
                return body

        elif request["values"]["task"] == "friendsPage":
            auto_checkout()
            with open("../UI/Friends/friends.html") as f:
                body = f.read()
                return body

        elif request["values"]["task"] == "dashboardPage":
            update_rooms()
            auto_checkout()
            with open("../UI/Dashboard/dashboard.html") as f:
                body = f.read()
                return body

        elif request["values"]["task"] == "preferences":
            name = request["values"]["user"]
            token = request["values"]["token"]
            if not correct_token(name, token):
                return json.dumps({'getPreferencesSuccess': False, 'status': 'Invalid token', 'volumePref': None})

            user = User.get_user(name)
            volumePref = user.info['volumePref']
            return json.dumps({'getPreferencesSuccess': True, 'status': 'Success, Logged in', 'volumePref': volumePref})

        elif request["values"]["task"] == "friends":
            name = request["values"]["user"]
            token = request["values"]["token"]
            if not correct_token(name, token):
                return json.dumps({'getFriendsSuccess': False, 'status': 'Invalid token', 'friends': None})

            return json.dumps({'getFriendsSuccess': True, 'status': 'Success, Logged in', 'friends': get_friends_with_rooms(name)})

        elif request["values"]["task"] == "friendRequests":
            name = request["values"]["user"]
            token = request["values"]["token"]
            if not correct_token(name, token):
                return json.dumps({'getFriendRequestsSuccess': False, 'status': 'Invalid token', 'friendRequests': None})

            return json.dumps({'getFriendRequestsSuccess': True, 'status': 'Success, Logged in', 'friendRequests': pending_friend_requests(name)})

        elif request["values"]["task"] == "rooms":
            update_rooms()
            auto_checkout()
            if "user" in request["values"]:
                name = request["values"]["user"]
                token = request["values"]["token"]
                if not correct_token(name, token):
                    return json.dumps({'getRoomsSuccess': False, 'status': 'Invalid token', 'rooms': None})
                all_rooms = get_all_rooms_info(name)
                return json.dumps({'getRoomsSuccess': True, 'status': 'Success, Logged in', 'rooms': all_rooms})
            else:
                all_rooms = get_all_rooms_info()
                return json.dumps({'getRoomsSuccess': True, 'status': 'Success, Not logged in', 'rooms': all_rooms})

        elif request["values"]["task"] == "isCheckedIn":
            name = request["values"]["user"]
            token = request["values"]["token"]
            if not correct_token(name, token):
                return json.dumps({'isCheckedInSuccess': False, 'status': 'Invalid token', 'isCheckedIn': None, 'roomNum': None, 'until': None})

            roomInfo = get_room(name)
            if roomInfo is None:
                return json.dumps({'isCheckedInSuccess': True, 'status': None, 'isCheckedIn': False, 'roomNum': None, 'until': None})

            room, endTime = roomInfo
            return json.dumps({'isCheckedInSuccess': True, 'status': None, 'isCheckedIn': True, 'roomNum': room, 'until': endTime})

        else:
            return KeyError("Unknown GET request")


    elif request["method"] == "POST":
        if request["form"]["task"] == "createAccount":
            name = request["form"]["user"]
            password = request["form"]["password"]
            if User.created(name):
                # User already exists
                return json.dumps({'createAccountSuccess': False, 'token': None})

            token = generateToken()
            user = User(name, {'password': password, 'token': token, 'volumePref': Noise.noPref})
            user.upload()
            return json.dumps({'createAccountSuccess': True, 'token': token})

        elif request["form"]["task"] == "login":
            name = request["form"]["user"]
            password = request["form"]["password"]
            if correct_password(name, password):
                user = User.get_user(name)
                token = generateToken()
                user.info['token'] = token
                user.update()
                return json.dumps({"loginSuccess": True, 'token': token})
            else:
                return json.dumps({"loginSuccess": False, 'token': None})

        elif request["form"]["task"] == "preferences":
            name = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(name, token):
                return json.dumps({'updatePreferencesSuccess': False, 'status': 'Invalid token'})

            volumePref = Noise.str_to_enum(request["form"]["volumePref"])
            user = User.get_user(name)
            user.info['volumePref'] = volumePref
            user.update()
            return json.dumps({'updatePreferencesSuccess': True, 'status': 'Success, Logged in'})

        elif request["form"]["task"] == "requestFriend":
            sender = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(sender, token):
                return json.dumps({'requestFriendSuccess': False, 'status': 'Invalid token'})

            recipient = request["form"]["friend"]
            try:
                send_request(sender, recipient)
                return json.dumps({'requestFriendSuccess': True, 'status': 'Success, Logged in'})
            except:
                json.dumps({'requestFriendSuccess': False, 'status': 'Could not request friend'})

        elif request["form"]["task"] == "acceptFriend":
            sender = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(sender, token):
                return json.dumps({'acceptFriendSuccess': False, 'status': 'Invalid token'})

            recipient = request["form"]["friend"]
            try:
                accept_request(sender, recipient)
                return json.dumps({'acceptFriendSuccess': True, 'status': 'Success, Logged in'})
            except:
                json.dumps({'acceptFriendSuccess': False, 'status': 'Could not accept friend'})

        elif request["form"]["task"] == "ignoreFriend":
            sender = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(sender, token):
                return json.dumps({'ignoreFriendSuccess': False, 'status': 'Invalid token'})

            recipient = request["form"]["friend"]
            try:
                remove_request(sender, recipient)
                return json.dumps({'ignoreFriendSuccess': True, 'status': 'Success, Logged in'})
            except:
                json.dumps({'ignoreFriendSuccess': False, 'status': 'Could not ignore friend request'})

        elif request["form"]["task"] == "removeFriend":
            sender = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(sender, token):
                return json.dumps({'removeFriendSuccess': False, 'status': 'Invalid token'})

            recipient = request["form"]["friend"]
            try:
                remove_friend(sender, recipient)
                return json.dumps({'removeFriendSuccess': True, 'status': 'Success, Logged in'})
            except:
                json.dumps({'removeFriendSuccess': False, 'status': 'Could not remove friend'})

        elif request["form"]["task"] == "checkin":
            name = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(name, token):
                return json.dumps({'checkinSuccess': False, 'status': 'Invalid token'})

            room = request["form"]["roomNum"]
            duration = int(request["form"]["duration"])
            volumePref = Noise.str_to_enum(request["form"]["volumePref"])
            try:
                add_occupant(name, room, duration, volumePref)
                return json.dumps({'checkinSuccess': True, 'status': None})
            except:
                return json.dumps({'checkinSuccess': False, 'status': 'Could not checkin'})

        elif request["form"]["task"] == "checkout":
            name = request["form"]["user"]
            token = request["form"]["token"]
            if not correct_token(name, token):
                return json.dumps({'checkoutSuccess': False, 'status': 'Invalid token'})

            room = request["form"]["roomNum"]
            try:
                remove_occupant(name, room)
                return json.dumps({'checkoutSuccess': True, 'status': None})
            except:
                return json.dumps({'checkoutSuccess': False, 'status': 'Could not checkout'})

        elif request["form"]["task"] == "updateRooms":
            try:
                update_rooms()
                return json.dumps({'updateRoomsSuccess': True, 'status': None})
            except:
                return json.dumps({'updateRoomsSuccess': False, 'status': 'Could not update rooms from Atlas'})

        elif request["form"]["task"] == "autoCheckout":
            try:
                auto_checkout()
                return json.dumps({'autoCheckoutSuccess': True, 'status': None})
            except:
                return json.dumps({'autoCheckoutSuccess': False, 'status': 'Could not auto checkout'})

        else:
            return KeyError("Unknown POST request")

    else:
        return KeyError("Unknown GET/POST request")