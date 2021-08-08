from sympy import *
import numpy as np
from cmath import *


class SmithPoint:
    
    
    def __init__(self, name, line_impedance = None, impedance = None, admittance = None, gamma = None, Nomalize = False):
        
        if line_impedance is None:
            raise Exception('Parameter missing: line_impedance')
        self.name = name
        self.Z0_val= line_impedance
        
        self.Z0 = Symbol('Z0')
        self.Z = Symbol('Z' + name)
        self.Y = Symbol('Y' + name)
        self.Gamma = Symbol('\u0393' + name)
        self.z = Symbol('z' + name)
        self.y = Symbol('y' + name)
               
        self.Z_y = 1/self.Y
        self.Z_g = self.Z0*(1+self.Gamma)/(1-self.Gamma)
        self.Y_z = 1/self.Z
        self.Y_g = self.Y_z.subs(self.Z, self.Z_g)
        self.Gamma_z = (-self.Z0 + self.Z)/(self.Z0 + self.Z)
        self.Gamma_y = self.Gamma_z.subs(self.Z, self.Z_y)
        
        if Nomalize:
            try:
                impedance *= line_impedance
            except TypeError:
                pass    
            try:
                admittance /= line_impedance
            except TypeError:
                pass 
        
        if impedance is not None:
            self.Y_val = complex(self.Y_z.subs([
                (self.Z, impedance)
            ]))
            self.Gamma_val = complex(self.Gamma_z.subs([
                (self.Z0, line_impedance),
                (self.Z, impedance)
            ]))
            self.Z_val = impedance
            if self.Y_val is not admittance and admittance is not None:
                raise Exception("Sorry, impedance value and admittance value are not related to each other")
            if self.Gamma_val is not gamma and gamma is not None:
                raise Exception("Sorry, impedance value and reflection coefficient value are not related to each other")
        elif admittance is not None:
            self.Z_val = complex(self.Z_y.subs([
                (self.Y, admittance)
            ]))
            self.Gamma_val = complex(self.Gamma_y.subs([
                (self.Z0, line_impedance),
                (self.Y, admittance)
            ]))
            self.Y_val = admittance
            if self.Z_val is not impedance and impedance is not None:
                raise Exception("Sorry, admittance value and impedance value are not related to each other")
            if self.Gamma_val is not gamma and gamma is not None:
                raise Exception("Sorry, admittance value and reflection coefficient value are not related to each other")
        elif gamma is not None:
            self.Z_val = complex(self.Z_g.subs([
                (self.Z0, line_impedance),
                (self.Gamma, gamma)
            ]))
            self.Y_val = complex(self.Y_g.subs([
                (self.Z0, line_impedance),
                (self.Gamma, gamma)
            ]))
            self.Gamma_val = gamma
            if self.Z_val is not impedance and impedance is not None:
                raise Exception("Sorry, reflection coefficient value and impedance value are not related to each other")
            if self.Y_val is not admittance and admittance is not None:
                raise Exception("Sorry, reflection coefficient value and admittance value are not related to each other")
            
    def get_impedance(self, Nomalize = False, round_index = 2): 
        if Nomalize:
            result = self.Z_val/self.Z0_val
        else:
            result = self.Z_val
        if round_index is None:
            return result
        else:
            return np.round(result, round_index)
        
    def get_admittance(self, Nomalize = False, round_index = 2): 
        if Nomalize:
            result = self.Y_val*self.Z0_val
        else:
            result = self.Y_val
        if round_index is None:
            return result
        else:
            return np.round(result, round_index)
        
    def get_gamma(self, round_index = 2):
        if round_index is None:
            result = self.Gamma_val
        else:
            try:
                result = np.round(self.Gamma_val, round_index)
            except TypeError:
                result = self.Gamma_val
        return result

    
    def get_gamma_module(self, round_index = 2):
        result = abs(self.Gamma_val)
        if round_index is None:
            return result
        else:
            return round(result, round_index)
        
    def get_gamma_polar(self, round_index = 2, unit = 'dergee'):
        if self.Gamma_val == 0:
            result = '0'
        else:
            module = abs(self.Gamma_val)
            if unit == 'dergee':
                theta = phase(self.Gamma_val)*180/np.pi
            elif unit == 'radian':
                theta = phase(self.Gamma_val)
            if round_index is not None:
                module = round(module, round_index)
                theta = round(theta, round_index)
            result = '{module}\N{angle}{theta}\N{DEGREE SIGN}'.format(module = module,
                                                                    theta = theta)
        return result
    
    def get_impedance_symbol(self, Nomalize = False):
        if Nomalize:
            return self.z
        else:
            return self.Z
        
    def get_admittance_symbol(self, Nomalize = False):
        if Nomalize:
            return self.y
        else:
            return self.Y
        
    def get_gamma_symbol(self):
        return self.Gamma
    
    def get_module_gamma_symbol(self):
        return Symbol('|' + str(self.Gamma) + '|')
        
    
    def get_impedance_formula(self, depend_on = 'gamma'):
        if depend_on == 'gamma':
            return self.Z_g
        elif depend_on == 'admittance':
            return self.Z_y
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))

    def get_admittance_formula(self, depend_on = 'impedance'):
        if depend_on == 'gamma':
            return self.Y_g
        elif depend_on == 'impedance':
            return self.Y_z
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))
            
    def get_gamma_formula(self, depend_on = 'impedance'):
        if depend_on == 'impedance':
            return self.Gamma_z
        elif depend_on == 'admittance':
            return self.Gamma_y
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))
