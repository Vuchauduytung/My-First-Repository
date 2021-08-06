from sympy import *


class SmithPoint:
    
    
    def __init__(self, name, line_impedance_val = 50, impedance_val = None, admittance_val = None, gamma_val = None):
        
        self.name = name
        self.line_impedance_val= line_impedance_val
        # self.impedance_val = impedance_val
        # self.gamma_val = gamma_val
        # self.admittance_val = admittance_val
        
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
        
        if impedance_val is not None:
            self.admittance_val = self.Y_z.subs([
                (self.Z, impedance_val)
            ])
            self.gamma_val = self.Gamma_z.subs([
                (self.Z0, line_impedance_val),
                (self.Z, impedance_val)
            ])
            if self.admittance_val is not admittance_val and admittance_val is not None:
                raise Exception("Sorry, impedance value and admittance value are not related to each other")
            if self.gamma_val is not gamma_val and gamma_val is not None:
                raise Exception("Sorry, impedance value and reflection coefficient value are not related to each other")
        elif admittance_val is not None:
            self.impedance_val = self.Z_y.subs([
                (self.Y, admittance_val)
            ])
            self.gamma_val = self.Gamma_y.subs([
                (self.Z0, line_impedance_val),
                (self.Y, admittance_val)
            ])
            if self.impedance_val is not impedance_val and impedance_val is not None:
                raise Exception("Sorry, admittance value and impedance value are not related to each other")
            if self.gamma_val is not gamma_val and gamma_val is not None:
                raise Exception("Sorry, admittance value and reflection coefficient value are not related to each other")
        elif gamma_val is not None:
            self.impedance_val = self.Z_g.subs([
                (self.Z0, line_impedance_val),
                (self.Gamma, gamma_val)
            ])
            self.admittance_val = self.Y_g.subs([
                (self.Z0, line_impedance_val),
                (self.Gamma, gamma_val)
            ])
            if self.impedance_val is not impedance_val and impedance_val is not None:
                raise Exception("Sorry, reflection coefficient value and impedance value are not related to each other")
            if self.admittance_val is not admittance_val and admittance_val is not None:
                raise Exception("Sorry, reflection coefficient value and admittance value are not related to each other")
            