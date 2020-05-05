"""Project-wide DateTime format string"""

import numpy as np


DT_STR = '%Y-%m-%dT%H:%M:%S'


def largest_indices(array, number):
    """Returns the "number" largest indices from a numpy array."""
    flat = array.flatten()
    indices = np.argpartition(flat, -number)[-number:]
    indices = indices[np.argsort(-flat[indices])]
    return np.unravel_index(indices, array.shape)


def is_valid_range(parser, arg, minimum=0, maximum=100):
    """
    This function checks wether a given argument is within the given range or
    not.
    """
    if arg < minimum:
        parser.error("%s < %s", arg, minimum)
    else:
        if arg > maximum:
            parser.error("%s > %s", arg, maximum)

    return arg


def chomp(string):
    """
    Simple callable method to remove additional newline characters at the end
    of a given string.
    """
    if string.endswith("\r\n"):
        return string[:-2]
    if string.endswith("\n"):
        return string[:-1]
    return string
