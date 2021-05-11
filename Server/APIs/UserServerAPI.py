import json
import sys, os
# sys.path.append(os.path.abspath(__file__))
os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Friends')
sys.path.append(server_path + '/Rooms')

from friends import *
from rooms import *

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
        if request["values"]["task"] == "loginpage":
            with open("../UI/Login/login.html") as f:
                body = f.read()
                return body
        elif request["values"]["task"] == "checkinpage":
            with open("../UI/Checkin/checkin.html") as f:
                body = f.read()
                return body
        elif request["values"]["task"] == "friendspage":
            with open("../UI/Friends/friends.html") as f:
                body = f.read()
                return body
        elif request["values"]["task"] == "dashboardpage":
            with open("../UI/Dashboard/dashboard.html") as f:
                body = f.read()
                return body
        elif request["values"]["task"] == "preferences":
            name = request["values"]["user"]
            return User.get_user(name)

        elif request["values"]["task"] == "friendswithrooms":
            name = request["values"]["user"]
            return json.dumps(get_friends_with_rooms(name))

        elif request["values"]["task"] == "friends":
            name = request["values"]["user"]
            return json.dumps(get_friends(name))

        elif request["values"]["task"] == "friendrequests":
            name = request["values"]["user"]
            return get_friend_requests(name)

        elif request["values"]["task"] == "rooms":
            update_rooms()
            all_rooms = get_all_rooms_info()
            return json.dumps(all_rooms)

        else:
            return KeyError("Unknown GET request")


    elif request["method"] == "POST":
        if request["form"]["task"] == "createaccount":
            # name = request["form"]["user"]
            # noise_pref = Noise.str_to_enum(request["form"]["noise"])
            # user = User(name, {'noise': noise_pref})
            # user.upload()
            with open("../UI/Dashboard/dashboard.html") as f:
                body = f.read()
                return body

        elif request["form"]["task"] == "login":
            with open("../UI/Dashboard/dashboard.html") as f:
                body = f.read()
                return body

        elif request["form"]["task"] == "preferences":
            name = request["form"]["user"]
            noise_pref = Noise.str_to_enum(request["form"]["noise"])
            return User.update_noise_pref(name, noise_pref)

        elif request["form"]["task"] == "requestfriend":
            sender = request["form"]["user"]
            recipient = request["form"]["friend"]
            return send_request(sender, recipient)

        elif request["form"]["task"] == "acceptfriend":
            sender = request["form"]["user"]
            recipient = request["form"]["friend"]
            return accept_request(sender, recipient)

        elif request["form"]["task"] == "removefriend":
            sender = request["form"]["user"]
            recipient = request["form"]["friend"]
            return remove_friend(sender, recipient)

        elif request["form"]["task"] == "checkin":
            update_rooms()
            name = request["form"]["user"]
            room = request["form"]["roomnum"]
            print(name, room)
            add_occupant(name, room)
            with open("../UI/Dashboard/dashboard.html") as f:
                body = f.read()
                return body

        elif request["form"]["task"] == "checkout":
            update_rooms()
            name = request["form"]["user"]
            room = request["form"]["roomnum"]
            print(name, room)
            return remove_occupant(name, room)

        elif request["form"]["task"] == "updaterooms":
            update_rooms()

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
    # Ricardo = User('Ricardo', {'noise': Noise.no_pref})
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