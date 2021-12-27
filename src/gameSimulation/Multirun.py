import random
import copy
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from . import GameUr, Strategies, Player, Dice, GameSettings
from multiprocessing import Process, Queue
import multiprocessing as mp


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


def multirun(n: int, gamesPerChunk:int, gs: GameSettings):
    PROCESSES = mp.cpu_count()
    CHUNKS = n//gamesPerChunk

    print("processes:",PROCESSES)
    print("total Games:", gamesPerChunk*CHUNKS)
    print("chunks:", CHUNKS)
    print("gamePerChunk:", gamesPerChunk)
    with mp.Pool(PROCESSES) as pool:
        print("start pool")
        results = pool.starmap(
            runGameNTimes, [(gamesPerChunk, copy.deepcopy(gs), i) for i in range(CHUNKS)])
        print("finish pool")

    h = []
    for h_sub in results:
        h.extend(h_sub)
    return h
