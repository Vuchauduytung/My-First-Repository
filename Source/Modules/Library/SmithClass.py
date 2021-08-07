from sympy import *


class SmithPoint:
    
    
    def __init__(self, name, line_impedance = 50, impedance = None, admittance = None, gamma = None, Nomalize = False):
        
        self.name = name
        self.Z0_val= line_impedance
        
        self.Z0 = Symbol('Z0')
        self.Z = Symbol('Z' + name)
        self.Y = Symbol('Y' + name)
        self.Gamma = Symbol('\u0393' + name)
               
        self.Z_y = 1/self.Y
        self.Z_g = self.Z0*(1+self.Gamma)/(1-self.Gamma)
        self.Y_z = 1/self.Z
        self.Y_g = self.Y_z.subs(self.Z, self.Z_g)
        self.Gamma_z = (-self.Z0 + self.Z)/(self.Z0 + self.Z)
        self.Gamma_y = self.Gamma_z.subs(self.Z, self.Z_y)
        
        if Nomalize:
            try:
                impedance *= line_impedance
                admittance /= line_impedance
            except TypeError:
                pass    
        
        if impedance is not None:
            self.admittance = self.Y_z.subs([
                (self.Z, impedance)
            ])
            self.Gamma_val = self.Gamma_z.subs([
                (self.Z0, line_impedance),
                (self.Z, impedance)
            ])
            if self.admittance is not admittance and admittance is not None:
                raise Exception("Sorry, impedance value and admittance value are not related to each other")
            if self.Gamma_val is not gamma and gamma is not None:
                raise Exception("Sorry, impedance value and reflection coefficient value are not related to each other")
        elif admittance is not None:
            self.Z_val = self.Z_y.subs([
                (self.Y, admittance)
            ])
            self.Gamma_val = self.Gamma_y.subs([
                (self.Z0, line_impedance),
                (self.Y, admittance)
            ])
            if self.Z_val is not impedance and impedance is not None:
                raise Exception("Sorry, admittance value and impedance value are not related to each other")
            if self.Gamma_val is not gamma and gamma is not None:
                raise Exception("Sorry, admittance value and reflection coefficient value are not related to each other")
        elif gamma is not None:
            self.Z_val = self.Z_g.subs([
                (self.Z0, line_impedance),
                (self.Gamma, gamma)
            ])
            self.admittance = self.Y_g.subs([
                (self.Z0, line_impedance),
                (self.Gamma, gamma)
            ])
            if self.Z_val is not impedance and impedance is not None:
                raise Exception("Sorry, reflection coefficient value and impedance value are not related to each other")
            if self.admittance is not admittance and admittance is not None:
                raise Exception("Sorry, reflection coefficient value and admittance value are not related to each other")
            
    def get_impedance(self, Nomalize = False): 
        if Nomalize:
            return self.Z_val
        else:
            return self.Z_val/self.Z0_val
        
    def get_admittance(self, Nomalize = False): 
        if Nomalize:
            return self.Y_val
        else:
            return self.Y_val*self.Z0_val
        
    def get_gamma(self):
        return self.Gamma_val
    
    def get_impedance_formula(self, depend_on = 'gamma'):
        if depend_on == 'gamma':
            return self.Z_g
        elif depend_on == 'admittance':
            return self.Z_y
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))

    def get_admittance_formula(self, depend_on = 'gamma'):
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