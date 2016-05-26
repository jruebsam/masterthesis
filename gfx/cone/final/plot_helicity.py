import style
style.setup()

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

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
markers = itertools.cycle('o^*')
from cycler import cycler

cc = itertools.cycle(plt.cm.spectral(np.linspace(0,1,10)))
#plt.rc('axes', prop_cycle=(cycler('color', cmap)))


def main():
    dpath1 = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_l2/'
    dpath2 = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_with_tip_l2/'

    rs = np.linspace(0, 0.5, 5)[::-1]
    cdir = os.getcwd()

    f, ax = style.newfig(0.9)
    # build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width + 0.5
    top = bottom + height

    l =  0.5*np.tan(np.pi/3.)
    h = radius = 0.25
    hs = rs

    l = ['Cone', 'Frustum']
    d = [dpath1, dpath2]


    for label, dpath in zip(l, d):
        os.chdir(os.path.join(dpath, 'data', 'h_%.3f' % radius))

        simpathes =  glob('*/*.ekin')
        simpathes =  glob('*/*.vb')

        omgs = sorted([float((x.split('/')[0]).split('_')[-1]) for x in simpathes])
        a_ekin, a_vz, a_vphi = [], [], []
        hells = []
        omgsn = []

        for i, simpath in enumerate(sorted(simpathes)):
            data = np.genfromtxt(simpath)
            time = data[:, 0]
            ekin = data[:, 1]
            hell   = data[:, 2]
            omgsn.append(omgs[i])
            #kp = int(len(hell)*0.75)
            hells.append( np.mean(hell))

        ax.plot(omgsn, hells, 'o-',  ms=3, mew=0, alpha=0.8, label=label)
    os.chdir(cdir)

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax.yaxis.set_major_formatter(formatter)

    ax.set_ylabel(r'$\left< H \right>$')
    ax.set_xlabel(r'$\omega$')

    ax.grid(True)
    #ax.set_ylim(0, 5*1e-4)
    ax.set_xlim(0.2, 2)
    plt.axvline(1, color='#e41a1c', lw=0.75, label=r'Crit.Slope $\alpha = \theta$')
    plt.axhline(0, color='k', lw=1.4)

    ax.legend(ncol = 1, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    plt.savefig('helicity.pdf')

if __name__=='__main__':
    main()
