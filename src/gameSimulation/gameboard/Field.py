from __future__ import annotations
from os import error
from typing import TYPE_CHECKING, List
from src.gameSimulation import constants
if TYPE_CHECKING:
    import Stone as S
    from src.gameSimulation.Player import Player
    from src.gameSimulation.GameSettings import GameSettings
    import src.gameSimulation.gameboard.Gameboard as GB

import src.gameSimulation.constants as c


class FieldFullError(error):
    def __init__(self, pos, playerStoneCount, maxStoneCount) -> None:
        msg = "Feld {pos} ist schon voll! ist/max: {playerStoneCount}/{maxStoneCount}".format(
            pos=pos, playerStoneCount=playerStoneCount, maxStoneCount=maxStoneCount)
        super().__init__(msg)


class Field(object):
    def __init__(self, position: int, gs: GameSettings, gb: GB.Gameboard) -> None:
        maxStones, playerExclusiv, isSave, doubleRoll = gs.getFieldSettings(
            position)
        self.__pos = position
        self.__maxStones = maxStones
        self.__playerExclusiv = playerExclusiv
        self.__isSave = isSave
        self.__doubleRoll = doubleRoll
        self.__gs = gs
        self.__gb = gb
        self.__stones: List[S.Stone] = []

    def addStone(self, stone: S.Stone) -> List[GB.MoveTuple]:
        thrownStones: List[S.Stone] = []
        if not self.__isSave:
            for oldStone in self.__stones:
                if oldStone.getPlayer() != stone.getPlayer() and not self.__playerExclusiv:
                    thrownStones.append(oldStone)
        
        for ts in thrownStones:
            self.__stones.remove(ts)

        
        if self.__playerExclusiv:
            if [s.getPlayer() for s in self.__stones].count(stone.getPlayer()) >= self.__maxStones:
                raise FieldFullError(self.__pos,
                                     len(list(filter(lambda s: s.getPlayer() ==
                                         stone.getPlayer(), self.__stones))),
                                     self.__maxStones)
        else:
            if len(self.__stones) >= self.__maxStones:
                raise FieldFullError(self.__pos, len(self.__stones),self.__maxStones)

        self.__stones.append(stone)
        return thrownStones

    def removeStone(self, stone: S.Stone):
        self.__stones.remove(stone)

    def getStones(self) -> List[S.Stone]:
        return self.__stones

    def getStones4Player(self,player:Player) -> List[S.Stone]:
        return list(filter(lambda s: s.getPlayer() == player, self.__stones))

    def getPosition(self) -> int:
        return self.__pos

    def getMaxStones(self) -> int:
        return self.__maxStones

    def getPlayerExclusiv(self) -> bool:
        return self.__playerExclusiv

    def getIsSave(self) -> bool:
        return self.__isSave

    def getDoubleRoll(self) -> bool:
        return self.__doubleRoll

    def playerCanPlaceStone(self, player: Player) -> bool:
        if len(self.__stones) > 0:
            # Wenn auf einem SaveField schon ein Stein liegt kann kein anderer Stein darauf ziehen.
            players = [s.getPlayer() for s in self.__stones]
            if self.__isSave:
                return False
            # Manche Felder werden für jeden Spieler einzeln betrachtet, er kann nur einen Stein darauf setzen wenn er seien Maximalanzahl an Steinen für das Feld noch nicht erreicht hat.
            elif self.__playerExclusiv:
                if players.count(player) >= self.__maxStones:
                    return False
            # Manche Felder werden für alle Spieler betrachtet, er kann nur einen Stein darauf setzen wenn die Maximalanzahl an Steinen für das Feld noch nicht erreicht hat.
            else:
                # Der Spieler kann sich nicht sebst werfen
                if player in players:
                    if players.count(player) >= self.__maxStones:
                        return False
        return True

    def __str__(self) -> str:
        stoneNameLenght = c.STONE_NAME_LEN
        if self.__pos == 0 or self.__pos == self.__gs.getGamelength()+1:  # start- / endfields

            # +1 for comma between and -1 for remove last comma
            outputlen = ((stoneNameLenght+1)*self.__maxStones)-1
        else:
            outputlen = (stoneNameLenght+1)*len(self.__gs.getPlayers())-1
        return "{stones:>{outputlen}}".format(stones=",".join([str(s) for s in self.__stones]), outputlen=outputlen)

    def __repr__(self) -> str:

        output = "pos: {pos}".format(pos=self.__pos,)
        # output = "pos: {pos}, maxStones: {maxStones}, playerExclusiv: {playerExclusiv}, isSave: {isSave}, doubleRoll: {doubleRoll}, gs: {gs}, gb: {gb}, stones: {stones}, ".format(pos= self.__pos,
        #                                                                                            maxStones= self.__maxStones,
        #                                                                                            playerExclusiv= self.__playerExclusiv,
        #                                                                                            isSave= self.__isSave,
        #                                                                                            doubleRoll= self.__doubleRoll,
        #                                                                                            gs= self.__gs,
        #                                                                                            gb= self.__gb,
        #                                                                                            stones= self.__stones,)
        return output
