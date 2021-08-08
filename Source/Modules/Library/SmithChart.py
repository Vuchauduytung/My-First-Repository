import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.core.numbers import I
import sympy.solvers as solv
import matplotlib.pyplot as plt
from scipy.special import factorial
    
def get_gm_isometric_equation(gamma_module):
    """
        @ Brief:    Find the locus equation of the isometric line of the reflectance according to the value
                    of the impedance at that point
        @ Param:    gamma_module: Thhe magnitude of the reflectance
        @ Retval:   gamma_module_locus_function: The desired locus equation
    """
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
    """
        @ Brief:    Calculate the imaginary part value of the impedance at the point with real part and the
                    relation equation between real and imaginary part, and the real part value of the given impedance
        @ Param:    
                    function: Relation equation between real and imaginary part
                    real_path: Value of the given real part
        @ Retval:   img_path: Value of the imaginary part
    """
    a, b = symbols('a b', real=True)
    try:
        img_path = solv.solve(funtion.subs(a, real_path), b)
    except Exception as err:
        print("An error occurred while finding the intersection between constant gamma's module and constants real impedance locus")
        print(err)
        img_path = None
    return img_path

def get_Smith_constant_gamma_module_locus(gamma_module):
    """
        @ Brief:    Create 2 vectors that contain the magnitude and argument values (complex number)
                    with argument ranging from -pi to pi and magnitude is the repeating vector of the given value
                    2 Vectors creat a circle with radius r, phase phi (polar form)
        @ Param:    gamma_module: Thhe magnitude of the reflectance
        @ Retval:   
                    r: Radius
                    phi: Phase angle
        
    """
    r = np.repeat(gamma_module, 360)
    phi = np.linspace(- np.pi, np.pi, num = 360)
    return r, phi

def get_Smith_constant_realpath_locus(real_value):
    """
        @ Brief:    Create 2 vectors contain the magnitude and argument values of the reflectance given 
                    the condition that Z=a+bj is the impedance at the considering point and a is a given value
                    and b is within a specified range
        @ Param:    real_value: Real part value of Z
        @ Retval:   
                    r: Radius
                    phi: Phase angle
        @ Description:  This function has a built-in ability to predict the trend of the phase angle for drawing Smith chhart
    """
    a = np.repeat(real_value, 360)
    b = np.linspace(-10, 10, num = 360)
    c = (a**2 + b**2 - 1)/((a+1)**2 + b**2)
    d = ((2*b)/((a+1)**2 + b**2)) 
    r = np.sqrt(c**2 + d**2)
    phi = np.arctan(d/c)
    for index in range(len(phi)-1):
        while phi[index] > np.pi:
            phi[index : ] -= 2*np.pi
        while phi[index] < -np.pi:
            phi[index : ] += 2*np.pi
        while abs(phi[index]-phi[index+1]) >= np.pi/2:
            if phi[index+1] > phi[index]:
                phi[index+1 : ] -= np.pi
            else:
                phi[index+1 : ] += np.pi
        if phi[index+1] < -np.pi/2:
            if index > 180:
                phi[index+1 : ] += np.pi
    return r, phi
