from lib.solutions.HLO import hello_solution


class TestHello():
    def test_hello(self):
        name = 'John'
        assert hello_solution.hello(name) == 'Hello, {}!'.format(name)
    
