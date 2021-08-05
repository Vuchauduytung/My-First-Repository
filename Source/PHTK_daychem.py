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
Zs_std, ZL_std, Zs_max_std, ZL_max_std = symbols('Zs_ ZL_ Zs_max_ ZL_max_')
Ys_std, YL_std, Ys_max_std, YL_max_std = symbols('Ys_ YL_ Ys_max_ YL_max_')
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
    
    Gamma_S_value = Gamma_.subs([(Z0, Z0_value), (Z, Zs_value)])
    print('{} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_S, abs(Gamma_S_value), phase(Gamma_S_value)))
    print('\n')
    
    print('For maximum power gain:')
    Gamma_S_max_value = Gamma_in_value.conjugate()
    print('\t{} = {}* = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_S_max, Gamma_in, abs(Gamma_S_max_value), phase(Gamma_S_max_value)*180/np.pi))
    print('\n')
    
    Zs_max_ = Z_.subs(Gamma, Gamma_S_max)
    print('{} = {}'.format(Zs_max, Zs_max_))
    print('\n')

    Zs_max_std_ = Zs_max_/Z0
    Zs_max_std_value = complex(Zs_max_std_.subs(Gamma_S_max, Gamma_S_max_value)) 
    print('{} = {}/{} = {} = {:.2f}'.format(Zs_max_std, Zs_max, Z0, Zs_max_std_, Zs_max_std_value))
    print('\n')

    Ys_max_std_value = 1/Zs_max_std_value
    print('{} = 1/{} = {:.2f}'.format(Ys_std, Zs_max_std, Ys_max_std_value))
    print('\n')

    Zs_std_value = Zs_value/Z0_value
    print('{} = {}/{} = {:.2f}'.format(Zs_std, Zs, Z0, Zs_std_value))
    print('\n')

    Ys_std_value = 1/Zs_std_value
    print('{} = 1/{} = {:.2f}'.format(Ys_std, Zs_std, Ys_std_value))
    print('\n')

    module_Gamma_S_max_value = abs(Gamma_S_max_value)
    print('{} = {:.2f}'.format(module_Gamma_S_max, module_Gamma_S_max_value))
    print('\n')

    gamma_module_S_locus_funtion = constant_module_gamma_function(module_Gamma_S_max_value)
    Ys_std_real_path = Ys_std_value.real
    Ysl1_std_imag_path = find_cmg_cri_intersection(gamma_module_S_locus_funtion, Ys_std_real_path)

    for imag_value in Ysl1_std_imag_path:
        value = complex(Ys_std_real_path, imag_value)
        try:
            Ysl1_std_value = np.append(Ysl1_std_value, value)
        except NameError:
            Ysl1_std_value = np.array([value])
            
    print('Look up Smith chart, we have:')
    print('Ya_ = ', Ysl1_std_value)
    print('\n')
    
    plot_smith_chart(Ysl1_std_value, Ys_std_value, Gamma_S_max_value, Gamma_S_value, 'input')
    
    # At the end of the wire
    myfunction(Z0_value, ZL_value, Gamma_out_value)
    
    input("Press Enter to stop this script >>")
    
def caculate_Gamma_short_circuit_stub(Y_inter_value, Y_init_value, Gamma_init_value, gate): 
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
    
    l_ = lamda * (180 - phase(Gamma_stub_in_value)*180/np.pi) * 0.5/360
    print('\t{} = {:.2f}*{}'.format(l, l_/lamda, lamda))
    print('\n')
    
    Z_inter_value = 1/Y_inter_value
    print('\t{} = 1/{} = {:.2f}'.format(Z_inter, Y_inter, Z_inter_value))
    print('\n')
    
    Gamma_inter_ = Gamma_.subs([(Z0, 1), (Z, Z_inter)])
    Gamma_inter_value = complex(Gamma_inter_.subs(Z_inter, Z_inter_value)) 
    print('\t{} = {} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_inter, Gamma_inter_, abs(Gamma_inter_value), phase(Gamma_inter_value)*180/np.pi))
    print('\n')
    
    d_ = lamda * (phase(Gamma_init_value) - phase(Gamma_inter_value)) * 0.5/(2*np.pi)
    print('\t{} = {:.2f}*{}'.format(d, d_/lamda, lamda))
    print('\n')

    return Gamma_inter_value, Gamma_stub_in_value
    
def plot_smith_chart(Y_inter_value, Y_init_value, Gamma_final_value, Gamma_init_value ,gate):
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
        Gamma_inter_val, Gamma_stub_in_val = caculate_Gamma_short_circuit_stub(Y_inter_val, Y_init_value, Gamma_init_value, gate)
        p1 = ax1.scatter(phase(Gamma_final_value), abs(Gamma_final_value), marker='o', s=100, color = 'r', alpha = 1, label = Z_result)
        p2 = ax1.scatter(phase(Gamma_final_value) + np.pi, abs(Gamma_final_value), marker='x', linewidths = 3, color = 'm', alpha = 1, label = Y_result)
        p3 = ax1.scatter(phase(Gamma_init_value), abs(Gamma_init_value), marker='o', s=100, color = 'y', alpha = 1, label = Z_init)
        p4 = ax1.scatter(phase(Gamma_init_value) + np.pi, abs(Gamma_init_value), marker='x', linewidths = 3, color = 'b', alpha = 1, label = Y_init)
        p5 = ax1.scatter(phase(Gamma_inter_val), abs(Gamma_inter_val), marker='o', s=100, color = 'orange', alpha = 1, label = Z_inter)
        p6 = ax1.scatter(phase(Gamma_inter_val) + np.pi, abs(Gamma_inter_val), marker='x', linewidths = 3, color = 'c', alpha = 1, label = Y_inter)
        r, phi = get_Smith_constant_gamma_module_locus(abs(Gamma_final_value))
        ax1.plot(phi, r, color = 'gray')
        r, phi = get_Smith_constant_gamma_module_locus(1)
        ax1.plot(phi, r, color = 'black')
        r, phi = get_Smith_constant_realpath_locus(abs(Y_init_value))
        ax1.plot(phi, r, color = 'violet')
        ax1.axes.xaxis.set_ticklabels([])
        ax1.axes.yaxis.set_ticklabels([])
        fontP = FontProperties()
        fontP.set_size('medium')
        title = 'note'
        ax1.legend(handles=[p1, p2, p3, p4, p5, p6], title = title, bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
        ax1.set_title('With {} = {:.2f}'.format(Y_inter ,Y_inter_val) + '\nOn main circuit')
        
        p7 = ax2.scatter(phase(Gamma_stub_in_val), abs(Gamma_stub_in_val), marker='o', s=100, color = 'r', alpha = 1, label = Z_stub_in)
        p8 = ax2.scatter(phase(Gamma_stub_in_val) + np.pi, abs(Gamma_stub_in_val), marker='x', linewidths = 3, color = 'm', alpha = 1, label = Y_stub_in)
        p9 = ax2.scatter(np.pi, 1, marker='o', s=100, color = 'r', alpha = 1, label = 'Z{}'.format(get_sub('short')))
        p10 = ax2.scatter(0, 1, marker='x', linewidths = 3, color = 'm', alpha = 1, label = 'Y{}'.format(get_sub('short')))
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
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)    

def myfunction(Z0_value, ZL_value, Gamma_out_value):
    Yb_std = symbols('Yb_')
    Gamma_L_value = Gamma_.subs([(Z0, Z0_value), (Z, ZL_value)])
    print('{} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_L, abs(Gamma_L_value), phase(Gamma_L_value)*180/np.pi))
    print('\n')
    print('For maximum power gain:')
    Gamma_L_max_value = Gamma_out_value.conjugate()
    print('\t{} = {}* = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_L_max, Gamma_out, abs(Gamma_L_max_value), phase(Gamma_L_max_value)*180/np.pi))
    print('\n')
    ZL_max_ = Z_.subs(Gamma, Gamma_L_max)
    print('{} = {}'.format(ZL_max, ZL_max_))
    print('\n')
    ZL_max_std_ = ZL_max_/Z0
    ZL_max_std_value = complex(ZL_max_std_.subs(Gamma_L_max, Gamma_L_max_value))
    print('{} = {}/{} = {} = {:.2f}'.format(ZL_max_std, ZL_max, Z0, ZL_max_std_, ZL_max_std_value))
    print('\n')
    YL_max_std_value = 1/ZL_max_std_value
    print('{} = 1/{} = {:.2f}'.format(YL_std, ZL_max_std, YL_max_std_value))
    print('\n')
    ZL_std_value = ZL_value/Z0_value
    print('{} = {}/{} = {:.2f}'.format(ZL_std, ZL, Z0, ZL_std_value))
    print('\n')
    YL_std_value = 1/ZL_std_value
    print('{} = 1/{} = {:.2f}'.format(YL_std, ZL_std, YL_std_value))
    print('\n')
    module_Gamma_L_max_value = abs(Gamma_L_max_value)
    print('{} = {:.2f}'.format(module_Gamma_S_max, module_Gamma_L_max_value))
    print('\n')
    gamma_module_S_locus_funtion = constant_module_gamma_function(module_Gamma_L_max_value)
    YL_std_real_path = YL_std_value.real
    Yb_std_imag_path = find_cmg_cri_intersection(gamma_module_S_locus_funtion, YL_std_real_path)

    for imag_value in Yb_std_imag_path:
        value = complex(YL_std_real_path, imag_value)
        try:
            Yb_std_value = np.append(Yb_std_value, value)
        except NameError:
            Yb_std_value = np.array([value])
            
    print('Look up Smith chart, we have:')
    print('{} = '.format(Yb_std), Yb_std_value)
    print('\n')
    
    plot_smith_chart(Yb_std_value, YL_std_value, Gamma_L_max_value, Gamma_L_value, 'output')
    

if __name__ == '__main__': 
    main()
