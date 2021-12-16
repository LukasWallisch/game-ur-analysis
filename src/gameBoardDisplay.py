from typing import List
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


def labelC(xy, text):
    xy = xy-[0,.1]  # shift y-value for label so that it's below the artist
    plt.text(xy[0],xy[1], text, ha="center", family='sans-serif', size=10)
def labelR(xy):
    xy += [.5,.5] 
    text = int(xy[1]+1)
    xy = xy-[0,.1]  # shift y-value for label so that it's below the artist
    plt.text(xy[0],xy[1], text, ha="center", family='sans-serif', size=10)


def getGameboard(prepareLength: int,
                 fightLength: int,
                 retreatLength: int,
                 fightSaveFields: List[int],
                 doubleRollFields: List[int], xoff=0, show_label=False) -> PatchCollection:
    gl = prepareLength+fightLength+retreatLength+2
    # create 3xgamelen grid to plot the artists
    grid = np.mgrid[0:1, 0:gl].reshape(2, -1).T
    startoff = 1

    patches = []
    fc = []
    for x in range(2):
        xy = grid[0]+[x,0]-[xoff,0]

        ellipse = mpatches.Ellipse(xy, 1, 1, fill=None)
        ellipse2 = mpatches.Ellipse(xy, .8, .8, fill=None)
        patches.append(ellipse)
        patches.append(ellipse2)
        if show_label:
            labelC(xy, "start")
        
    for y in range(gl):
        if y in range(prepareLength) or y in np.array(range(retreatLength))+prepareLength+fightLength:
            for x in range(2):
                xy = grid[y]-[.5-x,0]-[xoff,-.5]
                rect = mpatches.Rectangle(xy, 1, 1, fill=None)
                patches.append(rect)
                if show_label:
                    labelR(xy)

                if y in doubleRollFields:
                    print("doubleroll!")
                    rect = mpatches.Rectangle(
                        xy, 1, 1, linewidth=0, facecolor='green', hatch='///')
                    patches.append(rect)
        if y in np.array(range(fightLength))+prepareLength:
            xy = grid[y]-[xoff,-.5]
            rect = mpatches.Rectangle(xy, 1, 1,fill=None)
            patches.append(rect)
            if y in doubleRollFields:
                rect = mpatches.Rectangle(
                    xy, 1, 1, linewidth=0, facecolor='green', hatch='///')
                patches.append(rect)
            if show_label:
                labelR(xy)
            if y in fightSaveFields:
                rect = mpatches.RegularPolygon(xy+[.5, -.5], 4, .5, fill=None)
                patches.append(rect)
                if show_label:
                    labelR(xy)


    # for y in range(retreatLength):
    #     for x in range(2):
    #         xy = grid[y+startoff+prepareLength+fightLength]-[.5-x,0]-[xoff,-.5]
    #         rect = mpatches.Rectangle(xy , 1, 1)
    #         patches.append(rect)
    #         if show_label:
    #             labelR(xy)

    for x in range(2):
        xy = grid[-1]+[x,0]-[xoff,0]
        ellipse = mpatches.Ellipse(xy, 1, 1, lw=3, fill=None)
        patches.append(ellipse)
        if show_label:
            labelC(xy, "end")

    collection = PatchCollection(patches, match_original =True)
    return collection