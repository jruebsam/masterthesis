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

    path = [cone, frustum]

    f, ax = style.newfig(0.5, 1.5)
    omg = 1.25
    h = 0.25

    f = lambda x, a, b : a*x + b

    vp = '/'.join(['h_%.3f' % h, 'omg_%.2f' % omg, ('omg_%.2f' % omg) + '.ekin'])

    for i, p in enumerate(path):
        d =np.genfromtxt(os.path.join(p, vp))

        time = d[:, 0]
        vz = d[:, -3]

        b = time < 30

        lb =  p.split('/')[-1].title()
        ax.plot(time, vz, label=lb)

        popt, pcov = curve_fit(f, time[b], np.log(vz[b]))
        perr = np.sqrt(np.diag(pcov))

        if i==0:
            xdata = np.linspace(0, 50, 100)
        else:
            xdata = np.linspace(0, 80, 100)
        ydata = np.exp(f(xdata, *popt))
        ax.plot(xdata, ydata, '--', label=r'$\lambda: %.3f\pm %.3f$'\
                % (popt[0], perr[0]))

    plt.yscale('log')
    plt.legend(ncol = 1, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    ax.set_xlabel(r'Simulation Time t')
    ax.set_ylabel(r'$\left<v_z^2\right>$')

    #formatter = ticker.ScalarFormatter(useMathText=True)
    #formatter.set_scientific(True)
    #formatter.set_powerlimits((-2,-1))
    #ax.yaxis.set_major_formatter(formatter)

    ax.set_xlim(0, 120)
    ax.set_ylim(1e-11, 2*1e-3)
    ax.grid(True)
    plt.subplots_adjust(bottom=0.2, left=0.2)
    plt.savefig('decay_example.pdf')

if __name__=='__main__':
    main()
