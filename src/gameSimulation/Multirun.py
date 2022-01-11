import multiprocessing
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

def runGameDBfastest(settings:Tuple[GameSettings,int]):
    gs,fastest = settings
    g = GameUr(gs)
    g.run(fastest)
    return g.getStonesHistory4db(),g.getGamelength()


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

def multirunDB(n: int,processes:int, gamesPerChunk:int, gs: List[GameSettings],db_name_suffix:str):
    if processes == -1 or processes >= mp.cpu_count():
        PROCESSES = mp.cpu_count()
    else:
        PROCESSES = processes
    CHUNKS = n//gamesPerChunk
    

    # print("processes:",PROCESSES)
    # print("total Games:", gamesPerChunk*CHUNKS)
    print("chunks:", CHUNKS)
    print("gamePerChunk:", gamesPerChunk)
    print("gamesettings:", len(gs))
    createTabels(db_name_suffix)
    with mp.Pool(PROCESSES) as pool:
        chunksFinished = 0
        for i,sub_gs in enumerate(gs):
            print("for gs {}/{}".format(i+1, len(gs)))
            sub_results =[]
            for x in tqdm.tqdm(pool.imap_unordered(runGameDB, [sub_gs for _ in range(n)], gamesPerChunk), total=n, unit="games"):
                sub_results.append(x)
            chunksFinished += 1
            store_data_2_db({"gs": sub_gs, "history": sub_results},db_name_suffix)
    
    # h = []
    # for h_sub in results:
    #     h.extend(h_sub)
    return chunksFinished


def multirunDBSearchforFastest(n: int,processes:int, gamesPerChunk:int, gs: List[Tuple[GameSettings,int]],updateFastesNtimes:int =0 ):
    if processes == -1 or processes >= mp.cpu_count():
        PROCESSES = mp.cpu_count()
    else:
        PROCESSES = processes
    CHUNKS = n//gamesPerChunk
    

    # print("processes:",PROCESSES)
    # print("total Games:", gamesPerChunk*CHUNKS)
    print("processes:", PROCESSES)
    print("updateFastesNtimes:", updateFastesNtimes)
    print("chunks:", CHUNKS)
    print("gamePerChunk:", gamesPerChunk)
    print("gamesettings:", len(gs))
    createTabels("fastest")
    with mp.Pool(PROCESSES) as pool:
        chunksFinished = 0
        for i,gs_ in enumerate(gs):
            sub_gs,start_fastest = gs_
            sub_results =[]
            current_fastest = start_fastest
            for j in range(updateFastesNtimes):
                print("update {}/{} for gs {}/{}".format(j+1,updateFastesNtimes, i+1, len(gs)))
                
                print("current_fastest: {}".format(current_fastest))
                for x,new_fastest in tqdm.tqdm(pool.imap_unordered(runGameDBfastest, [(sub_gs,current_fastest) for i in range(n//updateFastesNtimes+1)], gamesPerChunk), total=n//updateFastesNtimes+1, unit="games"):
                    sub_results.append(x)
                    if new_fastest < current_fastest:
                        current_fastest = new_fastest
            chunksFinished += 1
            store_data_2_db({"gs": sub_gs, "history": sub_results},"fastest")
    
    # h = []
    # for h_sub in results:
    #     h.extend(h_sub)
    return chunksFinished
