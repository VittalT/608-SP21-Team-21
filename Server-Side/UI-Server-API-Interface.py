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
	#TODO: GET login: to be figured out using google - will be integrated and updated later

	POST pref: provide user, noise
	POST requestfriend: provide user, friend
	POST acceptfriend: provide user, friend
	POST removefriend: provide user, friend
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

			elif request["values"]["task"] == "friends":
				name = request["values"]["user"]
				return get_friends(name)

			elif request["values"]["task"] == "login": #TODO
				name = request["values"]["user"]
				return "Code to be called not yet complete. Input valid."


		elif request["method"] == "POST":
			if request["form"]["task"] == "pref":
				name = request["values"]["user"]
				noise_pref = str_to_enum(request["form"]["noise"])
				return update_noise_pref(name, noise_pref)

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

			elif request["form"]["task"] == "checkin": #TODO
				name = request["form"]["user"]
				# Check if room is in the database TODO
				# If noise is invalid, ignore it
				return "Code to be called not yet complete. Input valid."

			elif request["form"]["task"] == "login": #TODO
				User = get_user(request["form"]["user"])
				return "Code to be called not yet complete. Input valid."
	except Exception as e:
		return e

if __name__ == '__main__':
	me = User('Vittal', {'noise' : Noise.loud})
	me.upload()
	print (request_handler({"method":"GET", "values":{"user":"Vittal", "task":"pref"}}))
	print (request_handler({"method":"GET", "values":{"user":"Vittal", "task":"friends"}}))
	print (request_handler({"method":"GET", "values":{"user":"Vittal", "task":"rooms"}})) #TODO

	print (request_handler({"method":"POST", "form":{"user":"Vittal", "task":"pref", "noise":"quiet"}}))
	print (request_handler({"method":"POST", "form":{"user":"Vittal", "task":"pref", "noise":"happy"}}))

