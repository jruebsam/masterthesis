import matplotlib.pyplot as plt
import numpy as np
import os

def main():
    dpath = '/home/upgp/jruebsam/finaldata/noslip_validation/poiseuille_flow/1_default'

    labels = ['relative']
    #absolute identisch

    f = plt.figure()
    ax = f.add_subplot(111)

    o2_file = np.load(os.path.join(dpath, 'default_o2.npy'))
    res_o2, l2rel_o2, l2abs_o2 = o2_file.T

    o4_file = np.load(os.path.join(dpath, 'default_o4.npy'))
    res_o4, l2rel_o4, l2abs_o4 = o4_file.T

    ax.plot(res_o2, l2rel_o2, label='o2')
    ax.plot(res_o4, l2rel_o4, label='o4')

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel('gridpoints n')
    ax.set_ylabel('rel. l2-error')

    plt.legend()
    plt.grid()
    plt.show()

if __name__=='__main__':
    main()



