import json

from .GameSettings import GameSettings
from .Dice import Dice
from .Player import Player


class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bool):
            return int(obj)
        if isinstance(obj, Player):
            return obj.getJson()
        if isinstance(obj, Dice):
            return obj.getName()
        if isinstance(obj, GameSettings):
            return obj.getJson()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
