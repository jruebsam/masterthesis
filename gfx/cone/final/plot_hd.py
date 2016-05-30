import style as style
style.setup()
from glob import glob

from scipy.signal import argrelmax, argrelmin

from matplotlib import ticker
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import os, sys

def get_amp(x):
    maxids = argrelmax(x)[0][-2:]
    minids = argrelmin(x)[0][-2:]

    ids = np.sort(np.append(maxids, minids))

    amp = 0.5*(np.abs(x[ids[3]] - x[ids[2]]))
    old = 0.5*(np.abs(x[ids[1]] - x[ids[0]]))

    rel_error = np.abs(amp-old)/amp
    return amp, rel_error

cp = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

def main():
    path = '/home/upgp/jruebsam/simulations/mai16/week3'
    dirs = ['hd_series/data', 'hd_series/data',\
            'series_offset/data', 'series_offset/data']

    dirs = [os.path.join(path, x) for x in dirs]

    rs = np.array([0.0, 0.125])
    rs = np.append(rs, rs)

    cdir = os.getcwd()
    f, ax = style.newfig(0.9)

    for j, (r, dr) in enumerate(zip(rs, dirs)):
        os.chdir(os.path.join(dr, 'h_%.3f' % r))
        #c = 'k^-'
        cd = os.getcwd()

        simpathes =  glob('*/*.ekin')

        a_ekin, a_vz, a_vphi = [], [], []
        omgs = []
        hells = []
        for i, simpath in enumerate(sorted(simpathes)):
            omg = float((simpath.split('/')[-2]).split('_')[1])
            if omg>=0.8:
                data = np.genfromtxt(simpath)
                time = data[:, 0]
                vz   = data[:, -3]
                amp,_ = get_amp(vz)
                a_vz.append(amp)
                omgs.append(omg)



        ms, lw, mew = 4, 0.8, 0
        if (j==0) or (j==2):
            c = cp[0] if 'hd' in dr else cp[1]
            lab = r'$\Delta x = 1/256$' if 'hd' in dr else r'$\Delta x = 1/128$'
            lab = r'$h_+=0$; ' + lab
            ax.plot(omgs, a_vz, 'o-', color = c, ms=ms, lw=lw,mew=mew, label=lab)
        else:
            c = cp[3] if 'hd' in dr else cp[4]
            lab = r'$\Delta x = 1/256$' if 'hd' in dr else r'$\Delta x = 1/128$'
            lab = r'$h_+=0.125$; ' + lab
            ax.plot(omgs, a_vz, 'o-', color=c,  ms=ms, lw=lw, mew=mew, label=lab)

        os.chdir(cdir)

    plt.legend(ncol = 2, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    ax.set_xlabel(r'\omega')
    ax.set_ylabel(r'$A(\left<v_z^2\right>)$')

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3,-2))

    ax.legend(ncol = 2, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.25),
           fancybox=True, shadow=True)

    ax.yaxis.set_major_formatter(formatter)

    ax.grid(True)
    plt.subplots_adjust(top=0.8, bottom =0.15)

    ax.grid(True)
    plt.subplots_adjust(bottom=0.1)
    plt.savefig('hd_comparison.pdf')

if __name__=='__main__':
    main()

