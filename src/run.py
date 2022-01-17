from json import encoder
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random
import json
import numpy as np
from datetime import datetime

from gameSimulation.GameUr import GameUr, Player, Dice, GameSettings
import gameSimulation.Strategies as S
import gameSimulation.Multirun as Multirun
import gameSimulation.jsonDeEncoders as jsonDE


if __name__ == "__main__":
    equalSettings = [Dice.MultiD2Dice(4),4, 8, 2, [8], [4, 8, 14]]
    p0 = Player(0, 7, S.RandomStrategy())

    gs = [
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.MultiD2Dice(4), *equalSettings)]*10,
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.MultiD2Dice(3), *equalSettings)]*10,
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.MultiD2DiceNo0(3), *equalSettings)]*10,
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.D4(), *equalSettings)]*10,

        # *[GameSettings([p0, Player( 1, 7, S.RandomStrategy())],  *equalSettings)]*5,
        # *[GameSettings([p0, Player( 1, 7, S.MoveFirstStrategy())], *equalSettings)]*5,
        # *[GameSettings([p0, Player( 1, 7, S.MoveLastStrategy())], *equalSettings)]*5,
        # *[GameSettings([p0, Player( 1, 7, S.ScoreStrategy())], *equalSettings)]*5,
        # *[GameSettings([p0, Player( 1, 7, S.ScoreDoubleRollStrategy())], *equalSettings)]*5,
        # *[GameSettings([p0, Player( 1, 7, S.ScoreThrowOpponentStrategy())], *equalSettings)]*5,

        *[GameSettings([Player( 1, 1, S.RandomStrategy())],  *equalSettings)]*(420//1),
        *[GameSettings([Player( 1, 2, S.RandomStrategy())],  *equalSettings)]*(420//2),
        *[GameSettings([Player( 1, 3, S.RandomStrategy())],  *equalSettings)]*(420//3),
        *[GameSettings([Player( 1, 4, S.RandomStrategy())],  *equalSettings)]*(420//4),
        *[GameSettings([Player( 1, 5, S.RandomStrategy())],  *equalSettings)]*(420//5),
        *[GameSettings([Player( 1, 6, S.RandomStrategy())],  *equalSettings)]*(420//6),
        *[GameSettings([Player( 1, 7, S.RandomStrategy())],  *equalSettings)]*(420//7),

        # *[GameSettings([Player( 1, 2, S.RandomStrategy())],  *equalSettings)]*5,
        # *[GameSettings([Player( 1, 2, S.MoveFirstStrategy())], *equalSettings)]*5,
        # *[GameSettings([Player( 1, 2, S.MoveLastStrategy())], *equalSettings)]*5,
        # *[GameSettings([Player( 1, 2, S.ScoreStrategy())], *equalSettings)]*5,
        # *[GameSettings([Player( 1, 2, S.ScoreDoubleRollStrategy())], *equalSettings)]*5,
        # *[GameSettings([Player( 1, 2, S.ScoreThrowOpponentStrategy())], *equalSettings)]*5,
    ]
    gs_fastest = [
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.MultiD2Dice(4), *equalSettings)]*10,
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.MultiD2Dice(3), *equalSettings)]*10,
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.MultiD2DiceNo0(3), *equalSettings)]*10,
        # *[GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(1, 7, S.MoveFirstStrategy())], Dice.D4(), *equalSettings)]*10,

        # (GameSettings([p0, Player( 1, 7, S.RandomStrategy())],  *equalSettings),50),
        # (GameSettings([p0, Player( 1, 7, S.MoveFirstStrategy())], *equalSettings),50),
        # (GameSettings([p0, Player( 1, 7, S.MoveLastStrategy())], *equalSettings),50),
        # (GameSettings([p0, Player( 1, 7, S.ScoreStrategy())], *equalSettings),50),
        # (GameSettings([p0, Player( 1, 7, S.ScoreDoubleRollStrategy())], *equalSettings),50),
        # (GameSettings([p0, Player( 1, 7, S.ScoreThrowOpponentStrategy())], *equalSettings),50),
        # (GameSettings([p0], *equalSettings),20),
    ]
    runs = 25000


    delta0 = datetime.now()
    # cf = Multirun.multirunDB(runs,-1, 500, gs)
    cf = Multirun.multirunDB(runs,10, 100, gs,"baseline")


    #5000 [03:37<00:00, 229.91games/s]
    #5000 [03:46<00:00, 220.46games/s]

    delta1 = datetime.now()
    print("{} chunks finished after {}".format(cf, delta1-delta0))

    # h=[]
    # h.append(Multirun.runGame(gs[0],True))

    # id = 4
    # for i, h_sub in enumerate(h):
    #     delta0 = datetime.now()
    #     print("start save at ", delta0)
    #     with open("G:/Uni/BA/data/history_data_{:02d}_{:02d}.json".format(id,i), "w") as f:
    #         json.dump(h[i], f, cls=jsonDE.PlayerEncoder, indent=4)
    #     delta1 = datetime.now()
    #     print("finished save after", delta1-delta0)

    # for h_sub in h:
    #     store_data_2_db(h_sub)

    # tmp = []
    # for i in range(3):
    #     delta0 = datetime.now()
    #     with open("data/history_data_{:02d}.json".format(i), "r") as f:
    #         tmp.append(json.load(f))
    #     delta1 = datetime.now()
    #     print("finished load after", delta1-delta0)
