import style
style.setup()

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.latex.preamble']=r'\makeatletter \newcommand*{\rom}[1]{\expandafter\@slowromancap\romannumeral #1@} \makeatother'
plt.rcParams.update()

import os, sys
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it
import itertools
from scipy import optimize
import matplotlib.cm as cmx
from matplotlib import colors

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
markers = itertools.cycle('oh^*')

from cycler import cycler
cc = cycler('color', ['r', 'g', 'b', 'y'])
#cc = itertools.cycle(plt.cm.spectral(np.linspace(0,1,10)))
#plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def get_amp(series):
    n = len(series)/4
    data = series[3*n:]
    A = 0.5*(np.max(data)-np.min(data))
    return A

def main():
    dpath = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/'


    f, ax = style.newfig(1., 1.2)

    axins = zoomed_inset_axes(ax, 10., loc=2)
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    for axis in ['top','bottom','left','right']:
        axins.spines[axis].set_linewidth(0.4)
    axins.set_xticks([])
    axins.set_yticks([])

    axins2 = zoomed_inset_axes(ax, 5, loc=1)
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    for axis in ['top','bottom','left','right']:
        axins2.spines[axis].set_linewidth(0.4)
    axins2.set_xticks([])
    axins2.set_yticks([])


    modes = list(it.product(['df', 'vp', 'dffrac', 'vpfrac'], [1, 0]))
    labels = list(it.product(['DF', 'VP', 'DF-Vol.Frac.', 'VP-Vol.Frac'], ['o2', 'o4']))

    labels = [' '.join([x[0], x[1]]) for x in labels]

    jet = plt.get_cmap('jet')
    values = range(8)
    cNorm  = colors.Normalize(vmin=0, vmax=8)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    for idx, ((method, order), label) in enumerate(zip(modes, labels)):
        on = 'o2' if order else 'o4'
        a_ekin, a_vz, a_vphi = [], [], []
        omgs = []
        omgfs = np.arange(0.2, 2.1, 0.1)
        omgs = omgfs

        for omgf in omgfs:
            var_path = os.path.join(method, on, 'omg_{}'.format(omgf))
            sim_path = os.path.join(dpath, "data", var_path)

            dp = os.path.join(sim_path, '.'.join([sim_path.split('/')[-1], 'ekin']))
            simpath = dp
            try:
                data = np.genfromtxt(dp)
                time = data[:, 0]
                ekin = data[:, 1]
                vz   = data[:, -3]
                vphi = data[:, -1]
                #ax.plot(time, vz, label=simpath)
                a_ekin.append(get_amp(ekin))
                a_vz.append(get_amp(vz))
                a_vphi.append(get_amp(vphi))
            except:
                a_ekin.append(0)
                a_vz.append(0)
                a_vphi.append(0)


            #plt.plot(time, vz, label=simpath.split('/')[-1])
        print a_vz
        mks = markers.next()
        ds = (1., 2., 3., 2.)

        col = scalarMap.to_rgba(values[idx])
        if method == 'df' and on == 'o2':
            ax.plot(omgs, np.sqrt(a_vz), mks+'--', color=col, ms=4, mew=0.6, lw=0.8, alpha =0.8,
                    label=label, markerfacecolor='None', dashes=ds )

            axins.plot(omgs, np.sqrt(a_vz), mks+'--', color=col, ms=4,
                            mew=0.6, lw=0.5, alpha =0.8, markerfacecolor='None' , dashes=ds )
            axins2.plot(omgs, np.sqrt(a_vz), mks+'--', color=col, ms=4,
                            mew=0.6, lw=0.5, alpha =0.8, markerfacecolor='None' , dashes=ds )
        else:
            ax.plot(omgs, np.sqrt(a_vz), mks+'--', color=col, ms=4, mew=0, lw=0.5, alpha =0.8,
                    label= label, dashes=ds )

            axins.plot(omgs, np.sqrt(a_vz), mks+'--', color=col, ms=4,
                            mew=0, lw=0.5, alpha =0.8, dashes=ds )
            axins2.plot(omgs, np.sqrt(a_vz), mks+'--', color=col, ms=4,
                            mew=0, lw=0.5, alpha =0.8, dashes=ds )
        #plt.plot(omgs, a_vphi, 'ro--')
        #plt.plot(omgs, a_ekin, 'go--')

    axins.set_xlim(0.78, 0.82)
    axins.set_ylim(0.011, 0.014)
    mark_inset(ax, axins, loc1=1, loc2=4, fc="none", ec="0.5", lw=0.5)

    axins2.set_xlim(1.18, 1.22)
    axins2.set_ylim(0.032, 0.037)
    mark_inset(ax, axins2, loc1=2, loc2=3, fc="none", ec="0.5", lw=0.5)

    ax.set_ylim(0., 0.04)
    ax.set_xlim(0.15, 2.05)
    ax.set_xlabel(r'$\omega$')
    ax.set_ylabel(r'$A\left(\left<v_z^2\right>\right)$')
    ax.legend(ncol = 3, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.2),
           fancybox=True, shadow=True)

    ap=dict(arrowstyle='-|>' , facecolor='black', lw=0.8
            )
    kw=dict(size=10., horizontalalignment='center', verticalalignment='bottom')

    ax.annotate(r'(\rom{1})', xy=(1.2, 0.015),
                xytext=(1.2, 0.0002), arrowprops=ap, **kw)

    ax.annotate(r'(\rom{2})', xy=(0.75, 0.01),
                xytext=(0.75, 0.0002),  arrowprops=ap, **kw)

    ax.annotate(r'(\rom{3})', xy=(1.7, 0.01),
                xytext=(1.7, 0.0002),  arrowprops=ap, **kw)
    plt.subplots_adjust(top=0.85, bottom =0.1)

    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax.yaxis.set_major_formatter(formatter)


    ax.grid(True)
    plt.savefig('cylinder.pdf')

if __name__=='__main__':
    main()
