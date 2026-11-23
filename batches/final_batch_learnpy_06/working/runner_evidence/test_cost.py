import unittest
from helper import cost

class CostTests(unittest.TestCase):
    def test_cost(self):
        self.assertEqual(cost(3), 12)
