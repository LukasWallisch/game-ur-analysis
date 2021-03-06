from __future__ import annotations
import random
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import Player

from .gameboard.Gameboard import Gameboard, MoveTuple


class Strategy(object):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def getStrategyFromName(cls, name: str):
        if name == "random" or name == "Zufall":
            return RandomStrategy()
        elif name == "MoveFirst":
            return MoveFirstStrategy()
        elif name == "MoveLast":
            return MoveLastStrategy()
        elif name == "Score_DR+MD":
            return ScoreStrategy()
        elif name == "Score_DR":
            return ScoreDoubleRollStrategy()
        elif name == "Score_TO":
            return ScoreThrowOpponentStrategy()
        elif name == "ScoreMF_nF":
            return ScoreMF_nF()
        else:
            raise Exception("Unknown Strategy name: "+name)

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        raise NotImplementedError("this is just the interface")

    def __repr__(self) -> str:
        return self.getName()


class RandomStrategy(Strategy):
    def __init__(self) -> None:
        self.__name = "random"
        self.__fig_name = "Zufall"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            return random.choice(possibleMoves)
        else:
            return None


class MoveFirstStrategy(Strategy):
    def __init__(self) -> None:
        self.__name = "MoveFirst"
        self.__fig_name = "MoveFirst"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            srcFieldsPos = [m.srcField.getPosition() for m in possibleMoves]
            return possibleMoves[srcFieldsPos.index(np.max(srcFieldsPos))]
        else:
            return None


class MoveLastStrategy(Strategy):
    def __init__(self) -> None:
        self.__name = "MoveLast"
        self.__fig_name = "MoveLast"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            srcFieldsPos = [m.srcField.getPosition() for m in possibleMoves]
            return possibleMoves[srcFieldsPos.index(np.min(srcFieldsPos))]
        else:
            return None


class ScoreStrategy(Strategy):
    def __init__(self) -> None:
        self.__name = "Score_DR+MD"
        self.__fig_name = "Score DR & MD"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            scores = [(not m.srcField.getIsSave())*5 +
                      (m.destField.getIsSave())*10 +
                      (m.destField.getDoubleRoll())*100 +
                      (m.destField.getPosition()) -
                      (m.srcField.getPosition())
                      for m in possibleMoves]
            return possibleMoves[scores.index(np.max(scores))]
        else:
            return None


class ScoreDoubleRollStrategy(Strategy):
    def __init__(self) -> None:
        self.__name = "Score_DR"
        self.__fig_name = "Score DR"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            scores = [(m.destField.getDoubleRoll())*100
                      for m in possibleMoves]
            return possibleMoves[scores.index(np.max(scores))]
        else:
            return None


class ScoreThrowOpponentStrategy(Strategy):
    def __init__(self) -> None:
        self.__name = "Score_TO"
        self.__fig_name = "Score TO"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            scores = [(m.destField.wouldThrowOpponent(player))*100 +
                      (m.destField.getPosition())
                      for m in possibleMoves]
            return possibleMoves[scores.index(np.max(scores))]
        else:
            return None


class ScoreMF_nF(Strategy):
    def __init__(self) -> None:
        self.__name = "ScoreMF_nF"
        self.__fig_name = "Score MF nF"
        super().__init__()

    def getName(self) -> str:
        return self.__name

    def getFigName(self) -> str:
        return self.__fig_name

    def chooseMove(self, player: Player, diceRoll: int, gb: Gameboard) -> MoveTuple:
        possibleMoves = gb.getPossibleMoveTuples(player, diceRoll)
        if len(possibleMoves) > 0:
            scores = [
                ((not m.srcField.getIsSave())*m.destField.getIsSave())*100 +
                ((m.srcField.getIsSave())*(not  m.destField.getIsSave()))*(-100) +
                      (m.destField.getPosition())
                      for m in possibleMoves]
            return possibleMoves[scores.index(np.max(scores))]
        else:
            return None
