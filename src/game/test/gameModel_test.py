import unittest

from game import gameModelBlocking

# from src.gameUr import Ur

# class  Test_PossibleMoves(unittest.TestCase):
class  Test_ModelStringRepresentation(unittest.TestCase):
    def test_default_settings_str(self):
        test_string="start: p0: 7, p1: 7\n"
        test_string+="00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00\n"
        test_string+="end: p0: 0, p1: 0"
        model = gameModelBlocking.GameModel()
        self.assertEqual(str(model),test_string)


# class Test_PossibleMoves(unittest.TestCase):
#     def setUp(self):
#         self.ur = gameUr.Ur()
#     def test_default_settings_start_combis(self):
#         for move_dist in range(5):
#             self.assertEqual(self.ur.calcPossibleMoves(0,move_dist),[-1])
#             self.assertEqual(self.ur.calcPossibleMoves(1,move_dist),[-1])