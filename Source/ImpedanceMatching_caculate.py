# System framework
import numpy as np
from sympy import *
import skrf as rf
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from cmath import *

# User framework
from Modules.Library.SmithClass import SmithPoint as SP
from Modules.Library.SmithClass import SmithLine as SL
from Modules.Library.SmithChart import *

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
    Gamma_in_value = complex(input('\t{} = '.format('\u0393in')))
    Gamma_out_value = complex(input('\t{} = '.format('\u0393out')))
    Zs_value = complex(input('\t{} = '.format('Zs')))
    ZL_value = complex(input('\t{} = '.format('ZL')))
    Z0_value = complex(input('\t{} = '.format('Z0')))
    print('\n')
    point_A = SP(name = 's', impedance = Zs_value, line_impedance = Z0_value)
    point_B = SP(name = 'L', impedance = ZL_value, line_impedance = Z0_value)
    point_C = SP(name = 'in', gamma = Gamma_in_value, line_impedance = Z0_value)
    point_D = SP(name = 'out', gamma = Gamma_out_value, line_impedance = Z0_value)
    
    # At the begin of the line
    myfunction(point_A, point_C, Z0_value, 'input')
    # At the end of the wire
    myfunction(point_B, point_D, Z0_value, 'output')
    
    input("Press Enter to stop this script >>")
    
def caculate_Gamma_short_circuit_stub(src_point, des_point, intersection, gate): 
    """
        @ Brief:    Calculate the reflectance value at the equivalent_point and the point looking at the stub circuit
        @ Param:    
                    Y_inter_value: Conductive resistance at the equivalent_point
                    Y_init_value: Conductive resistance at the initial point
                    Gamma_eq_value: reflectance at the point looking at the circuit
                    gate: The gate of the scattering matrix
        @ Retval    
                    Gamma_inter_value: reflectance at the equivalent_point
                    Gamma_stub_in_value: reflectance looking at the circuit
    """
    
    lamda = symbols('\u03BB')   
    if gate == 'input':
        # Y_inter, Y_stub_in, Y_init = symbols('Y{} Y{} Y{}'.format('a_', 'stub_', 's_'))
        # Z_inter, Z_stub_in = symbols('Z{}, Z{}'.format('a_', 'stub_'))
        # Gamma_inter, Gamma_stub_in = symbols('\u0393{} \u0393{}'.format('a', 'stub'))
        # l, d = symbols('l{} d{}'.format(get_sub('1'), get_sub('1')))
        l_name = 'l1'
        d_name = 'd1'
    elif gate == 'output':
        # Y_inter, Y_stub_in, Y_init = symbols('Y{} Y{} Y{}'.format('b_', 'stub_', 'L_'))
        # Z_inter, Z_stub_in = symbols('Z{}, Z{}'.format('b_', 'stub_'))
        # Gamma_inter, Gamma_stub_in = symbols('\u0393{} \u0393{}'.format('b', 'stub'))
        # l, d = symbols('l{} d{}'.format(get_sub('2'), get_sub('2')))
        l_name = 'l2'
        d_name = 'd2'
    
    Y_inter_nv = intersection.get_admittance(Nomalize = True)    
    Y_src_point_nv = src_point.get_admittance(Nomalize = True)  
    Y_stub_in_nv = Y_inter_nv - Y_src_point_nv
    stub_in_point = SP(name = '_stub',
                       admittance = Y_stub_in_nv,
                       Nomalize = True)
    
    print('With {normalized_admittance_intersection} = {normalized_admittance_intersection_value}, we have: \n'\
        .format(normalized_admittance_intersection = intersection.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_intersection_value = intersection.get_admittance(Nomalize = True)))
    print('\t{normalized_admittance_stub_in_point} = {normalized_admittance_intersection} - {normalized_admittance_src_point} = {normalized_admittance_stub_in_point_value}'\
        .format(normalized_admittance_stub_in_point = stub_in_point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_intersection = intersection.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_src_point = src_point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_stub_in_point_value = stub_in_point.get_admittance(Nomalize = True)))     
    print('\n')
    
    # Z_stub_in_value = 1/Y_stub_in_nv
    # print('\t{} = 1/{} = {:.2f}'.format(Z_stub_in, Y_stub_in, Z_stub_in_value))
    
    # Gamma_stub_in_ = Gamma_.subs([(Z0, 1), (Z, Z_stub_in)])
    # Gamma_stub_in_value = complex(Gamma_stub_in_.subs(Z_stub_in, Z_stub_in_value)) 
    # print('\t{} = {} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_stub_in, Gamma_stub_in_, abs(Gamma_stub_in_value), phase(Gamma_stub_in_value)*180/np.pi))
    
    print('{admittance_stub_in_point} = {admittance_stub_in_point_value}'\
        .format(admittance_stub_in_point = stub_in_point.get_admittance_symbol(),
                admittance_stub_in_point_value = stub_in_point.get_admittance()))
    print('\n')
    
    print('{gamma_stub_in_point} = {gamma_stub_in_point_formula} = {gamma_stub_in_point_value}'\
        .format(gamma_stub_in_point = stub_in_point.get_gamma_symbol(),
                gamma_stub_in_point_formula = stub_in_point.get_gamma_formula(depend_on = 'admittance'),
                gamma_stub_in_point_value = stub_in_point.get_gamma_polar()))
    print('\n')
    
    shortcircuit_point = SP(name = '_short_circuit',
                            impedance = 0)
    
    print('\tDue to short circuit at the end of the stub, we have:')
    print('\t\{gamma_shortcircuit_point} = {gamma_shortcircuit_point_polar}'\
        .format(gamma_shortcircuit_point = shortcircuit_point.get_gamma_symbol(),
                gamma_shortcircuit_point_polar = shortcircuit_point.get_gamma_polar()))
    print('\n')
    
    l = SP(name = l_name,
           lamda = lamda,
           point_1 = shortcircuit_point,
           point_2 = stub_in_point)
    # l_length = get_wire_length(phase(Gamma_stub_in_value), np.pi)   
    # l_length = get_wire_length(stub_in_point.get_gamma_phase(round_index = None), 
    #                            shortcircuit_point.get_gamma_phase(round_index = None)) 
    l_length = l.get_absolute_length()
    # l_ = lamda * l_length
    # print('\t{l_symbol} = {:.2f}*{}'.format(l, l_/lamda, lamda))
    # print('\n')
    print('{l} = {l_length}'\
        .format(l = l.get_line_symbol(),
                l_length = l_length))
    
    # Z_inter_value = 1/Y_inter_value
    # print('\t{} = 1/{} = {:.2f}'.format(Z_inter, Y_inter, Z_inter_value))
    # print('\n')
    
    print('{admittance_intersection} = {admittance_intersection_value}'\
        .format(admittance_intersection = intersection.get_admittance_symbol(),
                admittance_intersection_value = intersection.get_admittance()))
    print('\n')
    
    # Gamma_inter_ = Gamma_.subs([(Z0, 1), (Z, Z_inter)])
    # Gamma_inter_value = complex(Gamma_inter_.subs(Z_inter, Z_inter_value)) 
    # print('\t{} = {} = {:.2f}\N{angle}{:.2f}\N{DEGREE SIGN}'.format(Gamma_inter, Gamma_inter_, abs(Gamma_inter_value), phase(Gamma_inter_value)*180/np.pi))
    # print('\n')
    
    print('{gamma_intersection} = {gamma_intersection_formula} = {gamma_intersection_polar}'\
        .format(gamma_intersection = intersection.get_gamma_symbol(),
                gamma_intersection_formula = intersection.get_gamma_formula(depend_on = 'admittance'),
                gamma_intersection_polar = intersection.get_gamma_polar()))
    print('\n')
    
    d = SP(name = d_name,
           lamda = lamda,
           point_1 = intersection,
           point_2 = des_point)
    
    # d_length = get_wire_length(phase(Gamma_eq_value), phase(Gamma_inter_value))
    # d_ = lamda * d_length
    # print('\t{} = {:.2f}*{}'.format(d, d_/lamda, lamda))
    # print('\n')
    d_length = d.get_absolute_length()
    print('{d} = {d_length}'\
        .format(d = d.get_line_symbol(),
                d_length = d_length))

    return stub_in_point
    
def plot_smith_chart(src_point, des_point, intersection, gate):
    """
        @ BriefL:   Draw the Smith graph from known parameters
        @ Param:    
                    Y_init_value: Conductive resistance at the initial point
                    Y_inter_value: Conductive resistance at the equivalent_point
                    Gamma_final_value: reflectance at the destination point
                    Gamma_init_value: reflectance at the initial point
                    gate: The gate of the scattering matrix
    """
    
    if gate == 'input':
        Y_inter, Y_stub_in, Y_init, Y_result = symbols('Y{} Y{} Y{} Y{}'.format('a', get_sub('stub'), get_sub('s'), get_sub('s_max')))
        Z_inter, Z_stub_in, Z_init, Z_result = symbols('Z{}, Z{} Z{} Z{}'.format('a', get_sub('stub'), get_sub('s'), get_sub('s_max')))
    elif gate == 'output':
        Y_inter, Y_stub_in, Y_init, Y_result = symbols('Y{} Y{} Y{} Y{}'.format('b', get_sub('stub'), get_sub('L'), get_sub('L_max')))
        Z_inter, Z_stub_in, Z_init, Z_result = symbols('Z{}, Z{} Z{} Z{}'.format('b', get_sub('stub'), get_sub('L'), get_sub('L_max')))
    fig, axes = plt.subplots(2, len(intersection), subplot_kw={'projection': 'polar'})
    
    for point in intersection:
        normalized_admittance_intersection = point.get_admittance(Nomalize = True)
        try:
            Y_inter_value = np.append(Y_inter_value, normalized_admittance_intersection)
        except NameError:
            Y_inter_value = np.array([normalized_admittance_intersection])
            
    for index, point in enumerate(intersection):
        try:
            ax1 = axes[0][index]
            ax2 = axes[1][index]
        except TypeError:
            ax1 = axes[0]
            ax2 = axes[1]
        stub_in_point = caculate_Gamma_short_circuit_stub(point, src_point, des_point, gate)
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
    """
        @ Brief: Transform the characters from normal normal format to subscript format
        @ Parma: x: Normal characters
        @ Retval: Characters in subscript format  
    """
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)    

def myfunction(start_point, gate_point, line_impedance, gate):
    """
        @brief      Caculate and display result for impedance matching problem
        @param      Zw_value          wire impedance
        @param      ZL_value          load impedance
        @param      Gamma_eq_value    equivalent reflectance looking at starting point of the line
        Explain:
            Gamma_L     reflectance looking at the end of the line
            Gamma_eq    reflectance looking at starting point of the line
            Gamma_g     reflectance at gate of scattering matrix module
            Zeq         equivalent impedance looking at starting point of the line
            Zeq_norm    equivalent impedance looking at starting point of the line normalized to Z0
            ZL          load impedance
            ZL_norm     load impedance normalized to Z0
            YL_norm     load admittance normalized to Z0
            Yit_norm    constant real value and reflectance' module equivalent_point 
            admittance normalized to Z0
    """
    
    if gate == 'input':
        equivalent_point_name = 's_max'
        intersection_name = 'a'
    elif gate == 'output':
        equivalent_point_name = 'L_max'
        intersection_name = 'b'

    print('{gamma_start_point} = {gamma_start_point_value}'\
        .format(gamma_start_point = start_point.get_gamma_symbol(),
                gamma_start_point_value = start_point.get_gamma_polar()))                                       
    print('\n')
    
    print('For maximum power gain:')
    Gamma_eq_value = gate_point.get_gamma().conjugate()
    equivalent_point = SP(name = equivalent_point_name, 
                      gamma = Gamma_eq_value, 
                      line_impedance = line_impedance)

    print('{gamma_equivalent_point} = {gamma_gate_point}* = {gamma_equivalent_point_value}'\
        .format(gamma_equivalent_point = equivalent_point.get_gamma_symbol(),
                gamma_gate_point = gate_point.get_gamma_symbol(),
                gamma_equivalent_point_value = equivalent_point.get_gamma_polar()))                                                                                          
    print('\n')

    print('{impedance_equivalent_point} = {impedance_equivalent_point_formula} = {impedance_equivalent_point_value}'\
        .format(impedance_equivalent_point = equivalent_point.get_impedance_symbol(), 
                impedance_equivalent_point_formula = equivalent_point.get_impedance_formula(),
                impedance_equivalent_point_value = equivalent_point.get_impedance()))                                                                             
    print('\n')

    print('{normalized_impedance_equivalent_point} = {normalized_impedance_equivalent_point_value}'\
        .format(normalized_impedance_equivalent_point = equivalent_point.get_impedance_symbol(Nomalize = True),
                normalized_impedance_equivalent_point_value = equivalent_point.get_impedance(Nomalize = True)))
    print('\n')
    
    print('{normalized_admittance_start_point} = {normalized_admittance_start_point_value}'\
        .format(normalized_admittance_start_point = start_point.get_impedance_symbol(Nomalize = True),
                normalized_admittance_start_point_value = start_point.get_admittance(Nomalize = True)))

    print('{normalized_admittance_start_point} = {normalized_admittance_start_point_value}'\
        .format(normalized_admittance_start_point = start_point.get_admittance_symbol(Nomalize = True),
                normalized_admittance_start_point_value = start_point.get_admittance(Nomalize = True)))
    print('\n')

    Gamma_eq_mv = equivalent_point.get_gamma_module()     

    print('{module_gamma_equivalent_point} = {module_gamma_equivalent_point_value}'\
        .format(module_gamma_equivalent_point = equivalent_point.get_module_gamma_symbol(),
                module_gamma_equivalent_point_value = equivalent_point.get_gamma_module()))
    print('\n')

    gm_isometric_equation = get_gm_isometric_equation(Gamma_eq_mv)
    # Real value of load admittance normalized to Z0
    YL_norm_rv = start_point.get_admittance(Nomalize = True).real
    # Image value of load admittance normalized to Z0
    Yit_norm_iv = find_cmg_cri_intersection(gm_isometric_equation, YL_norm_rv)
    
    print('Look up Smith chart, we have:')
    print('\n')
    
    for imag_value in Yit_norm_iv:
        value = complex(YL_norm_rv, imag_value)
        intersection_i = SP(name = intersection_name,
                                 line_impedance = line_impedance,
                                 admittance = value,
                                 Nomalize = True)
        try:
            intersection = np.append(intersection, intersection_i)
            print('\tor {normalized_admittance_intersection} = {normalized_admittance_intersection_value}'\
                .format(normalized_admittance_intersection = intersection_i.get_admittance_symbol(Nomalize = True),
                        normalized_admittance_intersection_value = intersection_i.get_admittance(Nomalize = True)))
        except NameError:
            intersection = np.array([intersection_i])
            print('\t{normalized_admittance_intersection} = {normalized_admittance_intersection_value}'\
                .format(normalized_admittance_intersection = intersection_i.get_admittance_symbol(Nomalize = True),
                        normalized_admittance_intersection_value = intersection_i.get_admittance(Nomalize = True)))
    print('\n')
    
    for point in intersection:
        stub_in_point_i = caculate_Gamma_short_circuit_stub(start_point, equivalent_point, point, gate)
    # plot_smith_chart(Yit_norm_value, YL_norm_value, Gamma_eq_value, Gamma_L_value, gate)
    # plot_smith_chart(start_point, equivalent_point, intersection, gate)
    stub_in_point = caculate_Gamma_short_circuit_stub(start_point, equivalent_point, intersection, gate)
    plot_smith_chart(start_point, equivalent_point, intersection, gate)

# def get_wire_length(src_phase, des_phase):
#     """
#         @ Brief:    Calculate the wire length needs to be added toward the source to get phase shift form 
#                     src_phase to des_phase (phase of the reflectance)
#         @ Param:    
#                     src_phase: Initial phase
#                     des-phase: Destination phase
#         @ Retval:   The additional wire length needed
#     """
#     while src_phase > 2*np.pi:
#         src_phase -= 2*np.pi
#     while src_phase < 0:
#         src_phase += 2*np.pi
#     while des_phase > 2*np.pi:
#         des_phase -= 2*np.pi
#     while des_phase < 0:
#         des_phase += 2*np.pi
#     if src_phase < des_phase:
#         pass
#     elif src_phase > des_phase:
#         des_phase += 2*np.pi
#     else:
#         print("Source's phase equals destination's phase")
#     length = (des_phase - src_phase) * 0.5/(2*np.pi)
#     return length

if __name__ == '__main__': 
    main()
