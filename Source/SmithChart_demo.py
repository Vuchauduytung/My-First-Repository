import cmath
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.core.numbers import I
from sympy.plotting import plot, plot_implicit
a, b, c, d = symbols('a b c d', real=True)
c = (a**2 + b**2 - 1)/((a+1)**2 + b**2)
d = ((2*b)/((a+1)**2 + b**2))  
a_vector = np.repeat(0.1, 50)
b_vector = np.linspace(-4, 16, num = 50)
# r_vector = np.repeat(2, 50)
# ang_vector = np.linspace(0, 0.9*np.pi, num = 50)
r_ = sqrt(c**2 + d**2)
phi_ = atan(d/c)
for i in range(50):
    r = r_.subs([(a, a_vector[i]), (b, b_vector[i])])
    phi = phi_.subs([(a, a_vector[i]), (b, b_vector[i])])
    if phi > np.pi:
        phi -= np.pi
    elif phi < -np.pi:
        phi += np.pi

    try:
        r_plt = np.append(r_plt, r)
    except:
        r_plt = np.array(r)
    try:
        old_phi = phi_plt[-1]
        possible_phi = np.array([phi, phi + np.pi])
        while possible_phi[0] > old_phi:
            possible_phi -= np.pi
        while old_phi > possible_phi[1]:
            possible_phi += np.pi
        delta_phi = possible_phi - old_phi
        abs_delta_phi = np.absolute(delta_phi)
        index_min = np.argmin(abs_delta_phi)
        phi__ = possible_phi[index_min]
        while phi__ < -np.pi:
            phi__ += 2*np.pi
        while phi__ > np.pi:
            phi__ -= 2*np.pi
        phi_plt = np.append(phi_plt, phi__)
    except:
        phi_plt = np.array([phi])

debug = True
plt.polar(phi_plt, r_plt)
plt.show()

