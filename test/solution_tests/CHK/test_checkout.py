from lib.solutions.CHK import checkout_solution


class TestSum():
    def test_should_return_total(self):
        assert checkout_solution.compute(1, 2) == 3