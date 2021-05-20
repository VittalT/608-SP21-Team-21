import json
import sys, os
# sys.path.append(os.path.abspath(__file__))
os.chdir('/var/jail/home/team21/Server')
server_path = '/var/jail/home/team21/Server'
sys.path.append(server_path)
sys.path.append(server_path + '/Preferences')
sys.path.append(server_path + '/Rooms')

from noise import *
from rooms import *

database = '../database.db'

def request_handler(request):
    if request["method"] == "POST":
        if request["form"]["task"] == "updateOccupancy":
            # try:
            room = request["form"]["roomNum"]
            occupancy_additional = int(request["form"]["occupancy"])
            update_room_occupancy(room, occupancy_additional)
            return json.dumps({'updateOccupancySuccess': True, 'status': None})
            # except:
            #     return json.dumps({'updateOccupancySuccess': False, 'status': 'Could not update occupancy'})

        elif request["form"]["task"] == "updateNoiseLevel":
            # try:
            room = request["form"]["roomNum"]
            rawNoiseLevel = float(request["form"]["noiseLevel"])
            noiseLevel = raw_noise_to_enum(rawNoiseLevel)
            update_room_noiseLevel(room, noiseLevel)
            return json.dumps({'updateNoiseLevelSuccess': True, 'status': None})
            # except:
            #     return json.dumps({'updateNoiseLevelSuccess': False, 'status': 'Could not update noise level'})

        else:
            return KeyError("Unknown POST request")

    else:
        return KeyError("Unknown GET/POST request")

QUIET_MODERATE_CUTOFF = 30
MODERATE_HIGH_CUTOFF = 70
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