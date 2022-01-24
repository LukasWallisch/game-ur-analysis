import json
import random
from typing import Dict


class Dice(object):
    def roll(self) -> int:
        raise NotImplementedError("this is just the interface")

    def getName(self) -> str:
        return self._name
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Dice):
            return __o.getJson() == self.getJson()
        else: return False

    def getJson(self) -> str:
        return json.dumps({"__dice__": {"n": self._name, "dc": 1}})

    @classmethod
    def fromDB(cls, dct: Dict):
        # print(dct)
        if dct["n"] == "D2":
            return D2()
        elif dct["n"] == "D4":
            return D4()
        elif dct["n"] == "D6":
            return D6()
        elif dct["n"] == "MultiD2Dice":
            return MultiD2Dice(dct["dc"])
        elif dct["n"] == "MultiD2DiceNo0":
            return MultiD2DiceNo0(dct["dc"])
        else:
            return None


class D2(Dice):
    def __init__(self) -> None:
        self._name = "D2"
    def roll(self):
        return random.choice([1, 0])


class D6(Dice):
    def __init__(self) -> None:
        self._name = "D6"
    def roll(self):
        return random.choice([1, 2, 3, 4, 5, 6])


class D4(Dice):
    def __init__(self) -> None:
        self._name = "D4"
    def roll(self):
        return random.choice([1, 2, 3, 4])


class MultiD2Dice(D2):
    def __init__(self, dicecount) -> None:
        super().__init__()
        self._name = "Multi D2 ({})".format(dicecount)
        self.__dicecount = dicecount

    def roll(self) -> int:
        d2_roll = super().roll
        return sum([d2_roll() for _ in range(0, self.__dicecount)])

    def getJson(self) -> str:
        return json.dumps({"__dice__": {"n": "MultiD2Dice", "dc": self.__dicecount}})


class MultiD2DiceNo0(D2):
    def __init__(self, dicecount) -> None:
        super().__init__()
        self._name = "Multi D2 ({}) 0->{} ".format(
            dicecount, dicecount)
        self.__dicecount = dicecount

    def roll(self) -> int:
        d2_roll = super().roll
        rollsum = sum([d2_roll() for _ in range(0, self.__dicecount)])
        return rollsum if rollsum > 0 else self.__dicecount+1

    def getJson(self) -> str:
        return json.dumps({"__dice__": {"n": "MultiD2DiceNo0", "dc": self.__dicecount}})


if __name__ == "__main__":
    d = MultiD2Dice(4)
    print(d.roll())
