import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .GameSettings import GameSettings
from .Player import Player
from .Dice import Dice


class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bool):
            return int(obj)
        if isinstance(obj, Player):
            return obj.getJson()
        if isinstance(obj, Dice):
            return obj.getJson()
        if isinstance(obj, GameSettings):
            return obj.getJson()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def decodingHooks(dct:dict):
    if "__player__" in dct:
        return Player.fromDB(dct["__player__"])
    elif "__dice__" in dct:
        return Dice.fromDB(dct["__dice__"])
    else:
        return dct
