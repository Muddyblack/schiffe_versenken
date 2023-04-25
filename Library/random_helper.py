"""Functions that expand the functionalitie of the random library"""

import random


def randint_exc(start, end, *exception):
    """Choosing random integers except for a particular number"""
    res = random.randint(start, end)
    if res not in exception:
        return res

    return randint_exc(start, end, *exception)
