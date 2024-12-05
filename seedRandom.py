# Its a nice idea to be able to play the same game again
# This is particularly useful for debugging and testing

# As the game uses randomness, to duplicate a game we need to
# know what random "seed" the game started with, and have a
# way to set the random number generator to that seed when
# we want to replay the game.

# That in itself is sufficient to play the exact game again
# in the same way. However, if we want to play the game again
# with the same seed, but with different user behaviour, but
# still have the same random choices, we need to be able to
# use multiple random number generators.

# So ideally, we would have two things:
# 1. A way to save and restore the state of a random number generator easily
#    in our application
# 2. A way to create a new random number generator that is derived from the
#    state of an existing random number generator

# on 1.
#
# Unfortunately the implementation of random is very complex,
# and the state of a random module is very large (624(?) 64-bit integers).
# This makes it difficult to store the state of a random number generator
# in a way that can be easily saved and restored.
#
# An alternative approach is to use a restricted set of seeds that can be
# stored easily, alongside a number of times the underlying merseinne twister
# has been called. This would allow the recreation of a random number
# generator with the same state as when it was saved.

# on 2.
#
# The unstated restrictions to child generators are:
# - They must not change the state of the parent generator
# - Multiple child generators can be created from the same parent generator and
#   they will all be independent of each other with different initial states
#
# A simple way to do this is to create new rngs by advancing the parent rng 
# but storing and replaying the results in subsequent calls to the random method.

# Both 1 and 2 fall down when it is revealed there is not one "pure" method to
# advance the merseinne twister. The underlying source code is:
# https://github.com/python/cpython/blob/main/Modules/_randommodule.c
# Here 

# random() : 1
# getrandbits(k) : K
# 

import _random

class _PeekingCountingRandom(_random.Random):
    """
    A subclass of the random.Random class that
    - tracks the number of times the random number generator has been called
    - allows peeking at the next random number
    - allows peeking at the next random number that hasn't been peeked at yet
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steps = 0
        self.peekdistance = 0

    def random(self):
        self.steps += 1
        self.peekdistance = max(0, self.peekdistance - 1)
        return super().random()
    
    def getrandbits(self, k):
        if k > 0:
            words = (k // 32) + 1
            self.steps += words
            self.peekdistance = max(0, self.peekdistance - words)
        return super().getrandbits(k)
    
    def peek(self):
        """
        Peek at the next random number
        """
        peekrng = _random.Random()
        peekrng.setstate(self.getstate())

        peeked = peekrng.random()

        return peeked

    def peek_unpeeked(self):
        """
        Peek at the next random number that hasn't been peeked at yet without advancing the random number generator
        """
        peekrng = _random.Random()
        peekrng.setstate(self.getstate())

        # This is quite a hack, but it works on the assumption that the
        # rng self will advance much faster than the peekrng and so
        # peekdistance will always be very small or nothing
        peekrng.advance(self.peekdistance)

        peeked = peekrng.random()
        self.peekdistance += 1

        return peeked

    def advance(self, steps):
        """
        Advance the random number generator by a number of steps
        Used to recreate the state of the random number generator
        """
        for _ in range(steps):
            self.random()

# Create a subclass of _PeekingCountingRandom that is the same as the random.Random class
import random
PeekingCountingRandom = type("PeekingCountingRandom", (_PeekingCountingRandom,), dict(random.Random.__dict__))

class DerivableRandom(PeekingCountingRandom):
    """
    A subclass of the random.Random class that can create child random number generators

    It also supports saving and restoring the state of the random number generator using a custom string representation
    """

    def __init__(self, seed: int | float, steps: int = 0, version: int = 1):
        super().__init__()

        # Check that the version is supported
        if version != 1:
            raise ValueError(f"Unknown version of DerivableRandom '{version}' specified")
        
        super().__init__(seed)
        self.seed = seed
        self.version = version
        self.advance(steps)

    @staticmethod
    def fromString(state: str):
        """
        Create a RandomGenerator from a custom string representation

        Generate the custom string representation using the toString() method
        """

        # Split the state into its components
        version, seed_b64, steps = state.split(".")
        
        # Parse the state components
        version = int(version, 16)
        seed = int(seed_b64, 16)
        steps = int(steps)

        # Create the RandomGenerator
        generator = DerivableRandom(seed, steps, version)

        return generator
    
    def toString(self):
        """
        Create a custom string representation of the RandomGenerator that can
        be used to recreate the RandomGenerator using the fromString() method
        """
        return f"{self.version}.{self.seed:x}.{self.steps}"

    def __str__(self):
        return f"RandomGenerator(seed={self.seed}, steps={self.steps}, version={self.version})"

    def child(self):
        """
        Create a new RandomGenerator that is derived from the state of this random number generator
        """
        next_seed = self.peek_unpeeked()
        child = DerivableRandom(next_seed, 0, self.version)
        return child
    
