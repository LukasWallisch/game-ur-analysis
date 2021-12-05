import sys
import os
print(sys.path)
print(os.getcwd())
import Player as P
import src.gameSimulation.GameUr as GameUr
from src.gameSimulation.Dice import MultiD2
from src.gameSimulation.GameSettings import GameSettings
from src.gameSimulation.Strategies import StrategyRandom

if __name__ == "__main__":

    dice = MultiD2(4)
    s = StrategyRandom()
    p1 = P.Player(0, 7, s)
    p2 = P.Player(1, 7, s)

    print(repr(p1))
    print(p1.getStrategy())
    gs = GameSettings([p1, p2], dice, 4, 8, 2, [8], [1, 8, 14])
    ur = GameUr.GameUr(gs)
    ur.tmp()
    print(ur)
