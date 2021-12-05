from typing import List
import src.gameSimulation.History as H
import src.gameSimulation.Dice as Dice
import src.gameSimulation.gameboard as GB
from src.gameSimulation.GameSettings import GameSettings
from src.gameSimulation.Player import Player

from src.gameSimulation.gameboard.Gameboard import MoveTuple


class GameUr:
    def __init__(self, gs:GameSettings) -> None:
        self.__gs = gs
        self.__gb = GB.Gameboard(gs)
        self.__dice = gs.getDice()
        self.__players = gs.getPlayers()
        # self.__round = 0
        self.__history = H.History(self.__gb, self.__gs)
    
    def tmp(self):
        self.__history.newRound()
        self.doMove(self.__players[0], 4)
        self.doMove(self.__players[1], 4)
        self.__history.newRound()
        self.doMove(self.__players[0], 4)
        self.doMove(self.__players[1], 4)
        # self.__players[0].getStones()[0].move(2)
        # self.__history.saveStep(self.__gb,2,self.__players[0])
        # self.__players[0].getStones()[1].move(3)
        # self.__history.saveStep(self.__gb, 3,self.__players[0])
        
    
    def __str__(self):
        return "Königliches Spiel von Ur:\n{history}".format(history=self.__history.getInfo())

    def __repr__(self) -> str:
        return self.__str__()

    def processRound(self) -> None:
        pass

    def executeMove(self,move:MoveTuple) ->List[MoveTuple] :
       move.srcField.removeStone(move.stone)
       throwMoves = move.destField.addStone(move.stone)
       return throwMoves

    def getGB(self):
        return self.__gb

    def doMove(self, player:Player, moveDist:int) -> List[GB.Stone]:
        strategy = player.getStrategy()
        move = strategy.chooseMove(player, moveDist, self.__gb)
        if move == None:
            print("No possible Move")
        else:
            throwMoves = self.executeMove(move)
            for throwMove in throwMoves:
                result = self.executeMove(throwMove)
                if result != None:

                    raise RuntimeError("A Throw Move can't produce a Throwmove")
        
        
        self.__history.saveStep(self.__gb, moveDist, player)

