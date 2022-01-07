from typing import List
from . import History as H
from . import Dice as Dice
from . import gameboard as GB
from .GameSettings import GameSettings
from .Player import Player

from .gameboard.Gameboard import MoveTuple
from .gameboard.Stone import Stone


class GameUr:
    def __init__(self, gs: GameSettings) -> None:
        self.__gs = gs
        self.__gb = GB.Gameboard(gs)
        self.__dice = gs.getDice()
        self.__players = gs.getPlayers()
        # self.__round = 0
        self.__history = H.History(self.__gb, self.__gs)

    def run(self, maxRounds: int = 0):
        gameKeepRunning = True
        currentRound = 0
        while gameKeepRunning and (maxRounds != 0 and currentRound <= maxRounds):
            currentRound += 1
            gameKeepRunning = self.processRound()
        self.__history.saveWinner(self.getWinner())

    def reset(self):
        self.__gb = GB.Gameboard(self.__gs)
        self.__dice = self.__gs.getDice()
        self.__players = self.__gs.getPlayers()
        # self.__round = 0
        self.__history = H.History(self.__gb, self.__gs)

    def getGamelength(self):
        return self.__history.getRoundCount()

    def getStonesHistory(self, forJson: bool):
        w = self.getWinner()
        gl = self.getGamelength()
        sp = self.__history.getStonePositions(forJson)
        if forJson:
            return {"winner": [w_.getName() for w_ in w],
                    "history": sp,
                    }
        else:
            return {"winner": w,
                    "gameLength": gl,
                    "history": sp,
                    "players": self.__players,
                    "dice": self.__dice,
                    "gameSettings": self.__gs
                    }

    def __str__(self):
        return "Königliches Spiel von Ur:\n{history}".format(history=self.__history.getInfo())

    # def __repr__(self) -> str:
    #     return self.__str__()

    def getWinner(self) -> List[Player]:
        winner = []
        for player in self.__players:
            if set(self.__gb.getEndField().getStones4Player(player)) == set(player.getStones()):
                winner.append(player)
        return winner

    def getGB(self):
        return self.__gb

    def processRound(self) -> bool:
        self.__history.newRound()
        for player in self.__players:
            landedOnDoubleRoll = True
            while landedOnDoubleRoll:
                diceRoll = self.__dice.roll()
                landedOnDoubleRoll = self.doMove(player, diceRoll)
                if set(self.__gb.getEndField().getStones4Player(player)) == set(player.getStones()):
                    return False
        return True

    def executeMove(self, move: MoveTuple) -> List[MoveTuple]:
        move.srcField.removeStone(move.stone)
        thrownStones = move.destField.addStone(move.stone)
        return thrownStones

    def executeThrowMove(self, stone: Stone) -> List[MoveTuple]:
        thrownStones = self.__gb.getStartField().addStone(stone)
        return thrownStones

    def doMove(self, player: Player, diceRoll: int) -> List[GB.Stone]:
        # print("doMove für Player {player}, diceRoll: {diceRoll}".format(player=player,diceRoll=diceRoll))
        landedOnDoubleRoll = False
        if diceRoll == 0:
            # print("Rolled 0")
            moveDist = 0
        else:
            strategy = player.getStrategy()
            move = strategy.chooseMove(player, diceRoll, self.__gb)
            if move == None:
                # print("No possible Move")
                moveDist = 0
            else:
                thrownStones = self.executeMove(move)
                moveDist = move.destField.getPosition() - move.srcField.getPosition()
                landedOnDoubleRoll = move.destField.getPosition() in self.__gs.getDoubleRollFields()
                # if landedOnDoubleRoll:
                #     print("DoubleRoll")
                for thrownStone in thrownStones:
                    result = self.executeThrowMove(thrownStone)
                    if result != []:
                        raise RuntimeError(
                            "A Throw Move can't produce a Throwmove")

        self.__history.saveStep(self.__gb, diceRoll, moveDist, player)
        # self.__history.printLastStep()
        return landedOnDoubleRoll
