import random
import copy
from datetime import datetime
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from store2db import createTabels, store_data_2_db
from .GameUr import GameUr
from .GameSettings import GameSettings
from multiprocessing import Process, Queue
import multiprocessing as mp
import tqdm


def getThreadCount()->int:
    return mp.cpu_count()


def runGameNTimes(n: int, gs: GameSettings, chunkId:int):
    delta0 = datetime.now()
    g = GameUr.GameUr(gs)
    h = []
    # print("chunk {}: start {} games".format(chunkId,n))
    for _ in range(n):
        g.run(1000)
        h.append(g.getStonesHistory())
        g.reset()
    delta1 = datetime.now()
    # print("chunk {}: finished {} games in {} ".format(chunkId,n, delta1-delta0))
    return h

def runGame(settings:Tuple[GameSettings, bool]):
    gs,forJson = settings
    g = GameUr(gs)
    g.run(1000)
    return g.getStonesHistory(forJson)


def runGameDB(gs: GameSettings):
    g = GameUr(gs)
    g.run(1000)
    return g.getStonesHistory4db()


def multirun(n: int, gamesPerChunk:int, gs: List[GameSettings],forJson:bool):
    PROCESSES = mp.cpu_count()
    CHUNKS = n//gamesPerChunk
    

    # print("processes:",PROCESSES)
    # print("total Games:", gamesPerChunk*CHUNKS)
    print("chunks:", CHUNKS)
    print("gamePerChunk:", gamesPerChunk)
    print("gamesettings:", len(gs))
    gamesDone = 0
    with mp.Pool(PROCESSES) as pool:
        results = []
        for sub_gs in gs:
            # print("start pool")
            # results = pool.imap_unordered(runGame,
            #      [copy.deepcopy(gs) for i in range(CHUNKS)],gamesPerChunk)
            sub_results =[]
            for x in tqdm.tqdm(pool.imap_unordered(runGame, [(copy.deepcopy(sub_gs), forJson) for i in range(n)], gamesPerChunk), total=n, unit="games"):
                sub_results.append(x)
            # print("finish pool")
            results.append({"gs":sub_gs,"history":sub_results})
    
    # h = []
    # for h_sub in results:
    #     h.extend(h_sub)
    return results

def multirunDB(n: int, gamesPerChunk:int, gs: List[GameSettings]):
    PROCESSES = mp.cpu_count()
    CHUNKS = n//gamesPerChunk
    

    # print("processes:",PROCESSES)
    # print("total Games:", gamesPerChunk*CHUNKS)
    print("chunks:", CHUNKS)
    print("gamePerChunk:", gamesPerChunk)
    print("gamesettings:", len(gs))
    createTabels()
    with mp.Pool(PROCESSES) as pool:
        chunksFinished = 0
        for sub_gs in gs:
            sub_results =[]
            for x in tqdm.tqdm(pool.imap_unordered(runGameDB, [copy.deepcopy(sub_gs) for i in range(n)], gamesPerChunk), total=n, unit="games"):
                sub_results.append(x)
            chunksFinished += 1
            store_data_2_db({"gs": sub_gs, "history": sub_results})
    
    # h = []
    # for h_sub in results:
    #     h.extend(h_sub)
    return chunksFinished
