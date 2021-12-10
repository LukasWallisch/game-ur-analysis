from typing import List
import src.gameSimulation.History as H
import src.gameSimulation.Dice as Dice
import src.gameSimulation.gameboard as GB
from src.gameSimulation.GameSettings import GameSettings
from src.gameSimulation.Player import Player

from src.gameSimulation.gameboard.Gameboard import MoveTuple


class GameUr:
    def __init__(self, gs: GameSettings) -> None:
        self.__gs = gs
        self.__gb = GB.Gameboard(gs)
        self.__dice = gs.getDice()
        self.__players = gs.getPlayers()
        # self.__round = 0
        self.__history = H.History(self.__gb, self.__gs)

    def run(self):
        self.__history.newRound()
        gameKeepRunning = True
        while gameKeepRunning:
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

    def __str__(self):
        return "Königliches Spiel von Ur:\n{history}".format(history=self.__history.getInfo())

    def __repr__(self) -> str:
        return self.__str__()

    def getWinner(self) -> Player:
        for player in self.__players:
            if set(self.__gb.getEndField().getStones4Player(player)) == set(player.getStones()):
                return player

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
        throwMoves = move.destField.addStone(move.stone)
        return throwMoves

    def getGB(self):
        return self.__gb

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
                throwMoves = self.executeMove(move)
                moveDist = move.destField.getPosition() - move.srcField.getPosition()
                landedOnDoubleRoll = move.destField.getPosition() in self.__gs.getDoubleRollFields()
                # if landedOnDoubleRoll:
                #     print("DoubleRoll")
                for throwMove in throwMoves:
                    result = self.executeMove(throwMove)
                    if result != None:
                        raise RuntimeError(
                            "A Throw Move can't produce a Throwmove")

        self.__history.saveStep(self.__gb, diceRoll, moveDist, player)
        return landedOnDoubleRoll
