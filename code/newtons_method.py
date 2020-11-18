# Choomno Moos
# Oct 29, 2020

import numpy as np
import scipy.linalg as la

x_0 = [-1,1,1]

def f(x_1,x_2,x_3):
    return np.array([x_1 + 2*x_2 - 3*x_3 + 3,
                     x_1**2 + 4*x_2**2 - 4*x_3,
                     x_1**2 - x_2**2 - x_3**2])

def J(x_1,x_2,x_3):
    return np.array([[1,2,-3],
                     [2*x_1,8*x_2,-4],
                     [2*x_1,-2*x_2,-2*x_3]])

def iterate_newton(x_old):
    Delta_x_n = la.solve(J(x_old[0],x_old[1],x_old[2]),
                         -f(x_old[0],x_old[1],x_old[2]))
    x_new = x_old + Delta_x_n
    return x_new

x = x_0
for i in range(10):
    print(x)
    x_old = x
    x = iterate_newton(x)
    if (x[0] == x_old[0] and x[1] == x_old[1] and x[2] == x_old[2]):
        break