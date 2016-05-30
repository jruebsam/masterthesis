import style
style.setup()

import numpy as np
import pycurb.analysis as pa
import matplotlib.pyplot as plt
import os
import tables as tb
from glob import glob
import matplotlib.colors as colors
import matplotlib.cm as cmx
from scipy import optimize

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def flow(x, h1, h2):
    return -(x**2 - x*(h1 + h2) + h1*h2)*4

def main():
    f, ax = style.newfig(0.45, hscale=1.6)

    x = np.linspace(0, 0.5, 5)
    vt =  flow(x, 0.25, 0.75)

    plt.plot(x, vt, 'bo--', mew=0, ms = 6, label='theory')

    vt[0]+= 0.3
    vt[1]+= 0.05
    plt.plot(x, vt, 'ro--', mew=0, ms = 4, label='vol.pen.')

    vt[0] = 0
    vt[1] = 0
    plt.plot(x, vt, 'go--', mew=0, ms = 3, label='dir. forcing.')

    plt.axvline(0.25, ls=':', c='k', lw =1)

    plt.xlim(-0.1, 0.6)
    plt.ylim(-1, 0.5)

    labels = ['L2', 'L1', 'B', 'R1', 'R2']
    plt.xticks(x, labels, rotation='vertical')
    l = [-0.5, 0, 0.5]
    l2 = ['-', 0, '+']

    plt.yticks(l,l , rotation='vertical')
    #ax.axes.get_yaxis().set_ticks([])

    plt.xlabel('Grid points')
    plt.ylabel(r'$\propto$ velocity $ v_x$')
    plt.legend(loc=4, fontsize=7)
    #ax.xaxis.tick_top()
    #ax.xaxis.set_label_position('top')
    #plt.subplots_adjust(bottom=0.0, top=0.77, right=1., left=0.2)
    plt.tight_layout()
    plt.savefig('stencil.pdf')
    #plt.show()

if __name__=='__main__':
    main()
