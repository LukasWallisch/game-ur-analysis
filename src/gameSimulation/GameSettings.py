from typing import List, Tuple

import src.gameSimulation.Player as P
import src.gameSimulation.Dice as D


class GameSettings:
    def __init__(self,
                 players: List[P.Player],
                 dice: D.Dice,
                 prepareLength: int,
                 fightLength: int,
                 retreatLength: int,
                 fightSaveFields: List[int],
                 doubleRollFields: List[int],
                 noThrow: bool = False,
                 exactFinish:bool = True
                 ) -> None:
        """ players: List[P.Player],
                 dice: D.Dice,
                 prepareLength: int,
                 fightLength: int,
                 retreatLength: int,
                 fightSaveFields: List[int],
                 doubleRollFields: List[int],
                 noThrow: bool = False,
                 exactFinish:bool = True
        Returns:
            int: [description]
        """
        self.__players = players
        self.__dice = dice
        self.__prepareLength = prepareLength
        self.__fightLength = fightLength
        self.__retreatLength = retreatLength
        self.__fightSaveFields = fightSaveFields
        self.__doubleRollFields = doubleRollFields
        self.__noThrow = noThrow
        self.__exactFinish = exactFinish


    def getGamelength(self) -> int:
        """Summe aus prepare, fight und retreat plus zusätzlich zwei Felder für Start und Ende

        Returns:
            int: [description]
        """

        return self.__prepareLength+self.__fightLength+self.__retreatLength+2

    def getFieldsSettings(self) :
        return{"prepareLength":self.__prepareLength,
        "fightLength":self.__fightLength,
        "retreatLength":self.__retreatLength,
        "fightSaveFields":self.__fightSaveFields,
        "doubleRollFields":self.__doubleRollFields}
    def getFieldSettings(self, position:int) -> Tuple[int,bool]:
        if position == 0 or position == self.getGamelength()-1:
            maxStones = max([len(p.getStones()) for p in self.__players])
            exclusiv = True
        elif position in range(1, self.__prepareLength) or position in [i+self.__prepareLength+self.__fightLength+1 for i in range(0, self.__retreatLength)]:
            maxStones = 1
            exclusiv = True
        else:
            maxStones = 1
            exclusiv = False
        isSave = position in self.__fightSaveFields or position == 0 or position == self.getGamelength()-1
        doubleRoll = position in self.__doubleRollFields

        return (maxStones, exclusiv, isSave, doubleRoll)

        
    def getPlayers(self) -> List[P.Player]:
        return self.__players

    def getDice(self) -> D.Dice:
        return self.__dice

    def getPrepareLength(self) -> int:
        return self.__prepareLength

    def getFightLength(self) -> int:
        return self.__fightLength

    def getRetreatLength(self) -> int:
        return self.__retreatLength

    def getFightSaveFields(self) -> List[int]:
        return self.__fightSaveFields

    def getDoubleRollFields(self) -> List[int]:
        return self.__doubleRollFields

    def getNoThrow(self) -> bool:
        return self.__noThrow

    def getExactFinish(self) -> bool:
        return self.__exactFinish