from enum import Enum

class Noise(Enum):
    quiet = 1
    moderate = 2
    loud = 3
    noPref = 4
    unknown = 5

    def str_form(self):
        """
        Converts a Noise enum to its associated string representation.
        """
        if self == Noise.quiet:
            return 'quiet'
        elif self == Noise.moderate:
            return 'moderate'
        elif self == Noise.loud:
            return 'loud'
        elif self == Noise.noPref:
            return 'none'
        else:
            return 'unknown'

    @staticmethod
    def str_to_enum(noise):
        """
        Converts a noise string representation into its associated Noise enum.
        """
        if noise == 'quiet':
            return Noise.quiet
        elif noise == 'moderate':
            return Noise.moderate
        elif noise == 'loud':
            return Noise.loud
        if noise == 'none':
            return Noise.noPref
        else:
            return Noise.unknown