import style
style.setup()

import matplotlib.pyplot as plt
import numpy as np

import pycurb.analysis as pa
import tables as tb
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable

def main():
    fdir = '/home/upgp/jruebsam/simulations/mar16/week3/volfrac_validation/lowres/data'
    f, ax = style.newfig(0.45, 1.5)

    with tb.open_file(os.path.join(fdir, 'simulation.h5')) as d:
        h = d.root.icdata.H[:, :, 0]



    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.0)

    dx = 1/32.
    d = dx/2.

    im = ax.imshow(h.T, interpolation='nearest', origin='lower', extent=[0 -d, 1-d, 0 -d , 1 -d], cmap='seismic')
    plt.colorbar(im, cax=cax, label='H(x, y, z)')

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85)

    plt.savefig('mask_volfrac.pdf')



if __name__=='__main__':
    main()
