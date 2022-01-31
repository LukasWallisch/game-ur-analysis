import sqlite3
import json
from os import path
from datetime import datetime
from itertools import groupby
from typing import Dict, List
import numpy as np


from codeGameSimulation.jsonDeEncoders import decodingHooks
from .GameSettings import GameSettings
from .GameUr import GameUr, Player, Dice, GameUrDTO
from . import Strategies as S




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def createTabels(db_dir: str, db_filename: str = ""):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    print(db_path)
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory

    con.execute('''CREATE TABLE IF NOT EXISTS game ( 
        gameID INTEGER PRIMARY KEY AUTOINCREMENT,
        gameSettingsID INTEGER,
        stepcount INTEGER,
        roundcount INTEGER,
        winners TEXT,
        stones TEXT,
        roundID TEXT,
        activePlayer TEXT,
        diceRoll TEXT,
        moveDist TEXT,
        newRound TEXT
        )''')

    con.execute('''CREATE TABLE IF NOT EXISTS gamesettings (
        gameSettingsID Integer PRIMARY KEY,
        players TEXT,
        dice TEXT,
        prepareLength Integer,
        fightLength Integer,
        retreatLength Integer,
        fightSaveFields TEXT,
        doubleRollFields TEXT,
        noThrow INTEGER,
        exactFinish INTEGER) ''')
    
    con.commit


def store_data_2_db(data: Dict[GameSettings, List[GameUrDTO]], db_dir: str, db_filename: str = ""):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory

    gs: GameSettings = data["gs"]
    gss: List[GameSettings] = []
    gsIDs = [-1]

    for row in con.execute('''select gameSettingsID, players, dice,
                           prepareLength , fightLength , retreatLength , fightSaveFields ,
                           doubleRollFields , noThrow , exactFinish from gamesettings'''):
        gss.append(GameSettings.fromDB(row))
        gsIDs.append(row["gameSettingsID"])

    if any([gs == gs_ for gs_ in gss]):
        gs_index = gss.index(gs)
        # print("use existing gs")
    else:
        gs_index = max(gsIDs)+1
        print("new gs")
        gs_keys = ["gameSettingsID"]
        gs_qms = ["?"]
        gs_values = [gs_index]

        kvs = gs.dbKeyValues()
        for k in kvs:
            gs_keys.append(k)
            gs_qms.append("?")
            gs_values.append(kvs[k])
        # print(gs_keys)
        # print(gs_qms)
        # print(gs_values)
        gs_keys_formated = ", ".join(gs_keys)
        gs_qms_formated = ", ".join(gs_qms)
        # print(gs_keys_formated)
        # print(gs_qms_formated)
        con.execute("INSERT INTO gamesettings(" + gs_keys_formated +
                    ") values ("+gs_qms_formated+")", gs_values)

    # print(gs_index)

    game_keys = ["gameSettingsID"]
    game_qms = ["?"]

    for k in GameUrDTO.dbKeys():
        game_keys.append(k)
        game_qms.append("?")
    
    game_keys_formated = ", ".join(game_keys)
    game_qms_formated = ", ".join(game_qms)
    
    # print(game_keys_formated)
    # print(game_qms_formated)

    con.executemany("INSERT INTO game ("+game_keys_formated +") VALUES ("+game_qms_formated+")",
                    [[gs_index, *g.dbValues()] for g in data["history"]])

    con.commit()


def getGameFromDB(gameID: int, db_dir: str, db_filename: str):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    delta0 = datetime.now()
    sqlite3.register_converter("text", lambda s: json.loads(s))
    with sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) as con:
        con.row_factory = sqlite3.Row
        rows_raw = con.execute(
            """select * from game where gameID==(?)""", [gameID]
        ).fetchone()
    return rows_raw

def getHistoryFromDB(db_dir: str, db_filename: str):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    delta0 = datetime.now()
    sqlite3.register_converter("text", lambda s: json.loads(s))
    with sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) as con:
        con.row_factory = sqlite3.Row
        rows_raw = con.execute(
            """select stones from game """
        ).fetchall()
    return rows_raw


def getDataFromDB(db_dir: str, db_filename: str):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    delta0 = datetime.now()
    with sqlite3.connect(db_path) as con:
        con.row_factory = lambda _, row: list(row)
        rows_raw = con.execute(
            """select gameID, gameSettingsID,roundcount,stepcount,winners from game"""
        ).fetchall()
    delta1 = datetime.now()
    print("db load finished after {}".format(delta1 - delta0))

    rows_raw.sort(key=lambda r: r[1])
    delta2 = datetime.now()
    print("sort finished after {}".format(delta2 - delta1))

    rows = [list(g) for _, g in groupby(rows_raw, lambda r: r[1])]
    delta3 = datetime.now()
    print("groupby finished after {}".format(delta3 - delta2))

    rows.sort(key=lambda rows_sub: np.median([r for _, _, r, _, _ in rows_sub]))
    delta3_1 = datetime.now()
    print("sort finished after {}".format(delta3_1 - delta1))

    ids = []
    settings = []
    roundCounts = []
    stepCounts = []
    winners = []
    for sub_row in rows:
        ids_sub = []
        settings_group = []
        roundCounts_sub = []
        stepCounts_sub = []
        winners_sub = []
        for i, s, rc, sc, w in sub_row:
            ids_sub.append(i)
            settings_group.append(s)
            roundCounts_sub.append(rc)
            stepCounts_sub.append(sc)
            winners_sub.append(json.loads(w))

        ids.append(ids_sub)
        settings.append(min(settings_group) if min(
            settings_group) == max(settings_group) else -1)
        roundCounts.append(roundCounts_sub)
        stepCounts.append(stepCounts_sub)
        winners.append(winners_sub)
    delta4 = datetime.now()
    print("split finished after {}".format(delta4 - delta3_1))
    return ids, roundCounts, stepCounts, winners, settings


def getSettingsFromDB(db_dir, db_filename):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    with sqlite3.connect(db_path) as con:
        con.row_factory = lambda _, row: list(row)
        settings = [[p if isinstance(p, int) else json.loads(p, object_hook=decodingHooks) for p in r]
                    for r in con.execute("""select * from gameSettings""").fetchall()]
    print("settings loaded")
    return settings


def getGSFromDB(db_dir, db_filename):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        settings = [GameSettings.fromDB(r)
                    for r in con.execute("""select * from gameSettings""").fetchall()]
    print("settings loaded")
    return settings



if __name__ == "__main__":

    createTabels()
    equalSettings = [4, 8, 2, [8], [4, 8, 13]]
    sub_gs = GameSettings([Player(0, 7, S.MoveFirstStrategy()), Player(
        1, 7, S.MoveFirstStrategy())], Dice.MultiD2Dice(4), *equalSettings)
    g = GameUr(sub_gs)
    g.run()
    h = g.getStonesHistory4db()
    tmp = {"gs": sub_gs, "history": [h]}

    print(tmp["history"][0].dbValues())
    store_data_2_db(tmp)
