from enum import Enum

import sys, os
# print(os.path.dirname(os.path.abspath('')))

def request_handler(request):
    return os.path.dirname(os.path.abspath(os.getcwd()))

class Noise(Enum):
    quiet = 1
    moderate = 2
    loud = 3
    noPref = 4
    unknown = 5

    def str_form(self):
        if self == Noise.quiet:
            return 'quiet'
        elif self == Noise.moderate:
            return 'moderate'
        elif self == Noise.loud:
            return 'loud'
        elif self == Noise.noPref:
            return 'noPref'
        else:
            return 'unknown'

    @staticmethod
    def str_to_enum(noise):
        if noise == 'quiet':
            return Noise.quiet
        elif noise == 'moderate':
            return Noise.moderate
        elif noise == 'loud':
            return Noise.loud
        if noise == 'noPref':
            return Noise.noPref
        else:
            return Noise.unknown