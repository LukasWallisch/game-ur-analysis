
from typing import List
import src.gameSimulation.gameboard as GB

import src.gameSimulation.Strategies as _Strategy


class Player:
    def __init__(self, id: int, stonecount: int, strategy: _Strategy.Strategy) -> None:
        self.__id = id
        self.__stones = [GB.Stone(self, i) for i in range(stonecount)]
        self.__strategy = strategy

    def getName(self) -> str:
        return "p{id:02d}".format(id=self.__id)

    def getID(self) -> int:
        return self.__id

    def getStones(self) -> List[GB.Stone]:
        return self.__stones

    def getStrategy(self) -> _Strategy.Strategy:
        return self.__strategy

    def getStoneCount(self) -> int:
        return len(self.__stones)

    def __str__(self) -> str:
        return "Player {id:02d} with stones {stones}".format(id=self.__id, stones="|".join([str(x) for x in self.__stones]))

    def __repr__(self) -> str:
        return "Player: id:{id}, strategy:{strategy}, stones:{stones}".format(id=self.__id, strategy=self.__strategy, stones=",".join([str(s)for s in self.__stones]))
