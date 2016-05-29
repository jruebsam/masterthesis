import style
style.setup()

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import tables as tb

from custommap import bipolar
from mpl_toolkits.axes_grid1 import make_axes_locatable

def main():
    dp = '/home/upgp/jruebsam/simulations/mai16/week5/2_relaxation_neu/data/cone/h_0.250/omg_1.25/gfx/'

    f, axes = plt.subplots(1, 3, figsize=style.figsize(1, 0.3))
    c = bipolar(neutral=0, lutsize=1024)

    times = [0, 200, 500]

    with tb.open_file(os.path.join(dp, '%08i.h5' % times[0])) as d:
        vz = d.root.xz.vz[:]
    lim = np.max(np.abs(vz))

    for i, (ax, time) in enumerate(zip(axes, times)):

        with tb.open_file(os.path.join(dp, '%08i.h5' % time)) as d:
            vz = d.root.xz.vz[:]

        #vz = vz/np.abs(vz)
        lim = np.max(np.abs(vz))
        cm = ax.imshow(vz.T, origin='lower', cmap = c, extent=[0, 1,0,1], vmin=-lim, vmax=lim)

        if i == 0:
            ax.set_ylabel(r'z')
            ax.set_yticks([0, 1])
            ax.yaxis.labelpad = -5

            labels = [item.get_text() for item in ax.get_yticklabels()]
            labels[1] = '1.25'
            labels[0] = '0'
            ax.set_yticklabels(labels)
        else:
            ax.yaxis.set_major_locator(plt.NullLocator())

        ax.set_xlabel(r'x')
        ax.set_xticks([0, 1])
        ax.xaxis.labelpad = -5
        ax.set_title(r'$t=%i$' % (time/10))

    divider = make_axes_locatable(axes[-1])
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cbar = plt.colorbar(cm, cax=cax)
    #cbar = f.colorbar(cax, shrink=0.8)
    cbar.set_label(r'$\propto v_z$', fontsize=12)
    cbar.set_ticks([])



    plt.subplots_adjust(wspace=0.01, left=0.1, bottom =0.15)

    #plt.show()
    plt.savefig('phase_decay.pdf')




if __name__=='__main__':
    main()
