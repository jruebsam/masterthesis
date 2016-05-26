import style as style
style.setup()

from matplotlib import ticker
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import os, sys

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

def main():
    cone     = "/home/upgp/jruebsam/simulations/mai16/week5/2_relaxation_neu/data/cone"
    frustum  = "/home/upgp/jruebsam/simulations/mai16/week5/2_relaxation_neu/data/frustum"

    pathes = [cone, frustum]

    f, ax = style.newfig(0.5)
    maxima = [1.45, 1.35, 1.25, 1.15, 1.05 ]
    hss  = np.linspace(0, 0.5, 5)

    f = lambda x, a, b : a*x + b


    for i, path in enumerate(pathes):
        hs, lb, err = [], [], []
        for omg, h  in zip(maxima, hss):
            vp = os.path.join('h_%.3f' % h, 'omg_%.2f' % omg, ('omg_%.2f' % omg) + '.ekin')

            ddir = os.path.join(path, vp)
            data = np.genfromtxt(ddir)
            time = data[:, 0]
            vz   = data[:, -3]
            b = time < 30
            popt, pcov = curve_fit(f, time[b], np.log(vz[b]))
            perr = np.sqrt(np.diag(pcov))

            hs.append(h)
            lb.append(popt[0])
            err.append(perr[0])

        label =  path.split('/')[-1].title()
        ax.errorbar(hs, lb, yerr=err, fmt='o-', label=label)
    plt.legend(ncol = 2, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    ax.set_xlabel(r'Offset $h_+$')
    ax.set_ylabel(r'Decay Rate $\lambda$')

    ax.set_ylim(-0.35, -0.1)
    ax.set_xlim(-0.05, 0.55)

    #formatter = ticker.ScalarFormatter(useMathText=True)
    #formatter.set_scientific(True)
    #formatter.set_powerlimits((-2,-1))
    #ax.yaxis.set_major_formatter(formatter)

    ax.grid(True)
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.savefig('fit_decay.pdf')

if __name__=='__main__':
    main()
