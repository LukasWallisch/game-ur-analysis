import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from src.gameSimulation import GameUr, Strategies, Player, Dice, GameSettings
from multiprocessing import Process, Queue
import multiprocessing as mp


def runGameNTimes(n: int, gs: GameSettings):
    print("start method")
    g = GameUr.GameUr(gs)
    gl = []
    w = []
    print("start for")
    for _ in range(n):
        g.run()
        gl.append(g.getGamelength())
        w.append(g.getWinner())
        g.reset()
    return (gl, w)


def multirun(n:int,gs:GameSettings):
    PROCESSES = mp.cpu_count()-2
    gamePerCpu = n//PROCESSES+1

    print(PROCESSES)
    print(gamePerCpu)
    print(gamePerCpu*PROCESSES)
    with mp.Pool(PROCESSES) as pool:
        print("start pool")
        results = pool.starmap(runGameNTimes, [(gamePerCpu,copy.deepcopy(gs))]*PROCESSES)
        print("finish pool")

    gl =  []
    w = []
    for gl_sub, w_sub in results:
        gl.extend(gl_sub)
        w.extend(w_sub)
    return (gl,w)
