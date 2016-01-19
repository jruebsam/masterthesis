import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import matplotlib.colors as colors
import matplotlib.cm as cmx

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#datafrom : /home/upgp/jruebsam/remake_sim/poiseuille_flow/o4_highres

def main():
    fpath = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(fpath, '..')

    with open('data/vp_o4hd/l2abs.pkl', 'rb') as f:
        l2abs =  pickle.load(f)
    with open('data/vp_o4hd/l2rel.pkl', 'rb') as f:
        l2rel =  pickle.load(f)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
    plot_l2(ax1, l2abs, 1)
    plot_l2(ax2, l2rel, 2)

    plt.subplots_adjust(wspace=0.5)
    plt.show()
    #plt.savefig('/'.join([outpath, 'vp_error.png']), dpi=300)

def plot_l2(ax, l2, plotnr):

    nus, res, errors = [], [], []
    for (re, nu), error in l2.iteritems():
        nus.append(nu)
        res.append(re)
        errors.append(error)
    nus, res, errors = np.array(nus), np.array(res), np.array(errors)


    allnus = sorted(list(set(list(nus))))
    allres = sorted(list(set(list(res))))
    values = range(len(allnus))
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=len(allnus))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    scatters = []
    for idx, re in enumerate(allres):
        b = (res == re)
        colorVal = scalarMap.to_rgba(values[idx])
        ax.plot(nus[b], errors[b], 'o', color=colorVal, label=r'$Re=%i$' % re)

    inset = inset_axes(ax, width="50%", height="50%", loc=2)
    for idx, nu in enumerate(allnus):
        b = (nus == nu)
        inset.scatter(nus[b], errors[b], c=res[b])

    ax.set_xlabel(r'$\nu$')

    if plotnr==1:
        inset.set_xlim(0.9*1e-5, 1.1*1e-3)
        inset.set_ylim(0.25, 2.0)
        ax.set_ylabel(r'$l_2$-error abs.')
    else:
        inset.set_xlim(0.9*1e-5, 1.1*1e-3)
        inset.set_ylim(0.0, 0.035)
        ax.set_ylabel(r'$l_2$-error rel.')
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
    inset.yaxis.tick_right()
    inset.yaxis.set_label_position("right")

    inset.set_xscale('log')
    ax.set_xlim(np.min(allnus)*0.5, np.max(allnus)*1.5)
    dx = 0.1*np.abs(np.max(errors)- np.abs(np.min(errors)))
    ax.set_ylim(-dx, np.max(errors)+dx)

    ax.set_xscale('log')
    if plotnr==2:
        ax.legend( loc='center', bbox_to_anchor=(-0.25, 0.5))

if __name__=='__main__':
    main()
