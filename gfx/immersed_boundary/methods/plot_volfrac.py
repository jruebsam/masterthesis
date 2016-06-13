import style
style.setup()

import matplotlib.pyplot as plt
import numpy as np

import pycurb.analysis as pa
import tables as tb
import os

def main():
    fdir = '/home/upgp/jruebsam/simulations/mar16/week3/volfrac_validation'
    f, ax = style.newfig(0.45, 1.5)

    files = sorted(os.listdir(os.path.join(fdir, 'data')),
            key = lambda x: int(x.split('_')[-1]))[1:]

    files = [os.path.join(fdir, 'data',  x) for x in files]

    samples, masks = [], []
    for f in files:
        with tb.open_file(os.path.join(f, 'simulation.h5')) as d:
            h = d.root.icdata.H[:, :, 0]
        samples.append(int(f.split('_')[-1]))
        masks.append(h)

    best = masks[-1]

    error = np.zeros(len(samples))
    b = best>0
    for i, mask in enumerate(masks):
        error[i] = pa.l2_error(mask, exact=best)
        #error[i] = np.mean(np.abs(mask[b]-best[b])/np.abs(best[b]))

    plt.plot(samples, error, 'bo--', ms=4, mew = 0.2, alpha=0.7)
    plt.xlabel('Samples N')
    plt.ylabel('rel. $l_2$-error')

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.grid()

    plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85)
    plt.savefig('error_volfrac.pdf')



if __name__=='__main__':
    main()
