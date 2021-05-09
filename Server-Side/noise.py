from enum import Enum


class Noise(Enum):
    no_pref = 0
    quiet = 1
    moderate = 2
    loud = 3

    def str_form(self):
        if self == Noise.no_pref:
            return 'has no noise preference'
        elif self == Noise.quiet:
            return 'prefers quiet noise levels'
        elif self == Noise.moderate:
            return 'prefers moderate noise levels'
        elif self == Noise.loud:
            return 'prefers loud noise levels'
        else:
            return 'has an unknown preference'

    @staticmethod
    def str_to_enum(noise):
        if noise == 'no_pref':
            return Noise.no_pref
        elif noise == 'quiet':
            return Noise.quiet
        elif noise == 'moderate':
            return Noise.moderate
        elif noise == 'loud':
            return Noise.loud