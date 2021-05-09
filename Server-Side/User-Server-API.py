from users import *
from rooms import *
from friends import *

# change this
database = "database.db"

def request_handler(request):
    '''
	Function executes get and post requests by interfacing with other functions that have been written.
	Checks that the inputs provided are valid, and, if they are, returns the correct outputs
	GET requests to get login page, user preferences, friends, friend requests, and rooms data
	POST request to login, update preferences, request_friend, accept_friend, remove_friend, and checkin

    #TODO: GET login: to be figured out using google - will be integrated and updated later
	GET pref: provide user
	GET friends: provide user
	GET friend_requests: provide user
	GET rooms: provide all rooms, capacities, num_occupies, and checkin option

	#TODO: POST login: to be figured out using google - will be integrated and updated later
	POST pref: provide user, noise
	POST request_friend: provide user, friend
	POST accept_friend: provide user, friend
	POST remove_friend: provide user, friend
	#TODO: POST checkin: provide user, room, (opt) noise
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
                return User.get_user(name)

            elif request["values"]["task"] == "friend_requests":
                name = request["values"]["user"]
                return get_friend_requests(name)

            elif request["values"]["task"] == "friends":
                name = request["values"]["user"]
                return get_friends(name)


        elif request["method"] == "POST":
            if request["form"]["task"] == "create_account":
                name = request["values"]["user"]
                noise_pref = Noise.str_to_enum(request["form"]["noise"])
                user = User(name, {'noise': noise_pref})
                user.upload()

            elif request["form"]["task"] == "pref":
                name = request["form"]["user"]
                noise_pref = Noise.str_to_enum(request["form"]["noise"])
                return User.update_noise_pref(name, noise_pref)

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
                user = User.get_user(name)
                room = request["form"]["room"]
                print(user, room)
                return add_occupant(room, user)

            elif request["form"]["task"] == "login": #TODO
                user = User.get_user(request["form"]["user"])
                return "Code to be called not yet complete. Input valid."
    except Exception as e:
        return e

if __name__ == '__main__':
    print("\n\nWeek 1")
    me = User('Vittal', {'noise': Noise.loud})
    print(me.upload())
    print(repr(me))
    print(me)
    User.update_noise_pref('Vittal', Noise.moderate)
    print(me)
    print()

    Ricardo = User('Ricardo', {'noise': Noise.no_pref})
    print(Ricardo.upload())
    print(User.get_user('Ricardo'))
    print(User.update_noise_pref('Ricardo', Noise.quiet))
    print(User.get_user('Ricardo'))
    print(User.get_all_users())
    print()

    try:
        me.upload()
    except Exception as e:
        print(e)
    print(User.get_user('Vittal'))
    print(User.update_noise_pref('Vittal', Noise.loud))
    print(User.get_user('Vittal'))
    try:
        User.get_user('RandomUnknown')
    except Exception as e:
        print(e)
    print(User.get_all_users())

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

