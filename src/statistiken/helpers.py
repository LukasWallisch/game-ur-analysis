from typing import List, Union, Literal
from os import path
import numpy as np
import math
import sqlite3

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as mt
import matplotlib.colors as mc
import colorsys

import pandas as pd

from codeGameSimulation.jsonDeEncoders import decodingHooks
from src.codeGameSimulation.GameSettings import GameSettings
import gameBoardDisplay as gbd


colors = ["crimson", "blue", "green", "red", "orange", "purple",
          "gold", "lime", "magenta",  "cyan"]
cmap = LinearSegmentedColormap.from_list("mycmap", colors)


def makeVlines(
    ax: axes.Axes,
    x: List[np.float64],
    yVlaues: List[List[np.float64]],
    ls: str,
    colors: Union[List[str], str],
    alpha=1.0,
):
    if not isinstance(colors, list):
        colors = [colors]*len(x)
    if len(yVlaues) > 0:
        for i, a in enumerate(x):
            offset = 1 / ((len(x)) * 5)
            ax.axvline(
                a,
                color=colors[i],
                ymin=offset * (i * 5 + 1),
                ymax=offset * (i * 5 + 4),
                ls=ls,
                alpha=alpha,
            )
    else:
        for i, a in enumerate(x):
            ax.axvline(a, color=colors[i], ls=ls, alpha=alpha)


def setup_grid(ax):
    majorLocator = mt.MultipleLocator(5)
    minorLocator = mt.MultipleLocator(1)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.grid(b=True, axis="x", which='major', color='grey', alpha=.5, linestyle='-')
    ax.grid(b=True, axis="x", which='minor', color='grey', alpha=.3, linestyle='--')


def make_bestcaseLine(ax, bestcase=-1):
    if bestcase != -1:
        ax.axvline(bestcase, color=(0, 0, 0, 0.3), ls="--")
        ax.set_xticks(list(ax.get_xticks()) + [bestcase])
        ax.text(
            bestcase,
            np.mean(list(ax.get_yticks())),
            "  theoretische kürzeste Spieldauer",
            rotation=90,
            ha="right",
            va="center",
        )


def colorboxplot(
    data: List, ax: axes.Axes, labels: List[str], colors: List[str], bestcase=-1, ncol=2
) -> List[np.float64]:

    setup_grid(ax)

    medianprops = dict(linestyle="-.", linewidth=0, color="firebrick")
    bp = ax.boxplot(
        data, 0, "|", False, labels=labels, medianprops=medianprops, autorange=True,  whis=(1, 99)
    )
    num_boxes = len(data)
    medians = np.empty(num_boxes)
    minimums = np.empty(num_boxes)
    maximums = np.empty(num_boxes)
    yValues = np.empty((num_boxes, 2))

    for i in range(num_boxes):
        box = bp["boxes"][i]

        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        # Alternate between Dark Khaki and Royal Blue
        ax.add_patch(mpatches.Polygon(
            box_coords, facecolor=colors[i], alpha=0.5))
        # Now draw the median lines back over what we just filled in
        med = bp["medians"][i]
        minimum = min(data[i])
        maximum = max(data[i])

        minimums[i] = minimum
        maximums[i] = maximum
        medians[i] = med.get_xdata()[0]
        yValues[i] = med.get_ydata()

        ax.text(
            med.get_xdata()[0],
            med.get_ydata()[1],
            "{:0.01f}  ".format(med.get_xdata()[0]),
            horizontalalignment="right",
            verticalalignment="bottom",
            color="red",
        )

        ax.text(
            minimum,
            i+1,
            "{:0.0f} ".format(minimum),
            horizontalalignment="right",
            verticalalignment="center",
        )
        ax.text(
            maximum,
            i+1,
            " {:0.0f}".format(maximum),
            horizontalalignment="left",
            verticalalignment="center",
        )

        ax.text(
            np.average(data[i]),
            med.get_ydata()[1],
            "  {:0.04}".format(np.average(data[i])),
            horizontalalignment="left",
            verticalalignment="bottom",
            color="blue",
        )

        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        # ax.plot( np.average(data[i]),i+1,
        #         color='w', marker='|', markersize=12,markeredgecolor='k')
    makeVlines(ax, medians, yValues, "-", "red")
    makeVlines(ax, [np.average(data_) for data_ in data], yValues, "--", "blue")
    makeVlines(ax, maximums, yValues, "-.", "purple")
    makeVlines(ax, minimums, yValues, "-.", "green")

    make_bestcaseLine(ax, bestcase)

    median_legend = mpl.lines.Line2D(
        [], [], ls="-", color="red", label="Spiellänge Median"
    )
    avg_legend = mpl.lines.Line2D(
        [], [], ls="--", color="blue", label="Spiellänge Durchschnitt"
    )
    fliers_min_legend = mpl.lines.Line2D(
        [], [], ls="-.", color="green", label="Spiellänge Minimum"
    )
    fliers_max_legend = mpl.lines.Line2D(
        [], [], ls="-.", color="purple", label="Spiellänge Maximum"
    )

    ax.legend(handles=[median_legend, avg_legend,
              fliers_min_legend, fliers_max_legend], ncol=ncol)
    return medians


def makeHistogram(data: List, ax: axes.Axes, labels: List[str], colors: List[str], bestcase=-1, fill=True):
    maxBin = max([max(x) for x in data])
    minBin = min([min(x) for x in data])
    bins = range(math.floor(minBin), math.ceil(maxBin) + 2)
    ax.hist(data, color=colors[: len(data)],
            density=True, histtype="step", bins=bins, align="right")
    if fill:
        ax.hist(
            data,
            color=colors[: len(data)],
            label=labels,
            density=True,
            histtype="stepfilled",
            alpha=0.3,
            bins=bins,
            align="right"
        )
    ax.xaxis.grid(True, linestyle="-", which="major",
                  color="lightgrey", alpha=0.5)
    make_bestcaseLine(ax, bestcase)
    ax.yaxis.set_major_formatter(mt.PercentFormatter())
    ax.legend(ncol=3)


def zeichneErrechnetenWert(ax: axes.Axes, rs: Literal["r", "s"], multiplikator: int = 1, exactFinish=True):
    if exactFinish:
        if rs == "r":
            val = 8.391927856222578
            xlabel = "errechnete Werte für die Spiellänge in Runden"
        elif rs == "s":
            val = 9.867846767445288
            xlabel = "errechnete Werte für die Spiellänge in Schritten"
        else:
            raise Exception("unbekannter Wert für rs")
    else:
        if rs == "s":
            val = 7.874997997960489
            xlabel = "errechnete Werte für die Spiellänge in Schritten (Ziel muss nicht exakt getroffen werden)"
        else:
            raise Exception("unbekannter Wert für rs")
    xticks_val = [val*multiplikator]
    print(multiplikator)
    if multiplikator != 1:
        xticks_label = ["⌀ Länge x {}".format(multiplikator)]
    else:
        xticks_label = ["⌀ Länge"]
    sec_ax = ax.secondary_xaxis("top")
    sec_ax.set_xticks(xticks_val, xticks_label)
    sec_ax.set_xlabel(xlabel)
    sec_ax.set_color("blue")
    ax.axvline(val*multiplikator, color="grey", ls=":")


def scale_color(rgb, scale):
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale), s=min(1, s * scale))


def drawGame(db_row: sqlite3.Row, gs: GameSettings, figsize=[18, 8], showDiceRoll=True):
    stepLineOcc = 0.1
    stepcount = len(db_row["roundID"])
    roundIDsLabels = list(set(db_row["roundID"]))
    roundIDsTicks = [db_row["roundID"].index(l) for l in roundIDsLabels]

    player_names = [p.getName() for p in gs.getPlayers()]

    height_ratios = [3]
    mosaic = [["game"]]
    if showDiceRoll:
        mosaic.append(["dice"])
        height_ratios.append(1)

    fig, ax_dict = plt.subplot_mosaic(mosaic, figsize=figsize, layout="constrained", gridspec_kw={'height_ratios': height_ratios})

    for ax_name in ax_dict:
        ax = ax_dict[ax_name]
        ax.sharex(ax_dict["game"])

        ax.set_xlabel('Zug')
        ax.xaxis.set_major_locator(mt.MultipleLocator(10))
        ax.xaxis.set_minor_locator(mt.MultipleLocator(1))

        secax = ax.secondary_xaxis('top')
        secax.set_xlabel('Runde')
        secax.set_xticks(roundIDsTicks, roundIDsLabels, color=(0.1, 0.1, 0.1, 0.8))

        ax.set_xbound(-2, stepcount)
        ax.set_xlim(-2, stepcount)

        labeled_Player = [False]*len(player_names)
        for i, ap in enumerate(db_row["activePlayer"]):
            if ap in player_names:
                facecolor = colors[player_names.index(ap)]
            else:
                continue
            if not labeled_Player[player_names.index(ap)]:
                ax.axvspan(i-0.5, i+0.5, facecolor=facecolor, alpha=stepLineOcc, label="Zug für Spieler {}".format(player_names.index(ap)))
                labeled_Player[player_names.index(ap)] = True
            else:
                ax.axvspan(i-0.5, i+0.5, facecolor=facecolor, alpha=stepLineOcc)

    stone_colors = [[scale_color(mc.to_rgb(colors[i]), sc) for sc in list(np.linspace(.4, 1.5, p.getStoneCount()))] for i, p in enumerate(gs.getPlayers())]
    ax_game: axes.Axes = ax_dict["game"]
    gbd.makeGameboardDisplay(ax_game, *list(gs.getFieldsSettings().values()), xoff=1.5, show_hspans=False)
    ax_game.set_yticks(range(0, 16), ["start"]+list(range(1, 15))+["end"])
    ax_game.set_ybound(-.6, 17)
    ax_game.set_ylim(-.6, 17)
    ax_game.grid("y")

    for drf in gs.getDoubleRollFields():
        ax_game.axhline(drf, color=(0, 0, 0, 0.3),  ls='--', lw=2)

    for i, p in enumerate(db_row["stones"]):
        ax: axes.Axes = ax_dict["game"]
        ax_hist: axes.Axes = ax_dict["game"]
        playerStones = db_row["stones"][p]
        pid = i
        for j, s in enumerate(playerStones):
            sid = j
            ax.plot(range(len(db_row["roundID"])), playerStones[s], marker='.', label=fr"$St_{{{pid},{sid}}}$", color=stone_colors[i][j])

    ax_game.legend(ncol=len(gs.getPlayers())+sum([p.getStoneCount() for p in gs.getPlayers()]), handletextpad=.3, columnspacing=1, loc="upper left")
    ax_game.set_title("Bewegung der Spielsteine $St_{j,i}:$Spieler $j$ , Stein $i$ im Verlauf eines Spiels")

    if showDiceRoll:
        ax = ax_dict["dice"]
        ax.set_axisbelow(True)
        ax.grid(zorder=0)
        md = ax.bar(range(1, len(db_row["roundID"])), db_row["moveDist"][1:], alpha=1, label="gezogen", width=.75)
        dr = ax.bar(range(1, len(db_row["roundID"])), db_row["diceRoll"][1:], alpha=1, label="gewürfelt", width=.75, ec="black", color="none")

        # md = ax.bar(np.arange(.8, len(db_row["roundID"])-.2), db_row["moveDist"][1:], alpha=1, label="gezogen", width=.4)
        # dr = ax.bar(np.arange(1.2, len(db_row["roundID"])+.2), db_row["diceRoll"][1:], alpha=1, label="gewürfelt", width=.4)
        ax.set_ybound(-.5, 5)
        ax.set_ylim(-.5, 5)
        ax.set_yticks(range(0, 5), list(range(0, 5)))

        ax.legend(borderaxespad=0., ncol=len(gs.getPlayers())+2)

    return fig
