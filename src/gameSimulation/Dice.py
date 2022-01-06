import random
class Dice(object):
    def roll(self)->int:
        raise NotImplementedError("this is just the interface")

    def getName(self) -> str:
        return self._name


class D2(Dice):
    def __init__(self) -> None:
        self._name = "D2"
    def roll(self):
        return random.choice([1,0])
class D6(Dice):
    def __init__(self) -> None:
        self._name = "D6"
    def roll(self):
        return random.choice([1,2,3,4,5,6])
class D4(Dice):
    def __init__(self) -> None:
        self._name = "D4"
    def roll(self):
        return random.choice([1,2,3,4])


class MultiD2Dice(D2):
    def __init__(self, dicecount) -> None:
        self._name = "Multi D2 with {} dice".format(dicecount)
        self.__dicecount = dicecount
        super().__init__()
    def roll(self) -> int:
        d2_roll = super().roll
        return sum([d2_roll() for _ in range(0, self.__dicecount)])
class MultiD2DiceNo0(D2):
    def __init__(self, dicecount) -> None:
        self._name = "Multi D2 with {} dice with {} instead of 0".format(dicecount,dicecount)
        self.__dicecount = dicecount
        super().__init__()
    def roll(self) -> int:
        d2_roll = super().roll
        rollsum = sum([d2_roll() for _ in range(0, self.__dicecount)])
        return rollsum if rollsum > 0 else self.__dicecount+1





if __name__ == "__main__":
    d = MultiD2Dice(4)
    print(d.roll())