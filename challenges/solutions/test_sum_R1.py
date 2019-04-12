import unittest
from sum_r1 import sumr1

class TESTSUM(unittest.TestCase):

    def test_sum_2_integer(self):
        self.assertEqual(sumr1(1,1), 2)


if __name__ == "__main__":
    unittest.main()