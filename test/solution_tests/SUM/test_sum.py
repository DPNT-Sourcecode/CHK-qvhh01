import unittest
from solutions.SUM import sum_solution


class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum_solution.sum(1, 2), 3)
    
    def test_sum_out_of_range(self):
        self.assertIsNone(sum_solution.sum(101, 2)) 



if __name__ == "__main__":
    unittest.main()