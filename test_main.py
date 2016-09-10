
import unittest

class MainTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_hello_world(self):
        text = "Hello world"
        assert text == "Hello world"

if __name__ == '__main__':
    unittest.main()
