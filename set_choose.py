import random
from typing import TypeVar, Set
T = TypeVar('T')


#To note - the index reference is not constant
#due to set
def setChoice(s: Set[T]) -> T | None:
    """
    Chooses a single element at random from a set.
    When given the empty set returns None.
    When given a non-empty set always returns a value.
    """
    if len(s) == 0:
        return None
    index = random.randint(0, len(s) - 1)
    p = 0
    for i in s:
        if p == index:
            return i
        p += 1
    return ValueError("Selected index not found in set; this should never happen")

def setChooseN(s: Set[T], n: int) -> Set[T]:
    if len(s) <= n:
        return set(s)
    available = set(s)
    result = set()
    while len(result) < n:
        choice = setChoice(available)
        result.add(choice)
        available.remove(choice)
    return result