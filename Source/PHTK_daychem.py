import numpy as np
from sympy import *
import skrf as rf
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from SmithChart import *
from cmath import *


# parameter
Gamma_S_max, Gamma_L_max, Gamma_S, Gamma_L, Gamma_in, Gamma_out, Gamma = symbols('\u0393s_max \u0393L_max \u0393s \u0393L \u0393in \u0393out \u0393')
Zs, Z0, ZL, Zs_max, ZL_max, Z = symbols('Zs Z0 ZL Zs_max ZL_max Z')
Zs_norm, ZL_norm, Zs_max_norm, ZL_max_norm = symbols('Zs_ ZL_ Zs_max_ ZL_max_')
Ys_norm, YL_norm, Ys_max_norm, YL_max_norm = symbols('Ys_ YL_ Ys_max_ YL_max_')
module_Gamma_S_max, module_Gamma_L_max = symbols('|\u0393s_max| |\u0393L_max|')

Gamma_ = (-Z0 + Z)/(Z0 + Z)
Z_ = Z0*(1+Gamma)/(1-Gamma)
    


def main():
    print('Please type:')
    Gamma_in_value = complex(input('\t{} = '.format(Gamma_in)))
    Gamma_out_value = complex(input('\t{} = '.format(Gamma_out)))
    Zs_value = complex(input('\t{} = '.format(Zs)))
    ZL_value = complex(input('\t{} = '.format(ZL)))
    Z0_value = complex(input('\t{} = '.format(Z0)))
    print('\n')
    #
    myfunction(Z0_value, Zs_value, Gamma_in_value, 'input')
    # At the end of the wire
    myfunction(Z0_value, ZL_value, Gamma_out_value, 'output')
    
    input("Press Enter to stop this script >>")
    
def caculate_Gamma_short_circuit_stub(Y_inter_value, Y_init_value, Gamma_eq_value, gate): 
    # Tính toán giá trị của hệ số phản xạ tại giao điểm và tại điểm nhìn vào mạch stub
    # Y_inter_value: dẫn kháng tại điểm giao
    # Y_init_value: dẫn kháng tại điểm ban đầu
    # Gamma_eq_value: hệ số phản xạ tại điểm nhìn vào mạch
    # gate: cổng của ma trận tán xạ
    # ret: Gamma_inter_value: hệ số phản xạ tại điểm giao
    #       Gamma_stub_in_value: hệ số phản xạ nhìn vào đầu mạch stub
    lamda = symbols('\u03BB')   
    if gate == 'input':
        Y_inter, Y_stub_in, Y_init = symbols('Y{} Y{} Y{}'.format('a_', 'stub_', 's_'))
        Z_inter, Z_stub_in = symbols('Z{}, Z{}'.format('a_', 'stub_'))
        Gamma_inter, Gamma_stub_in = symbols('\u0393{} \u0393{}'.format('a', 'stub'))
        l, d = symbols('l{} d{}'.format(get_sub('1'), get_sub('1')))
    elif gate == 'output':
        Y_inter, Y_stub_in, Y_init = symbols('Y{} Y{} Y{}'.format('b_', 'stub_', 'L_'))
        Z_inter, Z_stub_in = symbols('Z{}, Z{}'.format('b_', 'stub_'))
        Gamma_inter, Gamma_stub_in = symbols('\u0393{} \u0393{}'.format('b', 'stub'))
        l, d = symbols('l{} d{}'.format(get_sub('2'), get_sub('2')))
    Y_stub_in_value = Y_inter_value - Y_init_value
    print('With {} = {:.2f}, we have: \n'.format(Y_inter, Y_inter_value))
    print('\t{} = {} - {} = {:.2f}'.format(Y_stub_in, Y_inter, Y_init, Y_stub_in_value))     
    print('\n')
    
    Z_stub_in_value = 1/Y_stub_in_value
    print('\t{} = 1/{} = {:.2f}'.format(Z_stub_in, Y_stub_in, Z_stub_in_value))
    
    Gamma_stub_in_ = Gamma_.subs([(Z0, 1), (Z, Z_stub_in)])
    Gamma_stub_in_value = complex(Gamma_stub_in_.subs(Z_stub_in, Z_stub_in_value)) 
    print('\t{} = {} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_stub_in, Gamma_stub_in_, abs(Gamma_stub_in_value), phase(Gamma_stub_in_value)*180/np.pi))
    print('\tDue to short circuit at the end of the stub, we have:')
    print('\t\tGamma_short_circuit = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(1,-180))
    print('\n')
        
    l_length = get_wire_length(phase(Gamma_stub_in_value), np.pi)    
    l_ = lamda * l_length
    print('\t{} = {:.2f}*{}'.format(l, l_/lamda, lamda))
    print('\n')
    
    Z_inter_value = 1/Y_inter_value
    print('\t{} = 1/{} = {:.2f}'.format(Z_inter, Y_inter, Z_inter_value))
    print('\n')
    
    Gamma_inter_ = Gamma_.subs([(Z0, 1), (Z, Z_inter)])
    Gamma_inter_value = complex(Gamma_inter_.subs(Z_inter, Z_inter_value)) 
    print('\t{} = {} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_inter, Gamma_inter_, abs(Gamma_inter_value), phase(Gamma_inter_value)*180/np.pi))
    print('\n')

    d_length = get_wire_length(phase(Gamma_eq_value), phase(Gamma_inter_value))
    d_ = lamda * d_length
    print('\t{} = {:.2f}*{}'.format(d, d_/lamda, lamda))
    print('\n')

    return Gamma_inter_value, Gamma_stub_in_value
    
def plot_smith_chart(Y_inter_value, Y_init_value, Gamma_final_value, Gamma_init_value ,gate):
    # Vẽ đồ thị Smith từ thông số cho trước
    # Y_init_value: Dẫn kháng điểm ban đầu
    # Y_inter_value: Dẫn kháng điểm giao
    # Gamma_final_value: Hệ số phản xạ điểm đích
    # Gamma_init_value: Hệ số phản xạ điểm ban đầu
    # Cổng của ma trận tán xạ
    if gate == 'input':
        Y_inter, Y_stub_in, Y_init, Y_result = symbols('Y{} Y{} Y{} Y{}'.format('a', get_sub('stub'), get_sub('s'), get_sub('s_max')))
        Z_inter, Z_stub_in, Z_init, Z_result = symbols('Z{}, Z{} Z{} Z{}'.format('a', get_sub('stub'), get_sub('s'), get_sub('s_max')))
    elif gate == 'output':
        Y_inter, Y_stub_in, Y_init, Y_result = symbols('Y{} Y{} Y{} Y{}'.format('b', get_sub('stub'), get_sub('L'), get_sub('L_max')))
        Z_inter, Z_stub_in, Z_init, Z_result = symbols('Z{}, Z{} Z{} Z{}'.format('b', get_sub('stub'), get_sub('L'), get_sub('L_max')))
    fig, axes = plt.subplots(2, len(Y_inter_value), subplot_kw={'projection': 'polar'})
    for index, Y_inter_val in enumerate(Y_inter_value):
        try:
            ax1 = axes[0][index]
            ax2 = axes[1][index]
        except TypeError:
            ax1 = axes[0]
            ax2 = axes[1]
        Gamma_inter_val, Gamma_stub_in_val = caculate_Gamma_short_circuit_stub(Y_inter_val, Y_init_value, Gamma_final_value, gate)
        p1 = ax1.scatter(phase(Gamma_final_value), abs(Gamma_final_value), marker='o', s=100, color = 'r', alpha = 1, label = Z_result)
        p2 = ax1.scatter(phase(Gamma_final_value) + np.pi, abs(Gamma_final_value), marker='x', linewidths = 3, color = 'r', alpha = 1, label = Y_result)
        p3 = ax1.scatter(phase(Gamma_init_value), abs(Gamma_init_value), marker='o', s=100, color = 'b', alpha = 1, label = Z_init)
        p4 = ax1.scatter(phase(Gamma_init_value) + np.pi, abs(Gamma_init_value), marker='x', linewidths = 3, color = 'b', alpha = 1, label = Y_init)
        p5 = ax1.scatter(phase(Gamma_inter_val), abs(Gamma_inter_val), marker='o', s=100, color = 'orange', alpha = 1, label = Z_inter)
        p6 = ax1.scatter(phase(Gamma_inter_val) + np.pi, abs(Gamma_inter_val), marker='x', linewidths = 3, color = 'orange', alpha = 1, label = Y_inter)
        r, phi = get_Smith_constant_gamma_module_locus(abs(Gamma_final_value))
        ax1.plot(phi, r, color = 'c')
        r, phi = get_Smith_constant_gamma_module_locus(1)
        ax1.plot(phi, r, color = 'black')
        r, phi = get_Smith_constant_realpath_locus(Y_init_value.real)
        ax1.plot(phi, r, color = 'violet')
        ax1.axes.xaxis.set_ticklabels([])
        ax1.axes.yaxis.set_ticklabels([])
        fontP = FontProperties()
        fontP.set_size('medium')
        title = 'note'
        ax1.legend(handles=[p1, p2, p3, p4, p5, p6], title = title, bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
        ax1.set_title('With {} = {:.2f}'.format(Y_inter ,Y_inter_val) + '\nOn main circuit')
        
        p7 = ax2.scatter(phase(Gamma_stub_in_val), abs(Gamma_stub_in_val), marker='o', s=100, color = 'b', alpha = 1, label = Z_stub_in)
        p8 = ax2.scatter(phase(Gamma_stub_in_val) + np.pi, abs(Gamma_stub_in_val), marker='x', linewidths = 3, color = 'b', alpha = 1, label = Y_stub_in)
        p9 = ax2.scatter(np.pi, 1, marker='o', s=100, color = 'r', alpha = 1, label = 'Z{}'.format(get_sub('short')))
        p10 = ax2.scatter(0, 1, marker='x', linewidths = 3, color = 'r', alpha = 1, label = 'Y{}'.format(get_sub('short')))
        r, phi = get_Smith_constant_gamma_module_locus(1)
        ax2.plot(phi, r, color = 'black')
        ax2.axes.xaxis.set_ticklabels([])
        ax2.axes.yaxis.set_ticklabels([])
        fontP = FontProperties()
        fontP.set_size('medium')
        title = 'note'
        ax2.set_title('On stub circuit')
        ax2.legend(handles=[p7, p8, p9, p10], title = title, bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP) 
    fig.suptitle('Impedance matching at {}'.format(gate), fontsize=16)
    fig.show()
    
def get_sub(x):
    # Chuyển đổi từ từ ký tự bình thường sang subscript
    # x ký tự bình thường
    # ký tự dạng subscript
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)    

def myfunction(Zw_value, ZL_value, Gamma_g_value, gate):
    """
        @brief      Caculate and display result for impedance matching problem
        @param      Zw_value          wire impedance
        @param      ZL_value          load impedance
        @param      Gamma_eq_value    equivalent reflection coefficient looking at starting point of the line
        Explain:
            Gamma_L     reflection coefficient looking at the end of the line
            Gamma_eq    reflection coefficient looking at starting point of the line
            Gamma_g     reflection coefficient at gate of scattering matrix module
            Zeq         equivalent impedance looking at starting point of the line
            Zeq_norm    equivalent impedance looking at starting point of the line normalized to Z0
            ZL          load impedance
            ZL_norm     load impedance normalized to Z0
            YL_norm     load admittance normalized to Z0
            Yit_norm    constant real value and reflection coefficient' module intersection 
            admittance normalized to Z0
    """
    
    if gate == 'input':
        Gamma_L, Gamma_eq, Gamma_g = symbols('\u0393s \u0393s_max \u0393in')  
        Zeq, Zeq_norm, ZL, ZL_norm = symbols('Zs_max Zs_max_ Zs Zs_')
        YL_norm = symbols('Ys_')
        Yit_norm = symbols('Ya_')
    elif gate == 'output':
        Gamma_L, Gamma_eq, Gamma_g = symbols('\u0393L \u0393L_max \u0393out')  
        Zeq, Zeq_norm, ZL, ZL_norm = symbols('ZL_max ZL_max_ ZL ZL_')
        YL_norm = symbols('YL_')
        Yit_norm = symbols('Yb_')
    
    Gamma_L_value = Gamma_.subs([(Z0, Zw_value), (Z, ZL_value)])
    try:
        print('{} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_L, abs(Gamma_L_value), phase(Gamma_L_value)*180/np.pi))
    except TypeError:
        print('{} = 0'.format(Gamma_L))
    print('\n')
    print('For maximum power gain:')
    Gamma_eq_value = Gamma_g_value.conjugate()
    print('\t{} = {}* = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_eq, Gamma_g , abs(Gamma_eq_value), phase(Gamma_eq_value)*180/np.pi))
    print('\n')
    Zeq_ = Z_.subs(Gamma, Gamma_eq)
    print('{} = {}'.format(Zeq, Zeq_))
    print('\n')
    Zeq_norm_ = Zeq_/Z0
    ZL_eq_value = complex(Zeq_norm_.subs(Gamma_eq, Gamma_eq_value))
    print('{} = {}/{} = {} = {:.2f}'.format(Zeq_norm, Zeq, Z0, Zeq_norm_, ZL_eq_value))
    print('\n')
    YL_eq_value = 1/ZL_eq_value
    print('{} = 1/{} = {:.2f}'.format(YL_norm, Zeq_norm, YL_eq_value))
    print('\n')
    ZL_norm_value = ZL_value/Zw_value
    print('{} = {}/{} = {:.2f}'.format(ZL_norm, ZL, Z0, ZL_norm_value))
    print('\n')
    YL_norm_value = 1/ZL_norm_value
    print('{} = 1/{} = {:.2f}'.format(YL_norm, ZL_norm, YL_norm_value))
    print('\n')
    # Module value of reflection coefficient looking at starting point of the line
    Gamma_eq_mv = abs(Gamma_eq_value)       
    print('{} = {:.2f}'.format(module_Gamma_S_max, Gamma_eq_mv))
    print('\n')
    # Locus equation of reflection coefficient's module isometric line
    gm_isometric_equation = get_gm_isometric_equation(Gamma_eq_mv)
    # Real value of load admittance normalized to Z0
    YL_norm_rv = YL_norm_value.real
    # Image value of load admittance normalized to Z0
    Yit_norm_iv = find_cmg_cri_intersection(gm_isometric_equation, YL_norm_rv)

    for imag_value in Yit_norm_iv:
        value = complex(YL_norm_rv, imag_value)
        try:
            Yit_norm_value = np.append(Yit_norm_value, value)
        except NameError:
            Yit_norm_value = np.array([value])
            
    print('Look up Smith chart, we have:')
    print('{} = '.format(Yit_norm), Yit_norm_value)
    print('\n')
    
    plot_smith_chart(Yit_norm_value, YL_norm_value, Gamma_eq_value, Gamma_L_value, gate)

def get_wire_length(src_phase, des_phase):
    # Tính chiều dài đoạn cần bù thêm (về phía nguồn) để có pha dịch từ src_phase sang des_phase (pha của hệ số phản xạ)
    # src_phase ban đầu
    # des-phase pha lúc sau
    # ret đoạn dây cần bù 
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

if __name__ == '__main__': 
    main()
