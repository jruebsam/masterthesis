import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import sys, os

def flow(x, pr, h1, h2, pmax):
    return -1/(2*pr)*pmax*(x**2 - x*(h1 + h2) + h1*h2)

def fd_o2(x, dx):
    return (x[2:] -2*x[1:-1] + x[:-2])/dx**2

def fd_o4(x, dx):
    return (-x[4:] + 16*x[3:-1] - 30*x[2:-2] + 16*x[1:-3] - x[:-4])/(12*dx**2)

def main():
    pmax, h1, h2, re = 10., 0, 1, 10.0
    pr = np.sqrt(0.125*pmax/re)
    vp_o2 = '/home/upgp/jruebsam/simulations/feb16/week2/3_vp_gc/data/nu_0.000010/o2/res_32'
    vp_o4 = '/home/upgp/jruebsam/simulations/feb16/week2/3_vp_gc/data/nu_0.000010/o4/res_32'
    df_o2 = '/home/upgp/jruebsam/simulations/feb16/week2/4_df_gc/data/o2/res_32'
    df_o4 = '/home/upgp/jruebsam/simulations/feb16/week2/4_df_gc/data/o4/res_32'



    pathes = [vp_o2, vp_o4, df_o2, df_o4]
    order = [2, 4, 2, 4]
    method = ['Vp.', 'Vp.', 'Df.', 'Df.']

    dx = 1/31.

    s1 = '''\\begin{tabular}[b]{ccccc}\\hline \n Method & Order $n$&  $\\Delta_n v_x(B)$ & $\\Delta_n v_x(R1) $& Error \\\\ \\hline'''
    s2 = '''\\end{tabular}\n'''
    l = [s1, '\n']

    for i, (path, o, m)  in enumerate(zip(pathes, order, method)):

        with tb.open_file(os.path.join(path, 'simulation.h5')) as d:
            vx = d.root.simdata.vx[-1, 4, 4]
            #vx = d.root.simdata.vx[-1, 4, 4, rs/2:(rs/2)+rs]
        #vx/=(10/(np.sqrt(0.125)))

        z = np.linspace(0, 1, len(vx))
        thflow = flow(z, pr, 0, 1, pmax)


        if o == 2:
            eo2 = fd_o2(vx, dx)
            b_er = eo2[11]
            r1_er = eo2[12]
        else:
            eo4 = fd_o4(vx, dx)
            b_er = eo4[10]
            r1_er = eo4[11]

        print ' : '.join([m, str(o), str(b_er), str(r1_er)])

        if i<3:
            l.append( ' & '.join([m, str(o), str(b_er), str(r1_er)])+ '\\\\  \n')
        else:
            l.append( ' & '.join([m, str(o), str(b_er), str(r1_er)])+ '\\\\ \\hline  \n')
    plt.legend()
    plt.show()

    l.append(s2)
    with open('table.tex', 'w') as f:
        for elem in l:
            f.write(elem)


if __name__=='__main__':
    main()
