from __future__ import annotations
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from src.gameSimulation.Player import Player
    from src.gameSimulation.GameSettings import GameSettings
    from .Stone import Stone

from .Field import Field


class MoveTuple(object):
    def __init__(self, stone: Stone, srcField: Field, destField: Field) -> None:
        self.stone = stone
        self.srcField = srcField
        self.destField = destField
        super().__init__()


class Gameboard:
    def __init__(self, gs: GameSettings) -> None:
        self.__Fields = [Field(i, gs, self) for i in range(gs.getGamelength())]
        self.__gs = gs

        for p in gs.getPlayers():
            for s in p.getStones():
                self.__Fields[0].addStone(s)

    def __str__(self) -> str:
        return "pass"

    def getFields(self) -> List[Field]:
        return self.__Fields

    def getStartField(self) -> Field:
        return self.__Fields[0]

    def getEndField(self) -> Field:
        return self.__Fields[-1]

    def getThrowMove(self, stone:Stone, srcField:Field):
        return MoveTuple(stone,srcField, self.getStartField())

    def isMovePossible(self, field: Field, player: Player, diceRoll: int) -> Field | None:
        destination_ID = self.__Fields.index(field) + diceRoll
        # Stone on Finish cant move
        if field == self.__Fields[-1]:
            return None
        # if no exat finish can overroll
        if destination_ID >= len(self.__Fields):
            if self.__gs.getExactFinish():
                return None
            else:
                return self.__Fields[-1]
        else:
            destinationField = self.__Fields[destination_ID]
            if destinationField.playerCanPlaceStone(player):
                return destinationField
            else:
                return None

    def getPossibleMoveTuples(self, player: Player, diceRoll: int) -> List[MoveTuple]:
        possibleMoves: List[Stone] = []
        for field in self.__Fields:
            for stone in field.getStones():
                if stone.getPlayer() == player:
                    destField = self.isMovePossible(field, player, diceRoll)
                    if destField != None:
                        possibleMoves.append(
                            MoveTuple(stone, field, destField))
        return possibleMoves
