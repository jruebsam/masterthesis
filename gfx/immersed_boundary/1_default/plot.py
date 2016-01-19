import matplotlib as mpl
import numpy as np
import os
mpl.use('pgf')

from scipy import optimize

def figsize(scale):
    fig_width_pt = 448.13095 #from latex \the\textwidth
    inches_per_pt = 1.0/72.27
    golden_mean = (np.sqrt(5.0)-1.0)/2.0
    fig_width = fig_width_pt*inches_per_pt*scale
    fig_height = fig_width*golden_mean
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": figsize(0.9),     # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }
mpl.rcParams.update(pgf_with_latex)
import matplotlib.pyplot as plt

def newfig(width):
    fig = plt.figure(figsize=figsize(width))
    ax = fig.add_subplot(111)
    return fig, ax

def savefig(filename):
    plt.savefig('{}.pgf'.format(filename))
    plt.savefig('{}.pdf'.format(filename))

def main():
    dpath = '/home/upgp/jruebsam/finaldata/noslip_validation/poiseuille_flow/1_default'

    labels = ['relative'] #absolute identisch zu absolut

    f, ax = newfig(0.8)

    o2_file = np.load(os.path.join(dpath, 'default_o2.npy'))
    res_o2, l2rel_o2, l2abs_o2 = o2_file.T

    o4_file = np.load(os.path.join(dpath, 'default_o4.npy'))
    res_o4, l2rel_o4, l2abs_o4 = o4_file.T


    fitfunc = lambda p, x: p[0]*x**p[1]
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    p0 = [1., -2]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(res_o4, l2rel_o4))

    xn = np.linspace(7, 160, 200)
    yn = fitfunc(p1, xn)

    ax.plot(res_o2, l2rel_o2, 'o--', label='o2')
    ax.plot(res_o4, l2rel_o4, 'o--', label='o4')
    ax.plot(xn, yn, label='fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1])

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(r'gridpoints $N$')
    ax.set_ylabel(r'relative $l_2$-error')

    ax.set_xlim(5, 200)
    ax.set_ylim(1e-10, 1e-1)

    plt.legend()
    plt.grid()
    plt.tight_layout()
    #plt.show()
    savefig('relative_l2error')

if __name__=='__main__':
    main()



