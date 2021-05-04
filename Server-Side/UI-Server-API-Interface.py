from users_and_rooms.py import send_request

# WEEK 2 Deliverable - request handler

def request_handler(request):
	'''
	Function executes get and post requests by interfacing with other functions that have been written.
	Checks that the inputs provided are valid, and, if they are, returns the correct outputs
	GET requests to get rooms, friend data or preferences
	POST request to pref, checkin, login, addfriend, requestfriend, delfriend
	GET rooms: provide login (logged in status), user
	GET pref: provide user
	GET friends: provide user
	POST pref: provide user, noiselvl
	POST checkin: provide user, room, (opt) noiselvl
	POST login: to be figured out using google - will be integrated and updated later
	POST addfriend: provide user, friend
	POST requestfriend: provide user, friend
	POST delfriend: provide user, friend
	'''
	if request["method"] == "GET":
		if request["values"]["task"]=="rooms":
			#TODO pending Riccardo's code
			pass
		elif request["values"]["task"] == "pref":
			try:
				return get_account(request["values"]["user"])
			except:
				return "Invalid user"
		elif request["values"]["task"] == "friends":
			try:
				get_account(request["values"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
			

	if request["method"] == "POST":
		if request["form"]["task"] == "pref":
			try:
				if request["form"]["noiselvl"] == "quiet":
					try:
						update_noise_pref(request["form"]["user"], Noise.quiet)
					except:
						return "Invalid user"
				elif request["form"]["noiselvl"] == "loud":
					try:
						update_noise_pref(request["form"]["user"], Noise.loud)
					except:
						return "Invalid user"
				else:
					return "Invalid noise level"
			except:
				return "Invalid input"
			return get_account(request["form"]["user"])
		if request["form"]["task"] == "checkin":
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when rooms data base is accessible
				# Check if room is in the database TODO
				# If noiselvl is invalid, ignore it
				noise = 0; # 0 is no pref, 1 is quiet, 2 is loud
				if request["form"]["noiselvl"] == "quiet":
					noise = 1
				elif request["form"]["noiselvl"] == "loud":
					noise = 2
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if request["form"]["task"] == "login":
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when login figured out
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if request["form"]["task"] == "addfriend":
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				get_account(request["form"]["friend"])
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if request["form"]["task"] == "requestfriend":
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				get_account(request["form"]["friend"])
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if request["form"]["task"] == "delfriend":
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				get_account(request["form"]["friend"])
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"

# def getrooms(request):
# 	'''
# 	Returns a dictionary of the rooms, their current/max occupancy, noise levels, etc. (all the data we store about the room)
# 	'''
# 	pass

# def getfriends(request):


if __name__ == '__main__':
	me = User('Vittal', {'noise' : Noise.loud})
	create_account(me)
	print (request_handler({"method":"GET", "values":{"user":"Vittal", "task":"pref"}}))
	print (request_handler({"method":"GET", "values":{"user":"Vittal", "task":"friends"}}))
	print (request_handler({"method":"GET", "values":{"user":"Vittal", "task":"rooms"}})) #TODO

	print (request_handler({"method":"POST", "form":{"user":"Vittal", "task":"pref", "noiselvl":"quiet"}}))
	print (request_handler({"method":"POST", "form":{"user":"Vittal", "task":"pref", "noiselvl":"happy"}}))

