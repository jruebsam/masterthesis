import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import os, sys

from glob import glob

def main():

    do2 = 'data/nu_0.001000/o2/res_100'
    do4 = 'data/nu_0.001000/o4/res_100'


    ds = [do2, do4]
    for p in ds:
        with tb.open_file(os.path.join(p, 'simulation.h5'), 'r') as d:
            vx = d.root.simdata.vx[-1]

        plt.plot(vx[8, 8, :])
    plt.show()

if __name__=='__main__':
    main()
