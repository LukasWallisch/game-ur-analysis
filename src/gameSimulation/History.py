from . import constants as c
from . import GameSettings as GS
from . import gameboard as GB
from . import Player as P

from typing import Dict, List


class History(object):
    def __init__(self, gb: GB.Gameboard, gs: GS.GameSettings) -> None:
        self.__gbs = gs
        self.__players = gs.getPlayers()
        self.__rounds: List[Round] = []
        self.__currentRound = 0
        self.__rounds.append(Round(self.__currentRound))
        self.__winner: P.Player = None
        self.saveStep(gb, 0, 0, None)

    def newRound(self) -> None:
        self.__currentRound += 1
        self.__rounds.append(Round(self.__currentRound))

    def saveStep(self, gb: GB.Gameboard, diceRoll: int, moveDist: int, activePlayer: P.Player) -> None:
        self.__rounds[self.__currentRound].saveStep(gb, diceRoll, moveDist,
                                                    activePlayer)

    def saveWinner(self, winner: P.Player) -> None:
        self.__winner = winner

    def __str__(self) -> str:
        output = "{rounds}".format(
            rounds="\n".join([str(f) for f in self.__rounds]))
        if self.__winner != None:
            output += "Winner is Player {player}".format(player=self.__winner)
        return output

    def getInfo(self) -> str:
        output = "{rounds}".format(
            rounds="\n".join([r.getInfo(len(self.__players)) for r in self.__rounds]))
        if self.__winner != None:
            output += "\nWinner is Player {player}".format(
                player=self.__winner)
        return output

    def printLastStep(self) ->None:
        print(self.__rounds[-1].getSteps()[-1].getInfo(len(self.__players)))

    def getStonePositions(self, forJson: bool) -> dir:
        stonePositions = {"stones":{}}
        for p in self.__players:
            stonePositions["stones"].update({p.getName(): {}})
            for s in p.getStones():
                stonePositions["stones"][p.getName()].update({s.getName(): []})
        stonePositions.update({"roundID": []})
        stonePositions.update({"activePlayer": []})
        stonePositions.update({"diceRoll": []})
        stonePositions.update({"moveDist": []})
        stonePositions.update({"newRound": []})
        if not forJson:
            stonePositions.update({"globalStepID": []})

        roundID = -1
        globalStepID=0
        for r in self.__rounds:
            newRound = True
            roundID += 1
            for s in r.getSteps():
                stonePositions["roundID"].append(roundID)
                if not forJson:
                    stonePositions["globalStepID"].append(globalStepID)
                    globalStepID += 1

                player = s.getActivePlayer().getName() if s.getActivePlayer() != None else None
                stonePositions["activePlayer"].append(player)
                stonePositions["diceRoll"].append(s.getDiceRoll())
                stonePositions["moveDist"].append(s.getMoveDist())
                stonePositions["newRound"].append(newRound)
                newRound = False
                for f in s.getFields():
                    for st in f.getStones():
                        stonePositions["stones"][st.getPlayer().getName()][st.getName()].append(
                            f.getPos())
        return stonePositions


    def getStonePositions4db(self) -> Dict:
        stonePositions = {"stones":{}}
        for p in self.__players:
            stonePositions["stones"].update({p.getName(): {}})
            for s in p.getStones():
                stonePositions["stones"][p.getName()].update({s.getName(): []})
        stonePositions.update({"roundID": []})
        stonePositions.update({"activePlayer": []})
        stonePositions.update({"diceRoll": []})
        stonePositions.update({"moveDist": []})
        stonePositions.update({"newRound": []})

        roundID = -1
        for r in self.__rounds:
            newRound = True
            roundID += 1
            for s in r.getSteps():
                stonePositions["roundID"].append(roundID)
                player = s.getActivePlayer().getName() if s.getActivePlayer() != None else None
                stonePositions["activePlayer"].append(player)
                stonePositions["diceRoll"].append(s.getDiceRoll())
                stonePositions["moveDist"].append(s.getMoveDist())
                stonePositions["newRound"].append(newRound)
                newRound = False
                for f in s.getFields():
                    for st in f.getStones():
                        stonePositions["stones"][st.getPlayer().getName()][st.getName()].append(
                            f.getPos())
        
        stonePositions.update({"stepcount": len(stonePositions["roundID"])-1})
        stonePositions.update({"roundcount": max(stonePositions["roundID"])})
        return stonePositions

    def getRoundCount(self) -> int:
        return len(self.__rounds)


class Round(object):
    def __init__(self, id: int) -> None:
        self.__steps: List[Step] = []
        self.__id = id
        self.__currentStep = 0

    def saveStep(self, gb: GB.Gameboard, diceRoll: int, moveDist: int, activePlayer: P.Player) -> None:
        self.__steps.append(
            Step.fromGB(gb, self.__currentStep, diceRoll, moveDist, activePlayer))
        self.__currentStep += 1

    def getSteps(self):
        return self.__steps

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
        self.__name = "p{playerid}s{stoneid}".format(
            playerid=player.getID(), stoneid=id)

    @classmethod
    def fromGBStone(cls, stone: GB.Stone):
        return cls(stone.getPlayer(), stone.getId())

    def getInfo(self):
        output = "{playerAbbr}{playerid:0{playerIdLen}d}{stoneAbbr}{stoneid:0{stoneIdLen}d}".format(
            playerAbbr=c.PLAYER_ABBR, playerid=self.__player.getID(), playerIdLen=c.PLAYER_ID_LEN,
            stoneAbbr=c.STONE_ABBR, stoneid=self.__id, stoneIdLen=c.STONE_ID_LEN)
        return output

    def getName(self) -> str:
        return self.__name

    def getPlayer(self) -> P.Player:
        return self.__player

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return "H.Stone:" + str(self)


class Field:
    def __init__(self, stones: List[Stone], position: int, maxStones: int, playerExclusiv: bool) -> None:
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

    def getStones(self):
        return self.__stones

    def getPos(self):
        return self.__pos


class Step:
    def __init__(self, gameboard: List[Field], stepId: int, diceRoll: int, moveDist: int, activePlayer: P.Player) -> None:
        self.__activePlayer = activePlayer
        self.__id = stepId
        self.__diceRoll = diceRoll
        self.__moveDist = moveDist
        self.__gameboard = gameboard

    @classmethod
    def fromGB(cls, gb: GB.Gameboard, stepId: int, diceRoll: int, moveDist: int, activePlayer: P.Player):
        fields = [Field.fromGBField(f) for f in gb.getFields()]
        return cls(fields, stepId, diceRoll, moveDist, activePlayer)

    def getInfo(self, playerCount: int = 1) -> str:
        gameboard = "|".join([f.getInfo(playerCount)
                             for f in self.__gameboard])
        playername = "active Player: " + \
            self.__activePlayer.getName() if self.__activePlayer != None else "Start:"
        output = "Step{id:02d}: {playername:<{playernameLen}}  roll: {diceroll:02d} moveDist: {moveDist:02d} gameboard:{gameboard}".format(
            id=self.__id, playername=playername, playernameLen=c.HISTORY_PLAYERNAME_LEN, diceroll=self.__diceRoll, moveDist=self.__moveDist, gameboard=gameboard)
        return output

    def getActivePlayer(self) -> P.Player:
        return self.__activePlayer

    def getDiceRoll(self) -> int:
        return self.__diceRoll

    def getMoveDist(self) -> int:
        return self.__moveDist

    def getFields(self) -> List[Field]:
        return self.__gameboard
