import json
import sys, os

os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Preferences')
sys.path.append(server_path + '/Rooms')

from noise import *
from rooms import *

database = '../database.db'

def request_handler(request):
    """
	Function that executes GET and POST requests from the ESP32, by interfacing with functions from noise and rooms.py.
	Checks that the inputs provided are valid, and, if they are, updates the database and returns the correct outputs.
	POST: updateOccupancy, updateNoiseLevel

	POST
	- updateOccupancy: roomNum, occupancy
        - Returns:
        { updateOccupancySuccess: bool, status: string }
    - updateNoiseLevel: roomNum, noiseLevel
        - Returns:
        { updateNoiseLevelSuccess: bool, status: string }
    """

    if request["method"] == "POST":
        if request["form"]["task"] == "updateOccupancy":
            try:
                room = request["form"]["roomNum"]
                occupancy_additional = int(request["form"]["occupancy"])
                increment_room_occupancy(room, occupancy_additional)
                return json.dumps({'updateOccupancySuccess': True, 'status': None})
            except:
                return json.dumps({'updateOccupancySuccess': False, 'status': 'Could not update occupancy'})

        elif request["form"]["task"] == "updateNoiseLevel":
            try:
                room = request["form"]["roomNum"]
                rawNoiseLevel = float(request["form"]["noiseLevel"])
                noiseLevel = raw_noise_to_enum(rawNoiseLevel)
                update_room_noiseLevel(room, noiseLevel)
                return json.dumps({'updateNoiseLevelSuccess': True, 'status': None})
            except:
                return json.dumps({'updateNoiseLevelSuccess': False, 'status': 'Could not update noise level'})

        else:
            return KeyError("Unknown POST request")

    else:
        return KeyError("Unknown GET/POST request")

QUIET_MODERATE_CUTOFF = 700
MODERATE_HIGH_CUTOFF = 1200
def raw_noise_to_enum(rawNoiseLevel):
    noisePref = 5
    if rawNoiseLevel < QUIET_MODERATE_CUTOFF:
        noisePref = 1
    elif rawNoiseLevel >= MODERATE_HIGH_CUTOFF:
        noisePref = 3
    else:
        noisePref = 2
    return Noise(noisePref)

if __name__ == '__main2__':
    pass