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




def getGameboard(prepare:int,danger:int,aftermath:int, xoff=0, show_label=False) -> PatchCollection:
    gl = prepare+danger+aftermath
    # create 3xgamelen grid to plot the artists
    grid = np.mgrid[0:2:3j,-1:gl:(gl+2)*1j].reshape(2,-1).T
    startoff = 1

    patches = []

    for x in range(2):
        xy = grid[0]+[x,.5]-[xoff,.5]
        circle = mpatches.Circle(xy, 0.49, lw=3)
        patches.append(circle)
        if show_label:
            labelC(xy, "start")

    for y in range(prepare):
        for x in range(2):
            xy = grid[y+startoff]-[.5-x,0]-[xoff,.5]
            rect = mpatches.Rectangle(xy , 1, 1)
            patches.append(rect)
            if show_label:
                labelR(xy)

    for y in range(danger):
        xy = grid[y+startoff+prepare]-[xoff,.5]
        rect = mpatches.Rectangle(xy , 1, 1)
        patches.append(rect)
        if show_label:
            labelR(xy)

    for y in range(aftermath):
        for x in range(2):
            xy = grid[y+startoff+prepare+danger]-[.5-x,0]-[xoff,.5]
            rect = mpatches.Rectangle(xy , 1, 1)
            patches.append(rect)
            if show_label:
                labelR(xy)

    for x in range(2):
        xy = grid[startoff+prepare+danger+aftermath]+[x,.5]-[xoff,.5]
        circle = mpatches.Circle(xy, 0.49)
        patches.append(circle)
        circle = mpatches.Circle(xy, 0.45)
        patches.append(circle)
        if show_label:
            labelC(xy, "end")

    collection = PatchCollection(patches, ec="black", fc="none",)
    return collection