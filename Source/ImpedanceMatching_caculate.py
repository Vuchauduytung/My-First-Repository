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


def main():
    # User input
    print('\n')
    print('Please type:')
    Gamma_in_value = complex(input('\t{} = '.format('\u0393in')))
    Gamma_out_value = complex(input('\t{} = '.format('\u0393out')))
    Zs_value = complex(input('\t{} = '.format('Zs')))
    ZL_value = complex(input('\t{} = '.format('ZL')))
    Z0_value = complex(input('\t{} = '.format('Z0')))
    print('\n')
    
    # Initialize point on circuit
    point_A = SP(name = 's', 
                 impedance = Zs_value, 
                 line_impedance = Z0_value)
    point_B = SP(name = 'L', 
                 impedance = ZL_value, 
                 line_impedance = Z0_value)
    point_C = SP(name = 'in', 
                 gamma = Gamma_in_value, 
                 line_impedance = Z0_value)
    point_D = SP(name = 'out', 
                 gamma = Gamma_out_value, 
                 line_impedance = Z0_value)
    shortcircuit_point = SP(name = '_short_circuit',
                            impedance = 0,
                            line_impedance = Z0_value)
    
    print('Due to short circuit at the end of the stub, we have:')
    print('\t{gamma_shortcircuit_point} = {gamma_shortcircuit_point_polar}'\
        .format(gamma_shortcircuit_point = shortcircuit_point.get_gamma_symbol(),
                gamma_shortcircuit_point_polar = shortcircuit_point.get_gamma_polar()))
    print('\n')
    
    # At the begin of the line
        
    input_line_length = caculate_line_length_at_mainbranch_and_stub_to_get_maxpower(start_point = point_A, 
                                                                                    gate_point = point_C, 
                                                                                    equivalent_point_name = 's_max', 
                                                                                    line_impedance = Z0_value,
                                                                                    end_stub_point = shortcircuit_point,
                                                                                    gate = 'input')
                                                        
    # At the end of the line

    output_line_length = caculate_line_length_at_mainbranch_and_stub_to_get_maxpower(start_point = point_B, 
                                                                                     gate_point = point_D, 
                                                                                     equivalent_point_name = 'L_max', 
                                                                                     line_impedance = Z0_value,
                                                                                     end_stub_point = shortcircuit_point,
                                                                                     gate = 'output')
                                                                                         

    input("Press Enter to stop this script >>")
    
def caculate_Gamma_short_circuit_stub(start_point, end_point, line_name): 
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
    
    lamda = '\u03BB'   
    
    
    
    print('\t{admittance_start_point} = {admittance_start_point_value}'\
        .format(admittance_start_point = start_point.get_admittance_symbol(),
                admittance_start_point_value = start_point.get_admittance()))
    print('\n')
    
    print('\t{gamma_start_point} = {gamma_start_point_formula} = {gamma_start_point_polar}'\
        .format(gamma_start_point = start_point.get_gamma_symbol(),
                gamma_start_point_formula = start_point.get_gamma_formula(depend_on = 'admittance'),
                gamma_start_point_polar = start_point.get_gamma_polar()))
    print('\n')
    
    line = SL(name = line_name,
           lamda = lamda,
           point_1 = start_point,
           point_2 = end_point)

    line_length = line.get_absolute_length()
    print('\t{line} = {line_length}'\
        .format(line = line.get_line_symbol(),
                line_length = line_length))
    print('\n')

    return line_length
    
def plot_smith_chart(src_point, des_point, intersection, stub_in_point, stub_out_point, line_impedance, gate):
    """
        @ BriefL:   Draw the Smith graph from known parameters
        @ Param:    
                    Y_init_value: Conductive resistance at the initial point
                    Y_inter_value: Conductive resistance at the equivalent_point
                    Gamma_final_value: reflectance at the destination point
                    Gamma_init_value: reflectance at the initial point
                    gate: The gate of the scattering matrix
    """

    fig, axes = plt.subplots(2, len(intersection), subplot_kw={'projection': 'polar'})
    
    for point in intersection:
        normalized_admittance_intersection = point.get_admittance(Nomalize = True)
        try:
            Y_inter_value = np.append(Y_inter_value, normalized_admittance_intersection)
        except NameError:
            Y_inter_value = np.array([normalized_admittance_intersection])
    
    boder_point = SP(name = 'border', 
                     gamma = 1, 
                     line_impedance = line_impedance)
                                 
    for index, point in enumerate(intersection):
        try:
            ax1 = axes[0][index]
            ax2 = axes[1][index]
        except TypeError:
            ax1 = axes[0]
            ax2 = axes[1]
        
        p1 = ax1.scatter(des_point.get_gamma_phase(round_index = None), 
                         des_point.get_gamma_module(round_index = None), 
                         marker='o', 
                         s=100, 
                         color = 'r', 
                         alpha = 1, 
                         label = des_point.get_impedance_symbol(Nomalize = True))
        p2 = ax1.scatter(des_point.get_gamma_phase(round_index = None) + np.pi, 
                         des_point.get_gamma_module(round_index = None), 
                         marker='x', 
                         linewidths = 3, 
                         color = 'r', 
                         alpha = 1, 
                         label = des_point.get_admittance_symbol(Nomalize = True))
        p3 = ax1.scatter(src_point.get_gamma_phase(round_index = None), 
                         src_point.get_gamma_module(round_index = None), 
                         marker='o', 
                         s=100, 
                         color = 'b', 
                         alpha = 1, 
                         label = src_point.get_impedance_symbol(Nomalize = True))
        p4 = ax1.scatter(src_point.get_gamma_phase(round_index = None) + np.pi, 
                         src_point.get_gamma_module(round_index = None), 
                         marker='x', 
                         linewidths = 3, 
                         color = 'b', 
                         alpha = 1, 
                         label = src_point.get_admittance_symbol(Nomalize = True))
        p5 = ax1.scatter(point.get_gamma_phase(round_index = None), 
                         point.get_gamma_module(round_index = None), 
                         marker='o', 
                         s=100, 
                         color = 'orange', 
                         alpha = 1, 
                         label = point.get_impedance_symbol(Nomalize = True))
        p6 = ax1.scatter(point.get_gamma_phase(round_index = None) + np.pi, 
                         point.get_gamma_module(round_index = None), 
                         marker='x', 
                         linewidths = 3, 
                         color = 'orange', 
                         alpha = 1, 
                         label = point.get_admittance_symbol(Nomalize = True))
        
        theta, module = des_point.get_isometric_gamma_vector()
        ax1.plot(theta, module, color = 'c')
        theta, module = boder_point.get_isometric_gamma_vector()
        ax1.plot(theta, module, color = 'black')
        theta, module = src_point.get_isometric_impedance_realvalue_vector()
        ax1.plot(theta, module, color = 'violet')
        
        ax1.axes.xaxis.set_ticklabels([])
        ax1.axes.yaxis.set_ticklabels([])
        fontP = FontProperties()
        fontP.set_size('medium')
        title = 'note'
        ax1.legend(handles=[p1, p2, p3, p4, p5, p6], title = title, bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
        ax1.set_title('With {normalized_admittance_intersection} = {normalized_admittance_intersection_value}' \
            .format(normalized_admittance_intersection = point.get_admittance_symbol(Nomalize = True),
                    normalized_admittance_intersection_value = point.get_admittance(Nomalize = True)) 
            + '\nOn main circuit')
        
        p7 = ax2.scatter(stub_in_point[index].get_gamma_phase(round_index = None), 
                         stub_in_point[index].get_gamma_module(round_index = None), 
                         marker='o', 
                         s=100, 
                         color = 'b', 
                         alpha = 1, 
                         label = stub_in_point[index].get_impedance_symbol(Nomalize = True))
        p8 = ax2.scatter(stub_in_point[index].get_gamma_phase(round_index = None) + np.pi, 
                         stub_in_point[index].get_gamma_module(round_index = None), 
                         marker='x', 
                         linewidths = 3, 
                         color = 'b', 
                         alpha = 1, 
                         label = stub_in_point[index].get_admittance_symbol(Nomalize = True))
        p9 = ax2.scatter(stub_out_point.get_gamma_phase(round_index = None), 
                         stub_out_point.get_gamma_module(round_index = None), 
                         marker='o', 
                         s=100, 
                         color = 'r', 
                         alpha = 1, 
                         label = stub_out_point.get_impedance_symbol(Nomalize = True))
        p10 = ax2.scatter(stub_out_point.get_gamma_phase(round_index = None) + np.pi, 
                          stub_out_point.get_gamma_module(round_index = None), 
                          marker='x', 
                          linewidths = 3, 
                          color = 'r', 
                          alpha = 1, 
                          label = stub_out_point.get_admittance_symbol(Nomalize = True))
        
        theta, module = boder_point.get_isometric_gamma_vector()
        ax2.plot(theta, module, color = 'black')
 
        ax2.axes.xaxis.set_ticklabels([])
        ax2.axes.yaxis.set_ticklabels([])
        fontP = FontProperties()
        fontP.set_size('medium')
        title = 'note'
        ax2.set_title('On stub circuit')
        ax2.legend(handles=[p7, p8, p9, p10], title = title, bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP) 
    
    fig.suptitle('Impedance matching at {}'.format(gate), fontsize=16)
    fig.show()  

def find_intersection(start_point, equivalent_point, line_impedance, gate):
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
        intersection_name = 'a'
    elif gate == 'output':
        intersection_name = 'b'
    else:
        raise Exception("Unknown parameter '{}'".format(gate))

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
    
    for imag_value in Yit_norm_iv:
        value = complex(YL_norm_rv, imag_value)
        intersection_i = SP(name = intersection_name,
                                 admittance = value,
                                 line_impedance = line_impedance,
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

    return intersection

def find_equivalent_point_for_max_power(gate_point, equivalent_point_name, line_impedance):
    
    print('For maximum power gain:')
    Gamma_eq_value = gate_point.get_gamma().conjugate()
    equivalent_point = SP(name = equivalent_point_name, 
                          gamma = Gamma_eq_value, 
                          line_impedance = line_impedance)

    print('\t{gamma_equivalent_point} = {gamma_gate_point}* = {gamma_equivalent_point_value}'\
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
    
    return equivalent_point

def find_stub_in_point(start_point, intersection, line_impedance):
    
    for point in intersection:
        Y_inter_nv = point.get_admittance(Nomalize = True)    
        Y_src_point_nv = start_point.get_admittance(Nomalize = True)  
        Y_stub_in_nv = Y_inter_nv - Y_src_point_nv
        stub_in_point_i = SP(name = '_stub',
                        admittance = Y_stub_in_nv,
                        line_impedance = line_impedance,
                        Nomalize = True)                                     
        try:
            stub_in_point = np.append(stub_in_point, stub_in_point_i)
        except NameError: 
            stub_in_point = np.array([stub_in_point_i])
    
    return stub_in_point

def caculate_all_line_lenghts(point, equivalent_point, stub_in_point_i, start_point, shortcircuit_point, gate):
    
    if gate == 'input':
        mainbranch_line_name = 'd1'
        stub_name = 'l1'
    elif gate == 'output':
        mainbranch_line_name = 'd2'
        stub_name = 'l2'
    else:
        raise Exception("Unknown parameter: '{}'".format(gate))
    
    print('With {normalized_admittance_intersection} = {normalized_admittance_intersection_value}, we have: \n'\
        .format(normalized_admittance_intersection = point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_intersection_value = point.get_admittance(Nomalize = True)))
    d1 = caculate_Gamma_short_circuit_stub(point, 
                                           equivalent_point, 
                                           mainbranch_line_name) 
    print('\t{normalized_admittance_stub_in_point} = {normalized_admittance_intersection} - {normalized_admittance_src_point} = {normalized_admittance_stub_in_point_value}'\
        .format(normalized_admittance_stub_in_point = stub_in_point_i.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_intersection = point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_src_point = start_point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_stub_in_point_value = stub_in_point_i.get_admittance(Nomalize = True)))     
    print('\n')
    l1 = caculate_Gamma_short_circuit_stub(stub_in_point_i, 
                                           shortcircuit_point, 
                                           stub_name)    
    
    return d1, l1

def caculate_line_length_at_mainbranch_and_stub_to_get_maxpower(start_point, gate_point, equivalent_point_name, line_impedance, end_stub_point, gate):
    
    print('{gamma_start_point} = {gamma_start_point_value}'\
        .format(gamma_start_point = start_point.get_gamma_symbol(),
                gamma_start_point_value = start_point.get_gamma_polar()))                                       
    print('\n')
    
    
    
    print('{normalized_admittance_start_point} = {normalized_admittance_start_point_value}'\
        .format(normalized_admittance_start_point = start_point.get_impedance_symbol(Nomalize = True),
                normalized_admittance_start_point_value = start_point.get_admittance(Nomalize = True)))
    print('\n')
    
    print('{normalized_admittance_start_point} = {normalized_admittance_start_point_value}'\
        .format(normalized_admittance_start_point = start_point.get_admittance_symbol(Nomalize = True),
                normalized_admittance_start_point_value = start_point.get_admittance(Nomalize = True)))
    print('\n')
    
    equivalent_point = find_equivalent_point_for_max_power(gate_point, equivalent_point_name, line_impedance)
    
    intersection = find_intersection(start_point, equivalent_point, line_impedance, gate)
    
    stub_in_point = find_stub_in_point(start_point, intersection, line_impedance)
    
    for index, stub_in_point_i in enumerate(stub_in_point):
        d1, l1 = caculate_all_line_lenghts(intersection[index], equivalent_point, stub_in_point_i, start_point, end_stub_point, gate)
        try:
            result = np.append(result, (d1, l1))
        except NameError:
            result = np.array([(d1, l1)])
    
    plot_smith_chart(start_point, 
                     equivalent_point, 
                     intersection, 
                     stub_in_point, 
                     end_stub_point, 
                     line_impedance, 
                     gate)
    
    return result   
    

if __name__ == '__main__': 
    main()
