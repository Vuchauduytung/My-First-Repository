from sympy import *
import numpy as np
from cmath import *


class SmithPoint:
    # Class này chứa tất cả dữ liệu của một điểm trên mạch siêu cao tần
    # Khởi tạo bằng cách đưa vào name và một giá trị bất kỳ, có thể là trở kháng
    # hoặc dẫn kháng (admittance) chuẩn hóa hoặc tuyệt đối, hoặc giá trị của hệ số phản xạ
    # class này cung cấp tất cả thông tin về các thông số liên quan tới điểm đó bao gồm
    # ký hiệu, công thức và giá trị của các thông số liên quan tới điểm đó như, trở kháng,
    # dẫn kháng, hệ số phản xạ, góc pha, module của hệ số phản xạ
    
    
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
        # Lấy giá trị trở kháng tại điểm đang xét
        # Nomalize: giá trị trả về có chuẩn hóa hay k (True: có, False: không)
        # round_index: chỉ số của số làm tròn đến sau dấu . thập phân
        # ret: giá trị của trở kháng 
        
        if Nomalize:
            result = self.Z_val/self.Z0_val
        else:
            result = self.Z_val
        if round_index is None:
            return result
        else:
            return np.round(result, round_index)
        
    def get_admittance(self, Nomalize = False, round_index = 2): 
        # Lấy giá trị dẫn kháng tại điểm đang xét
        # Nomalize: giá trị trả về có chuẩn hóa hay k (True: có, False: không)
        # round_index: chỉ số của số làm tròn đến sau dấu . thập phân
        # ret: giá trị của dẫn kháng 
        
        if Nomalize:
            result = self.Y_val*self.Z0_val
        else:
            result = self.Y_val
        if round_index is None:
            return result
        else:
            return np.round(result, round_index)
        
    def get_gamma(self, round_index = 2):
        # Lấy giá trị hệ số phản xạ tại điểm đang xét
        # round_index: chỉ số của số làm tròn đến sau dấu . thập phân
        # ret: giá trị của hệ số phản xạ 
        
        if round_index is None:
            result = self.Gamma_val
        else:
            try:
                result = np.round(self.Gamma_val, round_index)
            except TypeError:
                result = self.Gamma_val
        return result

    
    def get_gamma_module(self, round_index = 2):
        # Lấy giá trị magnitude hệ số phản xạ tại điểm đang xét
        # round_index: chỉ số của số làm tròn đến sau dấu . thập phân
        # ret: giá trị magnitude của hệ số phản xạ 
        
        result = abs(self.Gamma_val)
        if round_index is None:
            return result
        else:
            return round(result, round_index)
        
    def get_gamma_phase(self, round_index = 2, unit = 'radian'):
        # Lấy giá trị phase hệ số phản xạ tại điểm đang xét
        # round_index: chỉ số của số làm tròn đến sau dấu . thập phân
        # ret: giá trị phase của hệ số phản xạ 
        
        if unit == 'radian':
            result = phase(self.Gamma_val)
        elif unit == 'dergee':
            result = phase(self.Gamma_val) * 180/np.pi
        else:
            raise Exception("Unknown parameter: '{}'".format(unit))
        if round_index is None:
            return result
        else:
            return round(result, round_index)
        
    def get_gamma_polar(self, round_index = 2, unit = 'dergee'):
        # Lấy giá trị string hệ số phản xạ tại điểm đang xét
        # round_index: chỉ số của số làm tròn đến sau dấu . thập phân
        # ret: string giá trị của hệ số phản xạ dưới dạng cực (polar)
        
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
        # Lấy ký hiệu của trở kháng tại điểm đang xét
        # Nomalize: ký hiệu trả về có chuẩn hóa hay k (True: có, False: không)
        # ret: ký hiệu của trở kháng
        
        if Nomalize:
            return self.z
        else:
            return self.Z
        
    def get_admittance_symbol(self, Nomalize = False):
        # Lấy ký hiệu của dẫn kháng tại điểm đang xét
        # Nomalize: ký hiệu trả về có chuẩn hóa hay k (True: có, False: không)
        # ret: ký hiệu của dẫn kháng
        
        if Nomalize:
            return self.y
        else:
            return self.Y
        
    def get_gamma_symbol(self):
        # Lấy ký hiệu của hệ số phản xạ tại điểm đang xét
        # ret: ký hiệu của hệ số phản xạ
        
        return self.Gamma
    
    def get_module_gamma_symbol(self):
        # Lấy ký hiệu của magnitude hệ số phản xạ tại điểm đang xét
        # ret: ký hiệu của magnitude hệ số phản xạ
        
        return Symbol('|' + str(self.Gamma) + '|')
    
    def get_impedance_formula(self, depend_on = 'gamma'):
        # Lấy công thức của trở kháng 
        # depend_on: công thức của trở kháng tính theo
        #   'gamma': tính theo hệ số phản xạ
        #   'admittance': tính theo dẫn kháng
        
        if depend_on == 'gamma':
            return self.Z_g
        elif depend_on == 'admittance':
            return self.Z_y
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))

    def get_admittance_formula(self, depend_on = 'impedance'):
        # Lấy công thức của dẫn kháng 
        # depend_on: công thức của dẫn kháng tính theo
        #   'gamma': tính theo hệ số phản xạ
        #   'impedance': tính theo trở kháng
        
        if depend_on == 'gamma':
            return self.Y_g
        elif depend_on == 'impedance':
            return self.Y_z
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))
            
    def get_gamma_formula(self, depend_on = 'impedance'):
        # Lấy công thức của hệ số phản xạ
        # depend_on: công thức của hệ số phản xạ tính theo
        #   'admittance': tính theo dẫn kháng
        #   'impedance': tính theo trở kháng
        
        if depend_on == 'impedance':
            return self.Gamma_z
        elif depend_on == 'admittance':
            return self.Gamma_y
        else:
            raise Exception("Unknown parameter: '{}'".format(depend_on))
    
    def get_isometric_gamma_vector(self, num = 360, angle_unit = 'radian'):
        """
        @ Brief:    Create 2 vectors that contain the magnitude and argument values (complex number)
                    with argument ranging from -pi to pi and magnitude is the repeating vector of the given value
                    2 Vectors creat a circle with radius r, phase phi (polar form)
        @ Param:    gamma_module: Thhe magnitude of the reflectance
        @ Retval:   
                    module_vector: Radius
                    theta_vector: Phase angle
        """
        
        gamma_module = self.get_gamma_module(round_index = None)
        module_vector = np.repeat(gamma_module, num)
        theta_vector = np.linspace(- np.pi, np.pi, num = num)
        if angle_unit == 'radian':
            result = (theta_vector, module_vector)
        elif angle_unit == 'degree':
            result = (theta_vector * 180/np.pi, module_vector)
        else:
            raise Exception("Unknown parameter '{}'".format(angle_unit))
        return result
    
    def get_isometric_impedance_realvalue_vector(self, num = 360, angle_unit = 'radian'):
        """
        @ Brief:    Create 2 vectors contain the magnitude and argument values of the reflectance given 
                    the condition that Z=a+bj is the impedance at the considering point and a is a given value
                    and b is within a specified range
        @ Param:    impedance_rv: Real part value of Z
        @ Retval:   
                    module_vector: Radius
                    theta_vector: Phase angle
        @ Description:  This function has a built-in ability to predict the trend of the phase angle for drawing Smith chhart
        """
        
        impedance_rv = self.get_impedance(Nomalize = True, 
                                          round_index = None)          
        a = np.repeat(impedance_rv, num)
        b = np.linspace(-10, 10, num = num)
        c = (a**2 + b**2 - 1)/((a+1)**2 + b**2)
        d = ((2*b)/((a+1)**2 + b**2)) 
        module_vector = np.sqrt(c**2 + d**2)
        theta_vector = np.arctan(d/c)
        for index in range(len(theta_vector)-1):
            while theta_vector[index] > np.pi:
                theta_vector[index : ] -= 2*np.pi
            while theta_vector[index] < -np.pi:
                theta_vector[index : ] += 2*np.pi
            while abs(theta_vector[index]-theta_vector[index+1]) >= np.pi/2:
                if theta_vector[index+1] > theta_vector[index]:
                    theta_vector[index+1 : ] -= np.pi
                else:
                    theta_vector[index+1 : ] += np.pi
            if theta_vector[index+1] < -np.pi/2:
                if index > 180:
                    theta_vector[index+1 : ] += np.pi
                    
        if angle_unit == 'radian':
            result = (theta_vector, module_vector)
        elif angle_unit == 'degree':
            result = (theta_vector * 180/np.pi, module_vector)
        else:
            raise Exception("Unknown parameter '{}'".format(angle_unit))
        return result

class SmithLine:
    # Class này chứa tất cả thông tin của đoạn dây cần xét
    # Khởi tạo bằng cách truyền tham số name (tên của đoạn dây),
    # tham số point_1 (điểm đầu mút thứ nhất), point_2 (điểm đầu mút
    # thứ 2)
    # Lưu ý: point_1 và point_2 bắt buộc phải là object của SmithPoint class
    # Class này có thể trả về giá trị chiều dài của đoạn dây đang xét
    
    def __init__(self, name, lamda, point_1 = None, point_2 = None):
        if isinstance(point_1, SmithPoint):
            self.point_1 = point_1
        else:
            raise Exception("'point_1' parameter must be SmithPoint class's object")
        if isinstance(point_2, SmithPoint):
            self.point_2 = point_2
        else:
            raise Exception("'point_1' parameter must be SmithPoint class's object")
        self.line = Symbol(name)
        self.lamda = Symbol(lamda)
    
    def get_scaled_length(self, direct = 0):
        # Lấy giá trị tuyệt đối của đoạn dây tính theo bước sóng
        # direct: xác định hướng tăng hoặc giảm chiều dài
        #   direct == 0: dịch chuyển theo hướng giảm chiều dài
        #   direct == 1: dịch chuyển theo hướng tăng chiều dài
        # ret: giá trị tuyệt đối của đoạn dây tính theo bước sóng
        
        phase_point_1 = self.point_1.get_gamma_phase(round_index = None)
        phase_point_2 = self.point_2.get_gamma_phase(round_index = None)
        if direct == 0:
            scaled_length = self.get_wire_length(phase_point_2, phase_point_1)
        elif direct == 1:
            scaled_length = self.get_wire_length(phase_point_1, phase_point_2)
        else:
            raise Exception("Invalid parameter for src_point. Value must be 1 or 2.")
        return scaled_length
            
    def get_wire_length(self, src_phase, des_phase):
        """
        @ Brief:    Calculate the wire length needs to be added toward the source to get phase shift form 
                    src_phase to des_phase (phase of the reflectance)
        @ Param:    
                    src_phase: Initial phase
                    des-phase: Destination phase
        @ Retval:   The additional wire length needed
        """
        
        while src_phase > 2*np.pi:
            src_phase -= 2*np.pi
        while src_phase < 0:
            src_phase += 2*np.pi
        while des_phase > 2*np.pi:
            des_phase -= 2*np.pi
        while des_phase < 0:
            des_phase += 2*np.pi
        if src_phase < des_phase:
            pass
        elif src_phase > des_phase:
            des_phase += 2*np.pi
        else:
            print("Source's phase equals destination's phase")
        length = (des_phase - src_phase) * 0.5/(2*np.pi)
        return length
    
    def get_absolute_length(self, direct = 0, round_index = 2):
        # Lấy giá trị tuyệt đối của đoạn dây tính theo bước sóng
        # direct: xác định hướng tăng hoặc giảm chiều dài
        #   direct == 0: dịch chuyển theo hướng giảm chiều dài
        #   direct == 1: dịch chuyển theo hướng tăng chiều dài
        # ret: giá trị tuyệt đối của đoạn dây tính theo bước sóng
        
        scaled_length = self.get_scaled_length(direct = direct)
        if round_index is None:
            absolute_length = scaled_length * self.lamda
        else:
            absolute_length = round(scaled_length, round_index) * self.lamda
        return absolute_length
    
    def get_line_symbol(self):
        # Lấy ký hiệu của đoạn dây
        # ret: ký hiệu của đoạn dây
        return self.line