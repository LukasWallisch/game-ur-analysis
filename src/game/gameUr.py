import numpy as np

# from game.gameModelBlocking import GameModel
from src.game.Exceptions import UnknownModeError
from src.game import gameModel


class Ur(object):
    def __init__(self, dice_count=4, stones=7, players=2, prepare=2, fight=8, retreat=4 ,mode="blocking") -> None:
        if players >= 256:
            raise Exception("max players 255")
        if stones >= 256:
            raise Exception("max stones 255")
        self.dice_count = dice_count
        self.prepare = prepare
        self.fight = fight
        self.retreat = retreat
        self.stones = stones
        self.players = players
        
        self.currentround = 0
        self.step = 0

        # set game Model accordint to selection
        if mode == "blocking":
            self.gm = gameModel.GameModel(
                stones=stones, players=players, prepare=prepare, fight=fight, retreat=retreat)
        else:
            raise UnknownModeError(mode)


    
    
    def __str__(self):
        return "round: {currentround} step: {step}\n".format(currentround=self.currentround, step=self.step) + str(self.gm)

    def __repr__(self) -> str:
        return self.__str__()
    

