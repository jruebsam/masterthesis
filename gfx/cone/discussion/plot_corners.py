import style
style.setup()

from scipy.signal import argrelmin, argrelmax
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from matplotlib import ticker
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it
import itertools
from scipy import optimize
plt.rcParams['text.latex.preamble']=r'\makeatletter \newcommand*{\rom}[1]{\expandafter\@slowromancap\romannumeral #1@} \makeatother'
plt.rcParams.update()

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
markers = itertools.cycle('o^*')
from cycler import cycler

def main():

    cdir = os.getcwd()

    rs = [0.375, 0.25]

    f, ax = plt.subplots(1, figsize=style.figsize(0.5, 1.0))

    # build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width + 0.5
    top = bottom + height

    l =  0.5*np.tan(np.pi/3.)

    for radius in [0.0]:
        h = radius
        r = 0.21650635094610973
        hc = 0.5*np.tan(np.pi/3.)

        p00 = (0.5-r, 0.375)
        p01 = (0.5+r, 0.375)
        p11 = (1,hc )
        p10 = (0, hc )
        po2= (1, 1 + h )
        po = (0, 1 + h )
        cube_lines = [p00, p01, p11, po2, po, p10]
        x = [p[0] for p in cube_lines]
        y = [p[1] for p in cube_lines]
        d = np.column_stack((x,y))
        p = Polygon(d, alpha=0.5, color='b', hatch='x')
        ax.add_artist(p)

    rs = np.linspace(0, 0.5, 5)
    w1s= [0.0, 0.0, 1.8, 1.75, 1.65]
    w2s= [0.7, 0.6, 0.5, 0.45, 0.4]

    for i, (w1, w2, radius) in enumerate(zip(w1s, w2s, rs)):
        dx = 0.125
        if i > 0:
            h = radius
            r = 0.21650635094610973
            hc = 0.5*np.tan(np.pi/3.)

            p00 = (0, 1 + (i-1)*dx)
            p01 = (1, 1 + (i-1)*dx)
            p11 = (0, 1 + i*dx)
            p10 = (1, 1 + i*dx)

            cube_lines = [p00, p01, p10, p11]
            x = [p[0] for p in cube_lines]
            y = [p[1] for p in cube_lines]
            d = np.column_stack((x,y))
            p = Polygon(d, alpha=0.5, color='b', hatch='x')
            ax.add_artist(p)

        if w1 > 0.1:
            theta = np.arccos(w1/2)
            hl = np.tan(theta)
            htop = 1 + i*dx
            x = [0, 1]
            y = [htop, htop -hl]
            if i==3:
                ax.plot(x, y, 'r', label=r'Peak \rom{6}')
            else:
                ax.plot(x, y, 'r')

        if w2 > 0.1:
            theta = np.arccos(w2/2)
            r = 0.3
            hl = np.tan(theta)*0.3

            htop = 1 + i*dx
            x = [0, r]
            y = [htop, htop -hl]
            if i==3:
                ax.plot(x, y, 'g', label=r'Peak \rom{3}')
            else:
                ax.plot(x, y, 'g')

    plt.ylim(0.375, 1.5)
    plt.xlabel('x')
    plt.ylabel('z')

    plt.legend(ncol = 2, fontsize=9, loc='upper center', bbox_to_anchor=(0.5, 1.2),
           fancybox=True, shadow=True)

    plt.subplots_adjust(bottom =0.15, top =0.8)
    plt.savefig('corners.pdf')

if __name__=='__main__':
    main()
