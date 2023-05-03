"""Functions that expand the functionalities of the random library"""

import random


def randint_exc(start, end, *exception):
    """Choosing random integers except for particular numbers"""
    if len(exception) >= end - start + 1:
        return None

    res = random.randint(start, end)
    if res not in exception:
        return res

    return randint_exc(start, end, *exception)
