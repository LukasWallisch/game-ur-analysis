from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.gameSimulation.Player import Player


class Stone(object):
    def __init__(self, player: Player, id: int) -> None:
        super().__init__()
        self.__player = player
        self.__id = id
        self.__name = "p{playerid}s{stoneid}".format(
            playerid=player.getID(), stoneid=id)

    def getPlayer(self) -> Player:
        return self.__player

    def getId(self) -> int:
        return self.__id
    
    def getName(self) -> str:
        return self.__name


    def __str__(self) -> str:
        return self.__name
