import numpy as np
from sympy import Matrix, diff, eye, sin, symbols, zeros


def riemann_curvature_tensor(list2d, syms):
    """
    Function to calculate Riemann Curvature Tensor of a given metric

    Parameters
    ----------
    list2d : list
        d list (Matrix) representing metric, containing ~sympy expressions
    syms : list
        1d list containing representaion of [x0,x1,x2...] in ~sympy expressions

    Returns
    -------
    list
        4d list of ~sympy expressions containing components of Riemann Tensor

    """
    christs = christoffels(list2d, syms)
    dims = len(syms)
    riemann_list = (np.zeros(shape=(dims, dims, dims, dims), dtype=int)).tolist()
    _counterlist = [i for i in range(dims ** 4)]
    for i in _counterlist:
        # t,s,r,n each goes from 0 to (dims-1)
        # hack for codeclimate. Could be done with 4 nested for loops
        n = i % dims
        r = (int(i / dims)) % (dims)
        s = (int(i / (dims ** 2))) % (dims)
        t = (int(i / (dims ** 3))) % (dims)
        temp = diff(christs[t][s][n], syms[r]) - diff(christs[t][r][n], syms[s])
        for p in range(dims):
            temp += (christs[p][s][n] * christs[t][p][r]) - christs[p][r][n] * christs[
                t
            ][p][s]
        riemann_list[t][s][r][n] = temp
    return riemann_list


def christoffels(list2d, syms):
    """
    Function to calculate christoffel symbols of a given metric

    Parameters
    ----------
    list2d : list
        2d list (Matrix) representing metric, containing ~sympy expressions
    syms : list
        1d list containing representaion of [x0,x1,x2...] in ~sympy expressions

    Returns
    -------
    list
        3d list of ~sympy expressions containing christoffel symbols

    """
    dims = len(syms)
    christlist = (np.zeros(shape=(dims, dims, dims), dtype=int)).tolist()
    mat = Matrix(list2d)
    mat_inv = mat.inv()
    _counterlist = [i for i in range(dims ** 3)]
    for t in _counterlist:
        # i,j,k each goes from 0 to (dims-1)
        # hack for codeclimate. Could be done with 3 nested for loops
        k = t % dims
        j = (int(t / dims)) % (dims)
        i = (int(t / (dims ** 2))) % (dims)
        temp = 0
        for n in range(dims):
            temp += (mat_inv[i, n] / 2) * (
                diff(list2d[n][j], syms[k])
                + diff(list2d[n][k], syms[j])
                - diff(list2d[j][k], syms[n])
            )
        christlist[i][j][k] = temp
    return christlist


def schwarzschild_christoffels(symbolstr="t r theta phi"):
    """Returns the 3d list of christoffel symbols of Schwarzschild Metric."""
    list2d = [[0 for i in range(4)] for i in range(4)]
    syms = symbols(symbolstr)
    c, a = symbols("c a")
    list2d[0][0] = 1 - (a / syms[1])
    list2d[1][1] = -1 / ((1 - (a / syms[1])) * (c ** 2))
    list2d[2][2] = -1 * (syms[1] ** 2) / (c ** 2)
    list2d[3][3] = -1 * (syms[1] ** 2) * (sin(syms[2]) ** 2) / (c ** 2)
    return christoffels(list2d, syms)
