import unittest

from seedRandom import DerivableRandom

class TestDerivableRandom(unittest.TestCase):

    def test_fromString(self):
        # Arrange
        state = "1.123.10"

        expected_seed = 0x123
        expected_steps = 10

        # Act
        result = DerivableRandom.fromString(state)

        # Assert
        self.assertEqual(result.seed, expected_seed)
        self.assertEqual(result.steps, expected_steps)

    def test_toString(self):
        # Arrange
        seed = 0x123
        steps = 10
        version = 1

        expected_state = "1.123.10"

        # Act
        generator = DerivableRandom(seed, steps, version)
        result = generator.toString()

        # Assert
        self.assertEqual(result, expected_state)

if __name__ == "__main__":
    unittest.main()
