import style
style.setup()

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import tables as tb

from custommap import bipolar
from mpl_toolkits.axes_grid1 import make_axes_locatable

def main():
    dpath = '/home/upgp/jruebsam/simulations/mai16/week2/move_border/data'

    f, axes = plt.subplots(1, 3, figsize=style.figsize(1, 0.3))
    c = bipolar(neutral=0, lutsize=1024)

    omgs = [1.3, 1.2, 1.1]
    walls = [0.0, 0.125, 0.25]

    for i, (ax, wall, omg) in enumerate(zip(axes, walls, omgs)):
        dp = os.path.join(dpath, 'wall_%.3f' % wall, 'omg_%.2f' % omg, 'gfx')

        n = 200
        with tb.open_file(os.path.join(dp, '%08i.h5' % n)) as d:
            vz = d.root.xz.vz[:]

        #vz = vz/np.abs(vz)

        cm = ax.imshow(vz.T, origin='lower', cmap = c, extent=[0, 1,0,1])

        if i == 0:
            ax.set_ylabel(r'z')
            ax.set_yticks([0, 1])
            ax.yaxis.labelpad = -5
        else:
            ax.yaxis.set_major_locator(plt.NullLocator())

        ax.set_xlabel(r'x')
        ax.set_xticks([0, 1])
        ax.xaxis.labelpad = -10
        print wall
        ax.set_title(r'r=%.3f' % (0.5 - wall))
        r = 0.5 - wall
        ax.plot(0.5, r/(0.5 + r), 'w+', ms=4 )



    divider = make_axes_locatable(axes[-1])
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cbar = plt.colorbar(cm, cax=cax)
    #cbar = f.colorbar(cax, shrink=0.8)
    cbar.set_label(r'$\frac{v_z}{|v_z|}$', fontsize=12)

    plt.subplots_adjust(wspace=0.01, left=0.1, bottom =0.15)

    #plt.show()
    plt.savefig('phase.pdf')




if __name__=='__main__':
    main()
