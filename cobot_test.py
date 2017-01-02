import unittest
import cobot

class test_cobot(unittest.TestCase):
    def test_listen(self):
        @cobot.listen(r'something')
        def some_func():
            if True:
                pass
        self.assertNotEqual(cobot.handlers, dict())
