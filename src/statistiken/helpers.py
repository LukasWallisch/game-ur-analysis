from typing import List, Union
from os import path
import numpy as np
import math
import json
import sqlite3
from datetime import datetime
from itertools import groupby

import matplotlib as mpl
import matplotlib.axes as axes
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

from gameSimulation.jsonDeEncoders import decodingHooks

colors = ["green", "blue", "red", "orange", "purple",
          "gold", "lime", "magenta", "crimson", "cyan"]
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
    data: List, ax: axes.Axes, labels: List[str], colors: List[str], bestcase=-1
) -> List[np.float64]:
    medianprops = dict(linestyle="-.", linewidth=0, color="firebrick")
    bp = ax.boxplot(
        data, 0, "|", False, labels=labels, medianprops=medianprops, autorange=True
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
              fliers_min_legend, fliers_max_legend])


def makeHistogram(ax, data, labels, colors, bestcase=-1, fill=True):
    maxBin = max([max(x) for x in data])
    minBin = min([min(x) for x in data])
    bins = range(math.floor(minBin), math.ceil(maxBin) + 2)
    ax.hist(data, color=colors[: len(data)],
            density=True, histtype="step", bins=bins)
    if fill:
        ax.hist(
            data,
            color=colors[: len(data)],
            label=labels,
            density=True,
            histtype="stepfilled",
            alpha=0.3,
            bins=bins,
        )
    ax.xaxis.grid(True, linestyle="-", which="major",
                  color="lightgrey", alpha=0.5)
    make_bestcaseLine(ax, bestcase)
    ax.legend(ncol=3)


def getDataFromDB(db_dir: str, db_filename: str):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    delta0 = datetime.now()
    with sqlite3.connect(db_path) as con:
        con.row_factory = lambda _, row: list(row)
        rows_raw = con.execute(
            """select gameSettingsID,roundcount,stepcount,winners from game"""
        ).fetchall()
    delta1 = datetime.now()
    print("db load finished after {}".format(delta1 - delta0))
    rows_raw.sort(key=lambda r: r[0])
    delta2 = datetime.now()
    print("sort finished after {}".format(delta2 - delta1))

    rows = [list(g) for _, g in groupby(rows_raw, lambda r: r[0])]
    delta3 = datetime.now()
    print("groupby finished after {}".format(delta3 - delta2))
    rows.sort(key=lambda rows_sub: np.median([r for _, r, _, _ in rows_sub]))
    delta3_1 = datetime.now()
    print("sort finished after {}".format(delta3_1 - delta1))

    settings = []
    roundCounts = []
    stepCounts = []
    winners = []
    for sub_row in rows:
        settings_group = []
        roundCounts_sub = []
        stepCounts_sub = []
        winners_sub = []
        for s, rc, sc, w in sub_row:
            settings_group.append(s)
            roundCounts_sub.append(rc)
            stepCounts_sub.append(sc)
            winners_sub.append(json.loads(w))
        settings.append(min(settings_group) if min(
            settings_group) == max(settings_group) else -1)
        roundCounts.append(roundCounts_sub)
        stepCounts.append(stepCounts_sub)
        winners.append(winners_sub)
    delta4 = datetime.now()
    print("split finished after {}".format(delta4 - delta3_1))
    return roundCounts, stepCounts, winners, settings


def getSettingsFromDB(db_dir, db_filename):
    if db_filename == "":
        db_filename = "gameHistories"
    db_path = path.join(db_dir, db_filename+".db")
    with sqlite3.connect(db_path) as con:
        con.row_factory = lambda _, row: list(row)
        settings = [[p if isinstance(p,int) else json.loads(p, object_hook=decodingHooks) for p in r]
                    for r in con.execute("""select * from gameSettings""").fetchall()]
    print("settings loaded")
    return settings
