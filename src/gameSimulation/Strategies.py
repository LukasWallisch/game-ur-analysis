from __future__ import annotations
import random
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.gameSimulation.Player import Player

from src.gameSimulation.gameboard.Gameboard import Gameboard, MoveTuple


class Strategy(object):
    def __init__(self) -> None:
        super().__init__()

    def getName(self) ->str:
        self.__name

    def chooseMove(self,player:Player, diceRoll:int, gb:Gameboard)->MoveTuple:
        raise NotImplementedError("this is just the interface")
    
    def __repr__(self) -> str:
        return self.getName()

class RandomStrategy(object):
    def __init__(self) -> None:
        self.__name = "random"
        super().__init__()
    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            return random.choice(possibleMoves)
        else:
            return None
    
class MoveFirstStrategy(object):
    def __init__(self) -> None:
        self.__name = "random"
        super().__init__()
    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            srcFieldsPos = [m.srcField.getPosition() for m in possibleMoves]
            return possibleMoves[srcFieldsPos.index(np.max(srcFieldsPos))]
        else:
            return None
class MoveLastStrategy(object):
    def __init__(self) -> None:
        self.__name = "random"
        super().__init__()
    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            srcFieldsPos = [m.srcField.getPosition() for m in possibleMoves]
            return possibleMoves[srcFieldsPos.index(np.min(srcFieldsPos))]
        else:
            return None
    