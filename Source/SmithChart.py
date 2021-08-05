import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.core.numbers import I
import sympy.solvers as solv
import matplotlib.pyplot as plt
from scipy.special import factorial

def plot_Smith(a_vector, b_vector, color, fig = None, ax = None):
    a, b, c, d = symbols('a b c d', real=True)
    c = (a**2 + b**2 - 1)/((a+1)**2 + b**2)
    d = ((2*b)/((a+1)**2 + b**2))  
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
    ax.plot(phi_plt, r_plt, color = color)
    plt.show()
    return fig, ax
    
def constant_module_gamma_function(gamma_module):
    if gamma_module > 1:
        print("Reflection coefficient's module can not larger 1")
        return None
    a, b = symbols('a b', real=True)
    c = (a**2 + b**2 - 1)/((a+1)**2 + b**2)
    d = ((2*b)/((a+1)**2 + b**2))  
    r = sqrt(c**2 + d**2)
    gamma_module_locus_function = Eq(r, gamma_module)
    return gamma_module_locus_function

def find_cmg_cri_intersection(funtion, real_path):
    a, b = symbols('a b', real=True)
    try:
        img_path = solv.solve(funtion.subs(a, real_path), b)
    except Exception as err:
        print("An error occurred while finding the intersection between constant gamma's module and constants real impedance locus")
        print(err)
        img_path = None
    return img_path

def get_Smith_constant_gamma_module_locus(gamma_module, color = None, fig = None, ax = None):
    r = np.repeat(gamma_module, 360)
    phi = np.linspace(- np.pi, np.pi, num = 360)
    # if fig is None and ax is None:
    #     fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # ax.plot(phi, r, color = color)
    # plt.show()
    return r, phi

def get_Smith_constant_realpath_locus(real_value, color = None, fig = None, ax = None):
    # if fig is None and ax is None:
    #     fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    a = np.repeat(real_value, 360)
    b = np.linspace(-10, 10, num = 360)
    c = (a**2 + b**2 - 1)/((a+1)**2 + b**2)
    d = ((2*b)/((a+1)**2 + b**2)) 
    r = np.sqrt(c**2 + d**2)
    phi = np.arctan(d/c)
    for index in range(len(phi)-1):
        while abs(phi[index]-phi[index+1]) >= np.pi/2:
            if phi[index+1] > phi[index]:
                phi[index+1:] -= np.pi
            else:
                phi[index+1:] += np.pi
    # ax.plot(phi, r)
    # plt.show()
    return r, phi
