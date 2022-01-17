
from __future__ import annotations
from math import atan2,degrees
from typing import List, Literal, Union
from matplotlib.collections import PathCollection
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.axes as maxes

def labelLine(line,align=True,**kwargs):

    ax = line.axes
    xdata = list(line.get_xdata())
    ydata = list(line.get_ydata())

    for i,x2 in enumerate(xdata[1:]):
        x = (x2+xdata[i])/2
        
        label = str(ydata[i+1]-ydata[i])
        y = (ydata[i+1]+ydata[i])/2


        ip = 1
        for i in range(len(xdata)):
            if x < xdata[i]:
                ip = i
                break

        if align:
            #Compute the slope
            dx = xdata[ip] - xdata[ip-1]
            dy = ydata[ip] - ydata[ip-1]
            ang = degrees(atan2(dy,dx))

            #Transform to screen co-ordinates
            pt = np.array([x,y]).reshape((1,2))
            trans_angle = ax.transData.transform_angles(np.array((ang,)),pt)[0]

        else:
            trans_angle = 0

        #Set a bunch of keyword arguments
        if 'color' not in kwargs:
            kwargs['color'] = line.get_color()

        if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
            kwargs['ha'] = 'center'

        if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
            kwargs['va'] = 'center'

        if 'backgroundcolor' not in kwargs:
            kwargs['backgroundcolor'] = "#00000000"

        # if 'clip_on' not in kwargs:
        #     kwargs['clip_on'] = True

        if 'zorder' not in kwargs:
            kwargs['zorder'] = 2.5

        

        ax.text(x,y,label,**kwargs)


def test_annotations(line, **kwargs):
    if 'color' not in kwargs:
        kwargs['color'] = line.get_color()

    ax = line.axes
    xdata = list(line.get_xdata())
    ydata = list(line.get_ydata())

    for i, x2 in enumerate(xdata[1:]):
        xy0 = (xdata[i], ydata[i])
        xy1 = (x2, ydata[i+1])

        label = str(ydata[i+1]-ydata[i])
        ax.annotate(label, xy=xy0, xycoords='data',
                    xytext=xy1, textcoords='data',
                    arrowprops=dict(arrowstyle="<->",
                                    connectionstyle="bar",
                                    ec="k",
                                    shrinkA=0, shrinkB=0,**kwargs))

def labelLine_at_x(line,x:int, align=True, **kwargs):

    ax = line.axes
    xdata = list(line.get_xdata())
    ydata = list(line.get_ydata())

    for i, _ in enumerate(xdata[1:]):

        label = str(ydata[i+1]-ydata[i])
        y = (ydata[i+1]+ydata[i])/2


        #Set a bunch of keyword arguments
        if 'color' not in kwargs:
            kwargs['color'] = line.get_color()

        if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
            kwargs['ha'] = 'center'

        if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
            kwargs['va'] = 'center'

        if 'backgroundcolor' not in kwargs:
            kwargs['backgroundcolor'] =  "#00000000"

        # if 'clip_on' not in kwargs:
        #     kwargs['clip_on'] = True

        if 'zorder' not in kwargs:
            kwargs['zorder'] = 2.5

        ax.text(x, y, label, **kwargs)
def labelLine_at_y(line,y:int, align=True,ignore0=False, **kwargs):

    ax = line.axes
    xdata = list(line.get_xdata())
    ydata = list(line.get_ydata())

    for i, _ in enumerate(xdata[1:]):
        if ignore0 and ydata[i+1]-ydata[i] == 0:
            continue
        label = str(ydata[i+1]-ydata[i])
        x = (xdata[i+1]+xdata[i])/2


        #Set a bunch of keyword arguments
        if 'color' not in kwargs:
            kwargs['color'] = line.get_color()

        if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
            kwargs['ha'] = 'center'

        if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
            kwargs['va'] = 'center'

        if 'backgroundcolor' not in kwargs:
            kwargs['backgroundcolor'] =  "#00000000"

        # if 'clip_on' not in kwargs:
        #     kwargs['clip_on'] = True

        if 'zorder' not in kwargs:
            kwargs['zorder'] = 2.5

        ax.text(x, y, label, **kwargs)

def _get_quater_square(x:int,y:int):
    return mpatches.Rectangle( (x-.25,y-.25), .5, .5, ec="darkblue",alpha=.2,fill=None)

def _get_square(x:int,y:int,state:Literal["prepare", "fight", "retreat"],clear:bool):
    if state=="prepare":
        fc = "green"
    elif state == "fight":
        fc = "red"
    elif state == "retreat":
        fc = "blue"
    if clear:
        return mpatches.Rectangle( (x-.5,y-.5), 1, 1, ec="black", lw=2, fc=fc, alpha=1,fill=None)
    else:
        return mpatches.Rectangle( (x-.5,y-.5), 1, 1, ec="black",lw=2, fc=fc, alpha=.3)

def _get_circle(x:int,y:int,state:Literal["start", "end","turn"]):
    patches = []
    if state=="start":
        patches.append(mpatches.Ellipse((x,y), 1, 1, fill=None))
        patches.append(mpatches.Ellipse((x,y), .8, .8, fill=None))
    elif state == "ende":
       patches.append(mpatches.Ellipse((x,y), 1, 1, lw=3, fill=None))
    elif state == "turn":
       patches.append(mpatches.Ellipse((x,y), .5, .5, lw=4, fill=None, ec="yellow"))
    return patches

def _get_five_dots(x:int,y:int,state:Literal["normal", "small"]):
    patches = []
    x_offset=[-1,1]*2
    y_offset=[-1]*2+[1]*2
    xy=zip(x_offset,y_offset)
    if state=="normal":
        offset = .3
        size0 = .2
        size1 = .3
    elif state == "small":
        offset = .1
        size0 = .05
        size1 = .1
    for x_,y_ in xy:
        patches.append(mpatches.Ellipse((x+offset*x_,y+offset*y_), size0, size0, color="darkblue"))
        patches.append(mpatches.Ellipse((x+offset*x_,y+offset*y_), size1, size1, color="black",fill=None))
    patches.append(mpatches.Ellipse((x,y), size0, size0, color="darkblue"))
    patches.append(mpatches.Ellipse((x,y), size1, size1,  color="black",fill=None))
    return patches

def _get_4five_dots(x:int,y:int):
    patches = []
    x_offset=[-1,1]*2
    y_offset=[-1]*2+[1]*2
    xy=zip(x_offset,y_offset)
    for x_,y_ in xy:
        patches.extend(_get_five_dots(x+x_*0.25,y+y_*0.25,"small"))
        patches.append(_get_quater_square(x+x_*0.25,y+y_*0.25))
    return patches

def _get_eye(x:int,y:int):
    patches = []
    patches.append(mpatches.Ellipse((x,y), .1, .1, color="darkblue"))
    patches.append(mpatches.Ellipse((x-.025,y), .2, .43, lw=2,color="black",fill=None))
    patches.append(mpatches.Ellipse((x+.025,y), .2, .43, lw=2,color="black",fill=None))
    return patches


def _get_4eyes(x:int,y:int):
    patches = []
    x_offset=[-1,1]*2
    y_offset=[-1]*2+[1]*2
    xy=zip(x_offset,y_offset)
    for x_,y_ in xy:
        patches.extend(_get_eye(x+x_*0.25,y+y_*0.25))
        patches.append(_get_quater_square(x+x_*0.25,y+y_*0.25))
    return patches

def _get_steps(x:int,y:int):
    patches = []
    x_offset=[-.25,.25]*2
    y_offset=[-.25]*2+[.25]*2
    x_offset1=[-.125,.125]*2
    y_offset1=[-.125]*2+[.125]*2
    xy=list(zip(x_offset,y_offset))
    xy_inner=list(zip(x_offset1,y_offset1))
    for x_,y_ in xy:
        patches.append(_get_quater_square(x+x_,y+y_))
        for x_i,y_i in xy_inner:
            pos_i=(x+x_+x_i,y+y_+y_i)
        #     print("inner pos ",pos_i)
            patches.append(mpatches.Rectangle([v-.125 for v in pos_i], .25, .25, ec="black",alpha=.2,fill=None))
            if (-x_i*2) != x_ or y_i*2 != y_:
                patches.append(mpatches.Ellipse(pos_i, .1, .1, color="darkblue"))


    return patches


def _get_starpatches(x:int,y:int):
    xy = np.array((0, 0))+(x,y)
    patches = []
    offset = np.array((.1, .1))
    fco = "orange"
    fcb = "blue"
    alpha = .5

    patches = []

    for direction in range(0, 4):
        coordSign = (-1 if direction in (0, 1) else 1, 1)
        coordVal = (1 if direction in (0, 3) else 2.5,
                    1 if direction in (1, 2) else 2.5)
        color = fcb if direction in [0, 2] else fco

        for mirror in [1, -1]:
            pos = offset * (1, 1) * coordSign * coordVal * mirror
            ellipse = mpatches.Ellipse(xy + pos,
                                       0.175, .375, 22.5+45*direction, fc="black", alpha=alpha)
            patches.append(ellipse)
            ellipse = mpatches.Ellipse(xy + pos,
                                       0.15, .35, 22.5+45*direction, fc=color, alpha=alpha)
            patches.append(ellipse)

    ellipse = mpatches.Ellipse(xy, 0.25, .25, fc="black", alpha=alpha)
    patches.append(ellipse)
    ellipse = mpatches.Ellipse(xy, 0.2, .2, fc=fco, alpha=alpha)
    patches.append(ellipse)

    return patches

    
def draw_squares(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]],state:Literal["prepare", "fight", "retreat"],clear):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]

    for x_ in x:
        for y_ in y:
            ax.add_patch(_get_square(x_,y_,state,clear))


def draw_stars(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]]):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]
    for x_ in x:
        for y_ in y:
            for p in _get_starpatches(x_,y_):
                ax.add_patch(p)

def draw_circles(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]],state:Literal["start", "ende","turn"]):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]
    for x_ in x:
        for y_ in y:
            for p in _get_circle(x_,y_,state):
                ax.add_patch(p)
                ax.text(x_,y_,str(state).upper(),va="center",ha="center",fontweight="bold",fontsize="x-small", zorder=6)

def draw_fives(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]],state:Literal["normal", "small"]):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]
    for x_ in x:
        for y_ in y:
            for p in _get_five_dots(x_,y_,state):
                ax.add_patch(p)

def draw_4fives(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]]):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]
    for x_ in x:
        for y_ in y:
            for p in _get_4five_dots(x_,y_):
                ax.add_patch(p)

def draw_4eyes(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]]):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]
    for x_ in x:
        for y_ in y:
            for p in _get_4eyes(x_,y_):
                ax.add_patch(p)

def draw_steps(ax:maxes.Axes,x:Union[int,List[int]],y:Union[int,List[int]]):
    if not isinstance(x,list):
        x=[x]
    if not isinstance(y,list):
        y=[y]
    for x_ in x:
        for y_ in y:
            for p in _get_steps(x_,y_):
                ax.add_patch(p)


def draw_path(ax:maxes.Axes,x,y,color):
    HEAD_WIDTH = .2
    HEAD_LEN = .25

    
    ax.plot(x, y, color=color,zorder=5,lw=4)

    path = np.asarray([x,y])
    # print(path)
    theta = np.arctan2(np.asarray(y)[1:] - np.asarray(y)[:-1], np.asarray(x)[1:] - np.asarray(x)[:-1])

    x = x[:-1]
    y = y[:-1]
    x_ = x + .25 * np.cos(theta)
    y_ = y + .25 * np.sin(theta)


    for x1, y1, x2, y2 in zip(x,y,x_-x,y_-y):
        ax.arrow(x1, y1, x2, y2, head_width=HEAD_WIDTH, head_length=HEAD_LEN,length_includes_head=True, color=color, ec="#00000055",zorder=5)



    
