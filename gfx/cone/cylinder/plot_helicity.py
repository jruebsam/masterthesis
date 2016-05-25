import style as style
style.setup()

import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import os, sys


cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']


def main():
    dpath = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o2/omg_1.5/omg_1.5'

    f, ax = style.newfig(1., 0.5)

    x = np.linspace(0 , 1.1, 128)

    d = np.genfromtxt(dpath+'.ekin')
    time = np.copy(d[:, 0])
    d = np.genfromtxt(dpath+'.vb')
    hell = d[:, 2]
    upper = d[:, 0]
    lower = d[:, 1]

    ax.plot(time, hell, label='Total Helicity')
    ax.plot(time, upper, label='Helicity in Upper Half')
    ax.plot(time, lower, label='Helicity in Lower Half')

    plt.legend(ncol = 3, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    #ax.set_ylim(0, 1.2)
    ax.set_xlabel(r'Simulation Time t')
    ax.set_ylabel(r'Helicity $H$')
    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.1, 0.18)
    ax.grid(True)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('helicity.pdf')

if __name__=='__main__':
    main()
