# Ctrl-F WEEK 2 Deliverable - request handler for week 2 updates

import sqlite3
from bs4 import BeautifulSoup
import datetime
from enum import Enum

accounts_server = 'accounts.py'
accounts_db = 'accounts_data.db'
#accounts_db = '/var/jail/home/vittalt/FinalProject/accounts_data.db'

with sqlite3.connect(accounts_db) as c:
	c.execute('''CREATE TABLE IF NOT EXISTS accounts_db (username text, noise_pref integer);''')


class Noise(Enum):
	no_pref = 0
	quiet = 1
	moderate = 2
	loud = 3

	def str_form(type):
		if type == Noise.no_pref:
			return 'has no noise preference'
		elif type == Noise.quiet:
			return 'prefers quiet noise levels'
		elif type == Noise.moderate:
			return 'prefers moderate noise levels'
		elif type == Noise.loud:
			return 'prefers loud noise levels'
		else:
			return 'has an unknown preference'


class User:
	def __init__(self, name="anonymous", prefs = None):
		self.name = name
		if prefs is None:
			prefs = {'noise' : Noise.no_pref}
		self.prefs = prefs

	def __repr__(self):
		return f"User(\'{self.name}\', {{'noise' : {self.prefs['noise']}}})"

	def __str__(self):
		return f"{self.name} {Noise.str_form(self.prefs['noise'])}."

	def update_name(self, new_name):
		self.name = new_name

	def update_prefs(self, new_prefs):
		self.prefs = new_prefs

	def update_noise_pref(self, new_noise_pref):
		self.prefs['noise'] = new_noise_pref

	def get_name(self):
		return self.name

	def get_prefs(self):
		return self.prefs

	def get_noise_pref(self):
		return self.get_prefs()['noise']


def user_to_db(user):
	return user.get_name(), user.get_noise_pref().value

def db_to_user(db_entry):
	name, noise_pref_id = db_entry
	return User(name, {'noise' : Noise(noise_pref_id)})


def user_in_db(c, user):
	return username_in_db(c, user_to_db(user)[0])

def username_in_db(c, username):
	return c.execute('''SELECT EXISTS (SELECT 1 FROM accounts_db WHERE username = ?);''', (username,)).fetchone()[0]


def create_account(user):
	with sqlite3.connect(accounts_db) as c:
		if user_in_db(c, user):
			return f'Account {user.get_name()} already exists!'
		else:
			c.execute('''INSERT INTO accounts_db VALUES (?, ?);''', user_to_db(user))
			return f'Account {user.get_name()} created.'

def create_user_account(username, noise_pref):
	return create_account(db_to_user((username, noise_pref)))


def update_prefs(user):
	with sqlite3.connect(accounts_db) as c:
		if user_in_db(c, user):
			c.execute('''UPDATE accounts_db SET noise_pref = ? WHERE username = ?;''', user_to_db(user)[::-1])
			return f'Account {user.get_name()} updated.'
		else:
			return f'Account {user.get_name()} does not exist!'

def update_noise_pref(username, noise_pref):
	return update_prefs(db_to_user((username, noise_pref)))


def get_account(username):
	with sqlite3.connect(accounts_db) as c:
		if username_in_db(c, username):
			return db_to_user(c.execute('''SELECT * FROM accounts_db WHERE username = ?''', (username,)).fetchone())
		else:
			return f'Account {username} does not exist!'

def get_all_accounts():
	with sqlite3.connect(accounts_db) as c:
		return [db_to_user(db_entry) for db_entry in c.execute('''SELECT * FROM accounts_db''').fetchall()]


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
	if (request["method"] == "GET"):
		if (request["values"]["task"]=="rooms"):
			#TODO pending Riccardo's code
			pass
		if (request["values"]["task"] == "pref"):
			try:
				return get_account(request["values"]["user"])
			except:
				return "Invalid user"
		if (request["values"]["task"] == "friends"):
			try:
				get_account(request["values"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
			

	if (request["method"] == "POST"):
		if (request["form"]["task"] == "pref"):
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
		if (request["form"]["task"] == "checkin"):
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
		if (request["form"]["task"] == "login"):
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when login figured out
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if (request["form"]["task"] == "addfriend"):
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				get_account(request["form"]["friend"])
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if (request["form"]["task"] == "requestfriend"):
			try:
				get_account(request["form"]["user"]) #TODO change this to correct code when the friends database and surrounding functionality is complete
				get_account(request["form"]["friend"])
				return "Code to be called not yet complete. Input valid."
			except:
				return "Invalid user"
		if (request["form"]["task"] == "delfriend"):
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

