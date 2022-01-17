from typing import List, Union
import numpy as np
import math
import matplotlib as mpl
import matplotlib.axes as axes
import matplotlib.patches as mpatches


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

        minimums[i] = minimum
        medians[i] = med.get_xdata()[0]
        yValues[i] = med.get_ydata()

        ax.text(
            med.get_xdata()[0],
            med.get_ydata()[1],
            "{:0.03f} ".format(med.get_xdata()[0]),
            horizontalalignment="right",
            verticalalignment="bottom",
        )

        ax.text(
            minimum,
            i+1,
            "{:0.03f}  ".format(minimum),
            horizontalalignment="right",
            verticalalignment="bottom",
        )

        ax.text(
            np.average(data[i]),
            med.get_ydata()[1],
            "  {:0.03f}".format(np.average(data[i])),
            horizontalalignment="left",
            verticalalignment="bottom",
            color="blue",
        )

        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        # ax.plot( np.average(data[i]),i+1,
        #         color='w', marker='|', markersize=12,markeredgecolor='k')
    makeVlines(ax, medians, yValues, "-", "red")
    makeVlines(ax, [np.average(data_)
               for data_ in data], yValues, "--", "blue")
    makeVlines(ax, minimums, yValues, "-.", "green")

    make_bestcaseLine(ax, bestcase)

    median_legend = mpl.lines.Line2D(
        [], [], ls="-", color="red", label="Spiellänge Median"
    )
    avg_legend = mpl.lines.Line2D(
        [], [], ls="--", color="blue", label="Spiellänge Durchschnitt"
    )
    fliers_legend = mpl.lines.Line2D(
        [], [], ls="-.", color="green", label="Spiellänge Minimum"
    )

    ax.legend(handles=[median_legend, avg_legend, fliers_legend])


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
