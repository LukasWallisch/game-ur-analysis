import json
from typing import Dict, List, Tuple

import numpy as np

from . import Player as P
from . import Dice as D
from .Strategies import Strategy
from .jsonDeEncoders import PlayerEncoder, decodingHooks


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
                 exactFinish: bool = True
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

    @classmethod
    def fromDB(cls, row: Dict):
        return GameSettings(json.loads(row["players"],
                                       object_hook=decodingHooks),
                            json.loads(row["dice"], object_hook=decodingHooks),
                            row["prepareLength"],
                            row["fightLength"],
                            row["retreatLength"],
                            json.loads(row["fightSaveFields"]),
                            json.loads(row["doubleRollFields"]),
                            bool(row["noThrow"]),
                            bool(row["exactFinish"])
                            )

    def dbKeyValues(self):

        return {"players": json.dumps(self.__players, cls=PlayerEncoder),
                "dice": self.__dice.getJson(),
                "prepareLength": self.__prepareLength,
                "fightLength": self.__fightLength,
                "retreatLength": self.__retreatLength,
                "fightSaveFields": json.dumps(self.__fightSaveFields),
                "doubleRollFields": json.dumps(self.__doubleRollFields),
                "noThrow": int(self.__noThrow),
                "exactFinish": int(self.__exactFinish)}

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GameSettings):
            # print("wrong Type")
            # print(__o)
            return False
        else:
            d = __o.__dice == self.__dice
            pl = __o.__players == self.__players
            ppL = __o.__prepareLength == self.__prepareLength
            fL = __o.__fightLength == self.__fightLength
            rL = __o.__retreatLength == self.__retreatLength
            fsF = __o.__fightSaveFields == self.__fightSaveFields
            drF = __o.__doubleRollFields == self.__doubleRollFields
            nT = __o.__noThrow == self.__noThrow
            ef = __o.__exactFinish == self.__exactFinish
            # print([d, pl, ppL, fL, rL, fsF, drF, nT, ef])
            return all([d, pl, ppL, fL, rL, fsF, drF, nT, ef])

    def getJson(self):
        return {"players": self.__players,
                "dice": self.__dice,
                "prepareLength": self.__prepareLength,
                "fightLength": self.__fightLength,
                "retreatLength": self.__retreatLength,
                "fightSaveFields": self.__fightSaveFields,
                "doubleRollFields": self.__doubleRollFields,
                "noThrow": self.__noThrow,
                "exactFinish": self.__exactFinish}

    def getGamelength(self) -> int:
        """Summe aus prepare, fight und retreat plus zusätzlich zwei Felder für Start und Ende

        Returns:
            int: [description]
        """

        return self.__prepareLength+self.__fightLength+self.__retreatLength+2

    def getFieldsSettings(self):
        return{"prepareLength": self.__prepareLength,
               "fightLength": self.__fightLength,
               "retreatLength": self.__retreatLength,
               "fightSaveFields": self.__fightSaveFields,
               "doubleRollFields": self.__doubleRollFields}

    def getFieldSettings(self, position: int) -> Tuple[int, bool]:
        if position == 0 or position == self.getGamelength()-1:
            maxStones = max([len(p.getStones()) for p in self.__players])
            exclusiv = True
            isSave = True
        elif position in np.array(range(0, self.__prepareLength))+1 or position in np.array(range(0, self.__retreatLength))+1+self.__prepareLength+self.__fightLength:
            maxStones = 1
            exclusiv = True
            isSave = True
        else:
            maxStones = 1
            exclusiv = False
            isSave = False
        doubleRoll = position in self.__doubleRollFields

        return (maxStones, exclusiv, isSave, doubleRoll)

    def getPlayers(self) -> List[P.Player]:
        return self.__players

    def getStrategies(self) -> List[Strategy]:
        return [p.getStrategy() for p in self.__players]

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
