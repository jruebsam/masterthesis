import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import matplotlib.colors as colors
import matplotlib.cm as cmx

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#datafrom : /home/upgp/jruebsam/remake_sim/poiseuille_flow/o4_highres

def sort_by_re(re, err):
    sorted_lists= sorted(zip(re, err), key=lambda x: x[0])
    re, err = [[x[i] for x in sorted_lists] for i in range(2)]
    return re, err

def main():
    fpath = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(fpath, '..')

    with open('data/vp_o4hd/l2rel.pkl', 'rb') as f:
        l2reld =  pickle.load(f)

    res, l2rel = [], []
    for (re, nu), error in l2reld.iteritems():
        if nu==1e-4:
            l2rel.append(error)
            res.append(re)
    res, l2rel = sort_by_re(res, l2rel)
    res, l2rel = np.array(res), np.array(l2rel)



    d = np.load('data/direct_forcing/dfo4.npy')
    dfre, dfl2rel, dfl2abs = d.T

    d = np.load('data/direct_forcing/dfo2.npy')
    dfreo2, dfl2relo2, dfl2abso2 = d.T


    plt.plot(res, l2rel, 'o--', label=r'V.P. with $\nu=1e-4$')
    plt.plot(dfre, dfl2rel, 'o--', label='direct forcing O4')
    plt.plot(dfreo2, dfl2relo2, 'o--', label='direct forcing O2')

    plt.xlabel(r'$Re$')
    plt.ylabel(r'$l_2$-Fehler')

    plt.legend()
    plt.ylim(-0.001, 0.016)

    #plt.show()
    plt.savefig('/'.join([outpath, 'dfo2o4.png']), dpi=300)



if __name__=='__main__':
    main()
