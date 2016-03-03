import matplotlib.pyplot as plt
import numpy as np
import os

def setup():
    plt.rcParams['text.latex.preamble']=[r"\usepackage{fourier}"]
    params = {'text.usetex' : True,
              'font.size' : 11,
              'font.family' : 'fourier',
              'text.latex.unicode': True,
              'axes.labelsize': 10,
              'font.size': 10,
              'legend.fontsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'figure.figsize': figsize(0.9)
              }
    plt.rcParams.update(params)

def figsize(scale):
    fig_width_pt = 448.13095 #from latex \the\textwidth
    inches_per_pt = 1.0/72.27
    golden_mean = (np.sqrt(5.0)-1.0)/2.0
    fig_width = fig_width_pt*inches_per_pt*scale
    fig_height = fig_width*golden_mean
    fig_size = [fig_width,fig_height]
    return fig_size

def newfig(width, hscale=1.):
    w, h =figsize(width)
    h*=hscale
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_subplot(111)
    return fig, ax

def savefig(filename):
    plt.savefig('{}.pdf'.format(filename))
