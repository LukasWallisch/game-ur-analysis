from src.game.Exceptions import NoStoneToRemoveError, UnknownFiledIDError
from src.game.stone import Stone
from tabulate import tabulate
import random


class GameModel(object):

    def __init__(self, stones=7, players=2, prepare=2, fight=8, retreat=4) -> None:
        super().__init__()

        self._playerscount = players
        self._players = range(players)
        self._startFieldID = 0
        self._endFieldID = 1+prepare+fight+retreat
        self._prepare = prepare
        self._fight = fight
        self._retreat = retreat

        self.gameboard = ([[[] for p in self._players]
                          for position in range(2+prepare+fight+retreat)])
        for p in self._players:
            self.gameboard[0][p].extend(
                [Stone(player=p, id=s) for s in range(stones)])
        # self.startfield = ([[Stone() for s in range(stones)] for p in range(players)])

    def __str__(self):

        outputData = []
        headers = ["state", "pos"]
        headers.extend(["p{player:02d}".format(player=player)
                       for player in self._players])
        for i, pos in enumerate(self.gameboard):

            if i == self._startFieldID:
                fieldstate = "start"
            elif i <= self._prepare:
                fieldstate = "prepare"
            elif i <= self._prepare+self._fight:
                fieldstate = "fight"
            elif i <= self._prepare+self._fight+self._retreat:
                fieldstate = "retreat"
            elif i == self._endFieldID:
                fieldstate = "end"
            else:
                raise UnknownFiledIDError(
                    pos, self._startFieldID, self._endFieldID)

            # if i == self._startFieldID:
            #     outputData.append(["start".format(pos=i), *[len(players) for players in pos]])
            # elif i == self._endFieldID:
            #     outputData.append(["end".format(pos=i), *[len(players) for players in pos]])
            # else:
            #     outputData.append(["{pos:02d}".format(pos=i), *[len(players) for players in pos]])
            outputData.append([fieldstate, "{pos:02d}".format(
                pos=i), *[len(players) for players in pos]])

        outputData.reverse()
        return tabulate(outputData, headers, tablefmt="presto")

    def _move_stone_throw(self, player: int, stone: Stone, moveDist: int) -> None:
        currentPosition = stone.getPositon()
        newPosition = currentPosition+moveDist
        nameCurrentPosition = "start" if currentPosition == self._startFieldID else "end" if currentPosition == self._endFieldID else str(
            currentPosition)
        # nameNewPosition = "start" if newPosition == self._startFieldID else "end" if newPosition == self._endFieldID else str(newPosition)
        if len(self.gameboard[currentPosition][player]) == 0:
            raise NoStoneToRemoveError(self, player, nameCurrentPosition)
        else:
            self.gameboard[currentPosition][player].remove(stone)
            self.gameboard[newPosition][player].append(stone)
            stone.moveTo(newPosition)


        if newPosition != self._startFieldID:
            for inactivePlayer in list(self._players)[0:player]+list(self._players)[player+1:self._playerscount]:
                for stone in self.gameboard[newPosition][inactivePlayer]:
                    print("stone:{} position:{}".format(stone,newPosition))

                    self._throw_stone(inactivePlayer, stone)

    def _throw_stone(self, player: int, stone: Stone) -> None:
        print(stone)
        currentPosition = stone.getPositon()
        newPosition = self._startFieldID
        nameCurrentPosition = "start" if currentPosition == self._startFieldID else "end" if currentPosition == self._endFieldID else str(
            currentPosition)
        if len(self.gameboard[currentPosition][player]) == 0:
            raise NoStoneToRemoveError(self, player, nameCurrentPosition)
        else:
            self.gameboard[currentPosition][player].remove(stone)
            self.gameboard[newPosition][player].append(stone)
            stone.moveTo(newPosition)

    def moveFirstAtPos(self, player: int, position: int, moveDist: int):
        self._move_stone_throw(
            player, self.gameboard[position][player][0], moveDist)

    def moveLastAtPos(self, player: int, position: int, moveDist: int):
        self._move_stone_throw(
            player, self.gameboard[position][player][-1], moveDist)

    def moveRandomAtPos(self, player: int, position: int, moveDist: int):
        self._move_stone_throw(
            player, random.choice(self.gameboard[position][player]), moveDist)

    def calcPossibleMoves(self, player: int, moveDist: int) -> list:
        """This function returns all stones that are possible to move for a given player and a given move distance in the current gamestate

        Args:
            player (int): index of the current player
            moveDist (int): movedistance / value form the dices

        Returns:
            list: with all possible fields from that the move can be started
        """
        return [-1]
