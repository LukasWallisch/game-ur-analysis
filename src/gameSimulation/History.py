import src.gameSimulation.constants as c
import src.gameSimulation.GameSettings as GS
import src.gameSimulation.gameboard as GB
from typing import List
import src.gameSimulation.Player as P


class History(object):
    def __init__(self, gb:GB.Gameboard, gs: GS.GameSettings ) -> None:
        self.__gbs = gs
        self.__players = gs.getPlayers()
        self.__rounds: List[Round] = []
        self.__currentRound = 0
        self.__rounds.append(Round(self.__currentRound))
        self.__winner:P.Player = None
        self.saveStep(gb,-1, None)

    def newRound(self) -> None:
        self.__currentRound += 1
        self.__rounds.append(Round(self.__currentRound))

    def saveStep(self, gb: GB.Gameboard, diceRoll: int, activePlayer: P.Player) -> None:
        self.__rounds[self.__currentRound].saveStep(gb, diceRoll,
                                                    activePlayer)
    def saveWinner(self, winner: P.Player) -> None:
        self.__winner = winner

    def __str__(self) -> str:
        output = "{rounds}".format(
            rounds="\n".join([str(f) for f in self.__rounds]))
        if self.__winner != None:
            output += "Winner is Player {player}".format(player=self.__winner)             
        return output

    def getInfo(self)->str:
        output = "{rounds}".format(
            rounds="\n".join([r.getInfo(len(self.__players)) for r in self.__rounds]))
        if self.__winner != None:
            output += "\nWinner is Player {player}".format(player=self.__winner)
        return output


class Round(object):
    def __init__(self, id: int) -> None:
        self.__steps: List[Step] = []
        self.__id = id
        self.__currentStep = 0

    def saveStep(self, gb: GB.Gameboard, diceRoll: int, activePlayer: P.Player) -> None:
        self.__steps.append(
            Step.fromGB(gb, self.__currentStep, diceRoll, activePlayer))
        self.__currentStep += 1

    def __str__(self) -> str:
        output = "Round{id:03d}: steps:\n{steps}".format(
            id=self.__id, steps="\n".join([str(f) for f in self.__steps]))
        return output

    def getInfo(self, playerCount: int = 1) -> str:
        output = "Round {id:03d}:\n{steps}".format(
            id=self.__id, steps="\n".join([s.getInfo(playerCount) for s in self.__steps]))
        return output


class Stone(object):
    def __init__(self, player: P.Player, id: int) -> None:
        self.__player = player
        self.__id = id

    @classmethod
    def fromGBStone(cls, stone: GB.Stone):
        return cls(stone.getPlayer(), stone.getId())

    def getInfo(self):
        output = "{playerAbbr}{playerid:0{playerIdLen}d}{stoneAbbr}{stoneid:0{stoneIdLen}d}".format(
            playerAbbr=c.PLAYER_ABBR, playerid=self.__player.getID(), playerIdLen=c.PLAYER_ID_LEN,
            stoneAbbr=c.STONE_ABBR, stoneid=self.__id, stoneIdLen=c.STONE_ID_LEN)
        return output

    def __str__(self) -> str:
        return "p{playerid}s{stoneid}".format(playerid=self.__player.getID(), stoneid=self.__id)

    def __repr__(self) -> str:
        return "H.Stone:" + str(self)


class Field:
    def __init__(self, stones: List[Stone], position: int, maxStones: int, playerExclusiv:bool) -> None:
        self.__maxStones = maxStones
        self.__stones = stones
        self.__pos = position
        self.__playerExclusiv = playerExclusiv

    @classmethod
    def fromGBField(cls, field: GB.Field):
        return cls([Stone.fromGBStone(s) for s in field.getStones()], field.getPosition(), field.getMaxStones(), field.getPlayerExclusiv())

    def getInfo(self, playerCount: int = 1):
        result = ",".join([s.getInfo() for s in self.__stones])
        playerCount = playerCount if self.__playerExclusiv else 1
        # +1 / -1 wegen den Kommas
        resultLen = (c.STONE_NAME_LEN+1)*self.__maxStones*playerCount-1
        output = "{result:{resultLen}}".format(
            result=result, resultLen=resultLen)
        return output

    


class Step:
    def __init__(self, gameboard: List[Field], stepId: int, diceRoll: int, activePlayer: P.Player) -> None:
        self.__activePlayer = activePlayer
        self.__id = stepId
        self.__diceRoll = diceRoll
        self.__gameboard = gameboard

    @classmethod
    def fromGB(cls, gb: GB.Gameboard, stepId: int, diceRoll: int, activePlayer: P.Player):
        fields = [Field.fromGBField(f) for f in gb.getFields()]
        return cls(fields, stepId, diceRoll, activePlayer)

    def getInfo(self, playerCount:int = 1) -> str:
        gameboard = "|".join([f.getInfo(playerCount) for f in self.__gameboard])
        playername = "active Player: "+self.__activePlayer.getName() if self.__activePlayer != None else "Start:"
        output = "Step{id:02d}: {playername:<{playernameLen}}  diceroll: {diceroll:02d} gameboard:{gameboard}".format(
            id=self.__id, playername=playername, playernameLen=c.HISTORY_PLAYERNAME_LEN, diceroll=self.__diceRoll, gameboard=gameboard)
        return output
