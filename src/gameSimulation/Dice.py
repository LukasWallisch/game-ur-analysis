import random
class Dice(object):
    def roll(self)->int:
        raise NotImplementedError("this is just the interface")


class D2(Dice):
    def roll(self):
        return random.choice([1,0])


class MultiD2Dice(D2):
    def __init__(self, dicecount) -> None:
        self.__dicecount = dicecount
        super().__init__()
    def roll(self) -> int:
        return sum([super().roll for _ in range(0,self.__dicecount) ])