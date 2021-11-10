class Error(Exception):
    def __init__(self, msg:str) -> None:
        super().__init__(msg)

class UnknownModeError(Error):
    def __init__(self, mode:str) -> None:
        self.message = "Unknown mode: {mode}\nonly following allowed: 'blocking'".format(mode=mode)
        super().__init__(self.message)


class UnknownFiledIDError(Error):
    def __init__(self, pos:int,startID:int, endID:int) -> None:
        self.message = "Unknown position: {pos}\nonly following range allowed: {start} - {end}".format(pos=pos,start=startID,end=endID)
        super().__init__(self.message)

class NoStoneToRemoveError(Error):
    def __init__(self, gameModel, player, position):
        self.message = "Cant remove stone for player{player} from position '{position}' because there is none!\n{gm}".format(player=player,position=position,gm=gameModel)
        super().__init__(self.message)
