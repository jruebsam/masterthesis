import style
style.setup()

import numpy as np
import os
import matplotlib.pyplot as plt
from collections import OrderedDict

plt.rcParams['text.latex.preamble']=r'\makeatletter \newcommand*{\rom}[1]{\expandafter\@slowromancap\romannumeral #1@} \makeatother'
plt.rcParams.update()

from matplotlib import ticker
from scipy.signal import argrelmin, argrelmax

def get_amp(x):
    maxids = argrelmax(x)[0][-2:]
    minids = argrelmin(x)[0][-2:]

    ids = np.sort(np.append(maxids, minids))

    amp = 0.5*(np.abs(x[ids[3]] - x[ids[2]]))
    old = 0.5*(np.abs(x[ids[1]] - x[ids[0]]))

    rel_error = np.abs(amp-old)/amp
    return amp, rel_error

def main():
    dpath1 = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_l2/'
    dpath2 = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_with_tip_l2/'


    m8  = [0.7, 0.8, 0.85, 0.9, 0.95][::-1]

    m1  = [1.45, 1.35, 1.25, 1.15, 1.05]
    m2  = [1.10, 1.00, 0.90, 0.80, 0.75]
    m3  = [0.70, 0.60, 0.50, 0.45, 0.40]


    hs = np.linspace(0, 0.5, 5)

    f, (ax1, ax2) =  plt.subplots(1, 2, figsize=style.figsize(0.9, 0.4))
    cdir = os.getcwd()

    modes = {1 : m1, 2 : m2 , 3: m3 , 8 : m8}
    modes = OrderedDict(sorted(modes.items(), key=lambda t: t[0]))
    print modes

    for key, mode in modes.iteritems():
        if key == 8:
            dpath = dpath2
        else:
            dpath = dpath1

        amps = []
        for h, m in zip(hs, mode):
            hpath = os.path.join(dpath, 'data', 'h_%.3f' % h)
            sim_path = os.path.join(hpath, 'omg_%.2f' % m,'omg_%.2f.ekin' % m)

            data = np.genfromtxt(sim_path)
            vphi = data[:, -1]
            vz   = data[:, -3]
            amp, _ = get_amp(vz)
            amps.append(amp)

        ax1.plot(hs, amps, 'o-',  ms=3, mew=0, alpha=0.8, label=r'(\rom{%i})' % key)
        ax2.plot(hs, mode, 'o-',  ms=3, mew=0, alpha=0.8)
    ax1.grid()
    ax2.grid()
    ax2.yaxis.tick_right()

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax1.yaxis.set_major_formatter(formatter)

    ax2.yaxis.set_label_position("right")

    ax1.set_xlabel(r'$h_+$')
    ax2.set_xlabel(r'$h_+$')
    ax1.set_ylabel(r'$A\left(\left<v_z^2\right>\right)$')
    ax2.set_ylabel(r'$\omega$')

    ax1.legend(ncol = 4, fontsize=8, loc='upper center', bbox_to_anchor=(1.1, 1.3),
           fancybox=True, shadow=True)
    plt.subplots_adjust(top=0.8, bottom =0.15)

    plt.legend()
    plt.savefig('amp_pos.pdf')



if __name__=='__main__':
    main()

