import unittest
from game import gameUr
from game import Exceptions

# from src.gameUr import Ur

# class  Test_PossibleMoves(unittest.TestCase):
class  Test_StringRepresentation(unittest.TestCase):
    def test_default_settings_str(self):
        test_string="round: 0 step: 0\n"
        test_string+="start: p0: 7, p1: 7\n"
        test_string+="00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00\n"
        test_string+="end: p0: 0, p1: 0"
        ur = gameUr.Ur()
        self.assertEqual(str(ur),test_string)

class Test_Errors(unittest.TestCase):
    def test_ModeError_negativ_Case(self):
        self.assertRaises(Exceptions.UnknownModeError, gameUr.Ur,mode="nope")
    def test_ModeError_positiv_Case(self):
        gameUr.Ur(mode="blocking")


# class Test_PossibleMoves(unittest.TestCase):
#     def setUp(self):
#         self.ur = gameUr.Ur()
#     def test_default_settings_start_combis(self):
#         for move_dist in range(5):
#             self.assertEqual(self.ur.calcPossibleMoves(0,move_dist),[-1])
#             self.assertEqual(self.ur.calcPossibleMoves(1,move_dist),[-1])