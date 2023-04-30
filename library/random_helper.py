"""Functions that expand the functionalities of the random library"""

import random


def randint_exc(start, end, *exception):
    """Choosing random integers except for particular numbers"""
    res = random.randint(start, end)
    if res not in exception:
        return res

    return randint_exc(start, end, *exception)
