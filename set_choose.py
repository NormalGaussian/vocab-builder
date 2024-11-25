import random
from typing import TypeVar, Set
T = TypeVar('T')

def setChoice(s: Set[T]) -> T | None:
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
