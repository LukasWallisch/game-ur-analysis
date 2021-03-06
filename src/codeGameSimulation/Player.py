
from typing import List
from . import gameboard as GB
from . import constants as c

from . import Strategies as _Strategy


class Player:
    def __init__(self, id: int, stonecount: int, strategy: _Strategy.Strategy) -> None:
        self.__id = id
        self.__stones = [GB.Stone(self, i) for i in range(stonecount)]
        self.__strategy = strategy

    @classmethod
    def fromDB(cls, input: dict):
        return cls(input["id"],
        input["stonecount"],
        _Strategy.Strategy.getStrategyFromName(input["strategy"]))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Player):
            return False
        else:
            i = __o.__id == self.__id
            s = len(__o.__stones) == len(self.__stones)
            st = __o.__strategy.getName() == self.__strategy.getName()
            return all([i, s, st])

    def getName(self) -> str:
        return "{abbr}{id:0{idLen}d}".format(id=self.__id, abbr=c.PLAYER_ABBR, idLen=c.PLAYER_ID_LEN)

    def getID(self) -> int:
        return self.__id

    def getStones(self) -> List[GB.Stone]:
        return self.__stones

    def getStrategy(self) -> _Strategy.Strategy:
        return self.__strategy

    def getStoneCount(self) -> int:
        return len(self.__stones)

    def __str__(self) -> str:
        return "Player {id:d} with stones {stones}".format(id=self.__id, stones="|".join([str(x) for x in self.__stones]))

    def __repr__(self) -> str:
        return "Player: id:{id}, strategy:{strategy}, stones:{stones}".format(id=self.__id, strategy=self.__strategy, stones=",".join([str(s)for s in self.__stones]))

    def getJson(self) -> dict:
        return {"__player__": {"id": self.__id, "stonecount": len(self.__stones), "strategy": self.__strategy.getName()}}
