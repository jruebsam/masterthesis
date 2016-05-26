import numpy as np
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os, sys

from glob import glob
from scipy.signal import argrelextrema


def main():
    hs = np.linspace(0, 0.5, 5)
    cdir = os.getcwd()

    maxima = [(1.45, 1.1), (1.35, 1.0), (1.25, 0.9), (1.15, 0.8), (1.05, 0.75)]
    hss  = np.linspace(0, 0.5, 5)

    cone     = "/home/upgp/jruebsam/simulations/mai16/week5/2_relaxation_neu/data/cone/"
    frustum  = "/home/upgp/jruebsam/simulations/mai16/week5/2_relaxation_neu/data/frustum/"

    pathes = [cone, frustum]

    tend = 150.

    f, axes = plt.subplots(1, 5)#, sharex=True, sharey=True)
    colors = ['ro--', 'bo--', 'yo-', 'go--', 'mo--']

    f = lambda x, a, b : a*x + b

    for ax, maxi, h  in zip(axes, maxima, hss):
        #for ax, omg in zip(axi, maxi):
        omg = maxi[0]
        for i, path in enumerate(pathes):
            vp = os.path.join('h_%.3f' % h, 'omg_%.2f' % omg, ('omg_%.2f' % omg) + '.ekin')
            ddir = os.path.join(path, vp)
            data = np.genfromtxt(ddir)
            time = data[:, 0]
            ekin = data[:, 1]
            vz   = data[:, -3]

            b = time < 30

            ax.plot(time[b], vz[b], label=h)
            popt, pcov = curve_fit(f, time[b], np.log(vz[b]))
            perr = np.sqrt(np.diag(pcov))

            xdata = np.linspace(0, 50, 100)
            ydata = np.exp(f(xdata, *popt))
            ax.plot(xdata, ydata, 'r--', label=r'$\lambda: %.3f : \sigma: %.3f$' % (popt[0], perr[0]))
            ax.legend()

        ax.set_yscale('log')

    plt.show()

if __name__=='__main__':
    main()
