import unittest
from LearningAlgos import *

class TestStringMethods(unittest.TestCase):

    def test_action_array(self):
        env = Environment(10)
        self.assertEqual(env.get_num_arms(), 10)

        env.list[0] = 1.0; #change the first probability to 1
        self.assertEqual(env.intract(1), 1)
        self.assertEqual(env.intract(1), 1)
        self.assertEqual(env.intract(1), 1)

        env.list[2] = 0;  # change the first probability to 1
        self.assertEqual(env.intract(3), 0)
        self.assertEqual(env.intract(3), 0)
        self.assertEqual(env.intract(3), 0)

if __name__ == '__main__':
    unittest.main()