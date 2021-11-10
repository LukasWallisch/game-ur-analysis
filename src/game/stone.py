class Stone(object):
    def __init__(self,player:int,id:int) -> None:
        super().__init__()
        self._name= "p{player:02d}st{id:02d}".format(player=player,id=id)
        self._position = 0
        self._history = bytearray()

    def moveTo(self, position: int):
        self._position = position
        self._history.append(position)

    def stay(self):
        self._history.append(self._position)


    def getPositon(self) -> int:
        return self._position

    def getHistory(self) -> int:
        return self._history

    def __str__(self) -> str:
        return "{name} at {pos:02d}".format(name=self._name,pos=self._position)
    def __repr__(self) -> str:
        return "{name} at {pos:02d}".format(name=self._name,pos=self._position)
    
