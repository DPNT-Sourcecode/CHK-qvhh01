from lib.solutions.HLO import hello_solution


class TestHello():
    def test_hello(self):
        name = 'Yaya'
        assert hello_solution.hello(name) == 'Hello I am {}'.format(name)
    
