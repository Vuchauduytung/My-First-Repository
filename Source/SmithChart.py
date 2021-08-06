import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.core.numbers import I
import sympy.solvers as solv
import matplotlib.pyplot as plt
from scipy.special import factorial
    
def get_gm_isometric_equation(gamma_module):
    # Tìm phương trình quỹ tích của đường đẳng độ lớn của hệ số phản xạ theo giá trị của
    # trở kháng tại vị trí đó
    # gamma_module: giá trị độ lớn của hệ số phản xạ
    # ret: gamma_module_locus_function: phương trình quỹ tích cần tìm
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
    # Tính giá trị của phần ảo của trở kháng tại điểm có phần thực và phương trình quan hệ
    # giữa phần thực và phần ảo, và giá trị của phần thực của trở kháng cho trước
    # funtion: phương trình quan hệ giữa phần thực và phần ảo
    # real_path: giá trị của phần thực cho trước
    # ret: img_path: giá trị của phần ảo tìm được
    a, b = symbols('a b', real=True)
    try:
        img_path = solv.solve(funtion.subs(a, real_path), b)
    except Exception as err:
        print("An error occurred while finding the intersection between constant gamma's module and constants real impedance locus")
        print(err)
        img_path = None
    return img_path

def get_Smith_constant_gamma_module_locus(gamma_module):
    # Tạo ra 2 vector các chứa giá trị của độ lớn và góc pha (số phức)
    # với góc pha chạy từ -pi tới pi và độ lớn là vector lặp lại của giá trị cho trước
    # 2 vector tạo nên một đường tròn bán kính r, góc pha phi (hệ tọa độ phức)
    # Ret: r: bán kính 
    #      phi: góc pha
    r = np.repeat(gamma_module, 360)
    phi = np.linspace(- np.pi, np.pi, num = 360)
    return r, phi

def get_Smith_constant_realpath_locus(real_value):
    # Tạo ra 2 vector các chứa giá trị của độ lớn và góc pha (số phức) của hệ số phản xạ
    # với điều kiện cho trước Z=a+bj là trở kháng tại điểm đang xét và a là một giá trị cho trước
    # và b nằm trong 1 khoảng quy định sẵn
    # Hàm này có tích hợp khả năng dự đoán xu hướng của góc pha dùng cho việc 
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
