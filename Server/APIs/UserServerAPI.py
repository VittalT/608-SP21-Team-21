import json
import sys, os
# sys.path.append(os.path.abspath(__file__))
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
    '''
	Function executes get and post requests by interfacing with other functions that have been written.
	Checks that the inputs provided are valid, and, if they are, returns the correct outputs
	GET requests to get login/create account page, user preferences, friends, friend requests, and rooms data
	POST request to create account, login, update preferences, request friend, accept friend, remove friend, and checkin

    #TODO: GET login: to be figured out using google - will be integrated and updated later
	GET pref: provide user
	GET friends: provide user
	GET friend requests: provide user
	GET rooms: provide all rooms, capacities, num_occupies, checkin, and checkout option

	#TODO: POST login: to be figured out using google - will be integrated and updated later
	POST pref: provide user, noise
	POST request friend: provide user, friend
	POST accept friend: provide user, friend
	POST remove friend: provide user, friend
	POST checkin: provide user, room
	POST checkout: provide user, room
	'''
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
                return json.dumps({'requestPreferencesSuccess': False, 'status': 'Invalid token', 'volumePref': None})

            user = User.get_user(name)
            volumePref = user.info['volumePref']
            return json.dumps({'requestPreferencesSuccess': True, 'status': 'Success, Logged in', 'volumePref': volumePref})

        elif request["values"]["task"] == "friends":
            name = request["values"]["user"]
            token = request["values"]["token"]
            if not correct_token(name, token):
                return json.dumps({'requestFriendSuccess': False, 'status': 'Invalid token', 'friends': None})

            return json.dumps({'requestFriendSuccess': True, 'status': 'Success, Logged in', 'friends': get_friends_with_rooms(name)})

        elif request["values"]["task"] == "friendRequests":
            name = request["values"]["user"]
            token = request["values"]["token"]
            if not correct_token(name, token):
                return json.dumps({'requestFriendRequestsSuccess': False, 'status': 'Invalid token', 'friendRequests': None})

            return json.dumps({'requestFriendRequestsSuccess': True, 'status': 'Success, Logged in', 'friendRequests': get_friend_requests(name)})

        elif request["values"]["task"] == "rooms":
            update_rooms()
            auto_checkout()
            if "user" in request["values"]:
                name = request["values"]["user"]
                token = request["values"]["token"]
                if not correct_token(name, token):
                    return json.dumps({'requestRoomsSuccess': False, 'status': 'Invalid token', 'rooms': None})
                all_rooms = get_all_rooms_info(name)
                return json.dumps({'requestRoomsSuccess': True, 'status': 'Success, Not logged in', 'rooms': all_rooms})
            else:
                all_rooms = get_all_rooms_info()
                return json.dumps({'requestRoomsSuccess': True, 'status': 'Success, Logged in', 'rooms': all_rooms})

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
                return json.dumps({'addFriendSuccess': False, 'status': 'Invalid token'})

            recipient = request["form"]["friend"]
            try:
                accept_request(sender, recipient)
                return json.dumps({'addFriendSuccess': True, 'status': 'Success, Logged in'})
            except:
                json.dumps({'addFriendSuccess': False, 'status': 'Could not accept friend'})

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
            duration = request["form"]["duration"]
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

        elif request["form"]["task"] == "updateOccupancy":
            try:
                room = request["form"]["roomNum"]
                occupancy = request["form"]["occupancy"]
                update_room_occupancy(room, occupancy)
                return json.dumps({'updateOccupancySuccess': True, 'status': None})
            except:
                return json.dumps({'updateOccupancySuccess': False, 'status': 'Could not update occupancy'})

        elif request["form"]["task"] == "updateNoiseLevel":
            try:
                room = request["form"]["roomNum"]
                noiseLevel = request["form"]["noiseLevel"]
                update_room_noiseLevel(room, noiseLevel)
                return json.dumps({'updateNoiseLevelSuccess': True, 'status': None})
            except:
                return json.dumps({'updateNoiseLevelSuccess': False, 'status': 'Could not update noise level'})

        else:
            return KeyError("Unknown POST request")

    else:
        return KeyError("Unknown GET/POST request")

if __name__ == '__main2__':
    # print("\n\nWeek 1")
    # me = User('Vittal', {'noise': Noise.loud})
    # print(me.upload())
    # print(repr(me))
    # print(me)
    # User.update_noise_pref('Vittal', Noise.moderate)
    # print(me)
    # print()
    #
    # Ricardo = User('Ricardo', {'noise': Noise.noPref})
    # print(Ricardo.upload())
    # print(User.get_user('Ricardo'))
    # print(User.update_noise_pref('Ricardo', Noise.quiet))
    # print(User.get_user('Ricardo'))
    # print(User.get_all_users())
    # print()
    #
    # try:
    #     me.upload()
    # except Exception as e:
    #     print(e)
    # print(User.get_user('Vittal'))
    # print(User.update_noise_pref('Vittal', Noise.loud))
    # print(User.get_user('Vittal'))
    # try:
    #     User.get_user('RandomUnknown')
    # except Exception as e:
    #     print(e)
    # print(User.get_all_users())

    print("\n\nWeek 2")
    # Creating rooms
    update_rooms()
    print(get_all_rooms_info())
    print(request_handler({"method":"GET", "values":{"task":"rooms"}}))

    # Creating account and updating preferences
    print(request_handler({"method": "POST", "form": {"user": "Vittal", "task": "create account", "noise": "loud"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "preferences"}}))
    print(request_handler({"method":"POST", "form":{"user":"Vittal", "task":"preferences", "noise":"quiet"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "preferences"}}))
    print(request_handler({"method":"POST", "form":{"user":"Vittal", "task":"preferences", "noise":"moderate"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "preferences"}}))
    print()

    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "preferences"}}))
    print(request_handler({"method": "GET", "values": {"user": "Vittal", "task": "friends"}}))
    print()

    print(request_handler({"method": "POST", "form": {"user": "Ricardo", "task": "create account", "noise": "quiet"}}))

    # Checkin and Checkout
    requests = [
        {"method": "POST", "form": {"user": "Vittal", "room": "1-115", "task": "checkin"}},
        {"method": "POST", "form": {"user": "Ricardo", "room": "1-134", "task": "checkin"}},
        {"method": "POST", "form": {"user": "Ricardo", "room": "1-134", "task": "checkout"}},
        {"method": "POST", "form": {"user": "Ricardo", "room": "1-115", "task": "checkin"}},
        {"method": "POST", "form": {"user": "Vittal", "room": "1-115", "task": "checkout"}},
        {"method": "POST", "form": {"user": "Ricardo", "room": "1-115", "task": "checkout"}},
    ]



    for request in requests:
        print(request)
        print(request_handler(request))
        for user in ['Vittal', 'Ricardo']:
            for task in ['rooms']:
                print(user, task)
                print(request_handler({"method": "GET", "values": {"user": user, "task": task}}))
        print()

    # Modifying friends
    requests = [
        {"method": "POST", "form": {"user": "Vittal", "friend": "Ricardo", "task": "request friend"}},
        {"method": "POST", "form": {"user": "Ricardo", "friend": "Vittal", "task": "accept friend"}},
        {"method": "POST", "form": {"user": "Ricardo", "friend": "Vittal", "task": "remove friend"}}
    ]

    for request in requests:
        print(request)
        print(request_handler(request))
        for user in ['Vittal', 'Ricardo']:
            for task in ['friends', 'friend requests']:
                print(user, task)
                print(request_handler({"method": "GET", "values": {"user": user, "task": task}}))
        print()