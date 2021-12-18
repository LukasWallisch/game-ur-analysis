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


def starpatches(coords):
    xy = np.array((0.5, 0.5))+coords
    patches = []
    offset = np.array((.1, .1))
    fco = "orange"
    fcb = "blue"

    patches = []


    for direction in range(0, 4):
        coordSign = (-1 if direction in (0, 1) else 1, 1)
        coordVal = (1 if direction in (0, 3) else 2.5,
                    1 if direction in (1, 2) else 2.5)
        color = fcb if direction in [0, 2] else fco

        for mirror in [1,-1]:
            pos = offset * (1, 1) * coordSign * coordVal * mirror
            ellipse = mpatches.Ellipse(xy+ pos ,
                                    0.15, .35, 22.5+45*direction, ec="black", lw=1, alpha=0.5, fc=color)
            patches.append(ellipse)
        

    ellipse = mpatches.Ellipse(xy, 0.2, .2, fc=fco, ec="black", lw=1,)
    patches.append(ellipse)

    return patches



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

                if y in np.array(doubleRollFields)-1:
                    # rect = mpatches.Rectangle(
                    #     xy, 1, 1, edgecolor="black", facecolor='grey', hatch='///')
                    # patches.append(rect)
                    patches.extend(starpatches(xy))
        if y in np.array(range(fightLength))+prepareLength:
            xy = grid[y]-[xoff,-.5]
            rect = mpatches.Rectangle(xy, 1, 1,fill=None)
            patches.append(rect)
            if show_label:
                labelR(xy)
            if y in np.array(doubleRollFields)-1:
                # rect = mpatches.Rectangle(
                #     xy, 1, 1, edgecolor ="black", facecolor='grey', hatch='///')
                # patches.append(rect)
                patches.extend(starpatches(xy))

            if y in np.array(fightSaveFields)-1:
                patches.extend(starpatches(xy))
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