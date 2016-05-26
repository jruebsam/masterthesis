import style as style
style.setup()

import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import os, sys


cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']


def main():
    dpath = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o2/omg_1.5/simulation.h5'
    dpath2= '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o4/omg_1.5/simulation.h5'



    f, ax = style.newfig(1., 0.6)

    x = np.linspace(0 , 1.1, 128)

    for i, (p, o) in enumerate(zip([dpath, dpath2], ['o2', 'o4'])):
        with tb.open_file(p, 'r') as d:
            vz = d.root.simdata.vz[-1]
        ax.plot(x, vz[64, 64]+i*0.01, label=o)

    plt.legend(ncol = 1, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    #ax.set_ylim(0, 1.2)
    ax.set_xlabel(r'z')
    ax.set_ylabel(r'$v_z$')

    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlim(0, 1.1)

    ax.grid(True)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('oscillations.pdf')

if __name__=='__main__':
    main()
