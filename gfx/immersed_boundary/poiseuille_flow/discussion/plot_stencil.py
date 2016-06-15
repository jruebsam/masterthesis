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


    path = '/home/upgp/jruebsam/simulations/feb16/week4/3_vp_gc'
    do2 = path+'/data/nu_0.001000/o2/res_100'
    do4 = path+'/data/nu_0.001000/o4/res_100'

    ds = [do2, do4]
    for p,l  in zip(ds, ['FD2', 'FD4']):
        with tb.open_file(os.path.join(p, 'simulation.h5'), 'r') as d:
            vx = d.root.simdata.vx[-1]
            h = d.root.icdata.H[0, 0, :]


        plt.plot(vx[8, 8, 45: 50], 'o--', label=l)
    plt.ylim(-0.00002, 0.00002)

    plt.xlabel('Grid points')
    plt.xticks([])
    plt.yticks([])
    plt.ylabel(r'Velocity $ v_x$')
    plt.legend(loc=3, fontsize=7)
    #ax.xaxis.tick_top()
    #ax.xaxis.set_label_position('top')
    #plt.subplots_adjust(bottom=0.0, top=0.77, right=1., left=0.2)
    plt.tight_layout()
    plt.savefig('stencil.pdf')

if __name__=='__main__':
    main()
