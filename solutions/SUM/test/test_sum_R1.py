import unittest
from solutions.SUM import sum_solution

class TESTSUM(unittest.TestCase):

    def test_sum_2_integer(self):
        self.assertEqual(sum_solution.compute(1,1), 2)


if __name__ == "__main__":
    unittest.main()