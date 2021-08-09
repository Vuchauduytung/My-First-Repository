# System framework
import numpy as np
from sympy import *
from cmath import *
import sympy.solvers as solv

# User framework
from SmithClass import SmithPoint as SP
from SmithClass import SmithLine as SL
import SmithChart as SC


solution = ''

def caculate_line_length_at_mainbranch_and_stub_to_get_maxpower(start_point, gate_point, equivalent_point_name, line_impedance, end_stub_point, gate):
    # Hàm này tính toán chiều dài dây chêm và dây ở mạch chính để có công suất cực đại 
    # Hàm này chỉ áp dụng cho 1 gate
    # start_point: điểm bắt đầu
    # gate_point: điểm đầu vào của ma trận tán xạ
    # equivalent_point_name: điểm tương đương trong phối hợp trở kháng
    # line_impedance : Trở kháng đường dây
    # end_stub_point: điểm cuối cùng của stub
    # gate: "'input' hoặc 'output'"
    # ret: chiều dài đường dây bù thêm trên nhánh chính và stub
    
    global solution
    
    solution += '{gamma_start_point} = {gamma_start_point_value}'\
        .format(gamma_start_point = start_point.get_gamma_symbol(),
                gamma_start_point_value = start_point.get_gamma_polar())
    solution += '\n\n' 
    
    solution += '{normalized_admittance_start_point} = {normalized_admittance_start_point_value}'\
        .format(normalized_admittance_start_point = start_point.get_impedance_symbol(Nomalize = True),
                normalized_admittance_start_point_value = start_point.get_admittance(Nomalize = True))
    solution += '\n\n'
 
    solution += '{normalized_admittance_start_point} = {normalized_admittance_start_point_value}'\
        .format(normalized_admittance_start_point = start_point.get_admittance_symbol(Nomalize = True),
                normalized_admittance_start_point_value = start_point.get_admittance(Nomalize = True))
    solution += '\n\n'
    
    equivalent_point = find_equivalent_point_for_max_power(gate_point, equivalent_point_name, line_impedance)
    
    intersection = find_intersection(start_point, equivalent_point, line_impedance, gate)
    
    stub_in_point = find_stub_in_point(start_point, intersection, line_impedance)
    
    for index, stub_in_point_i in enumerate(stub_in_point):
        d1, l1 = caculate_all_line_lenghts(intersection[index], equivalent_point, stub_in_point_i, start_point, end_stub_point, gate)
        try:
            result.append((d1, l1))
        except NameError:
            result = [(d1, l1)]
    
    SC.plot_smith_chart(start_point, 
                        equivalent_point, 
                        intersection, 
                        stub_in_point, 
                        end_stub_point, 
                        line_impedance, 
                        gate)
    return result   

def find_equivalent_point_for_max_power(gate_point, equivalent_point_name, line_impedance):
    # 
    global solution
    
    solution += 'For maximum power gain:'
    
    Gamma_eq_value = gate_point.get_gamma().conjugate()
    equivalent_point = SP(name = equivalent_point_name, 
                          gamma = Gamma_eq_value, 
                          line_impedance = line_impedance)
    
    solution += '\t{gamma_equivalent_point} = {gamma_gate_point}* = {gamma_equivalent_point_value}'\
        .format(gamma_equivalent_point = equivalent_point.get_gamma_symbol(),
                gamma_gate_point = gate_point.get_gamma_symbol(),
                gamma_equivalent_point_value = equivalent_point.get_gamma_polar())
    solution += '\n\n'
    
    solution += '{impedance_equivalent_point} = {impedance_equivalent_point_formula} = {impedance_equivalent_point_value}'\
        .format(impedance_equivalent_point = equivalent_point.get_impedance_symbol(), 
                impedance_equivalent_point_formula = equivalent_point.get_impedance_formula(),
                impedance_equivalent_point_value = equivalent_point.get_impedance())
    solution += '\n\n'

    solution += '{normalized_impedance_equivalent_point} = {normalized_impedance_equivalent_point_value}'\
        .format(normalized_impedance_equivalent_point = equivalent_point.get_impedance_symbol(Nomalize = True),
                normalized_impedance_equivalent_point_value = equivalent_point.get_impedance(Nomalize = True))
    solution += '\n\n'
    
    return equivalent_point

def find_intersection(start_point, equivalent_point, line_impedance, gate):
    """
        @brief      Caculate and display result for impedance matching problem
        @param      Zw_value          wire impedance
        @param      ZL_value          load impedance
        @param      Gamma_eq_value    equivalent reflectance looking at starting point of the line
    """
    
    if gate == 'input':
        intersection_name = 'a'
    elif gate == 'output':
        intersection_name = 'b'
    else:
        raise Exception("Unknown parameter '{}'".format(gate))

    Gamma_eq_mv = equivalent_point.get_gamma_module()     
  
    global solution
    
    solution += '{module_gamma_equivalent_point} = {module_gamma_equivalent_point_value}'\
        .format(module_gamma_equivalent_point = equivalent_point.get_module_gamma_symbol(),
                module_gamma_equivalent_point_value = Gamma_eq_mv)
    solution += '\n\n'
    
    gm_isometric_equation = equivalent_point.get_gm_isometric_equation()
    # Real value of load admittance normalized to Z0
    YL_norm_rv = start_point.get_admittance(Nomalize = True).real
    # Image value of load admittance normalized to Z0
    Yit_norm_iv = find_cmg_cri_intersection(gm_isometric_equation, YL_norm_rv)
    
    solution += 'Look up Smith chart, we have:'
    
    for imag_value in Yit_norm_iv:
        value = complex(YL_norm_rv, imag_value)
        intersection_i = SP(name = intersection_name,
                                 admittance = value,
                                 line_impedance = line_impedance,
                                 Nomalize = True)
        try:
            intersection = np.append(intersection, intersection_i)
            solution += '\tor {normalized_admittance_intersection} = {normalized_admittance_intersection_value}'\
                .format(normalized_admittance_intersection = intersection_i.get_admittance_symbol(Nomalize = True),
                        normalized_admittance_intersection_value = intersection_i.get_admittance(Nomalize = True))
        except NameError:
            intersection = np.array([intersection_i])
            solution += '\t{normalized_admittance_intersection} = {normalized_admittance_intersection_value}'\
                .format(normalized_admittance_intersection = intersection_i.get_admittance_symbol(Nomalize = True),
                        normalized_admittance_intersection_value = intersection_i.get_admittance(Nomalize = True))
    solution += '\n\n'            
    return intersection

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

    global solution
    
    solution += 'With {normalized_admittance_intersection} = {normalized_admittance_intersection_value}, we have: \n'\
        .format(normalized_admittance_intersection = point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_intersection_value = point.get_admittance(Nomalize = True))
    solution += '\n\n'    
    
    d1 = caculate_Gamma_short_circuit_stub(point, 
                                           equivalent_point, 
                                           mainbranch_line_name) 

    solution += '\t{normalized_admittance_stub_in_point} = {normalized_admittance_intersection} - {normalized_admittance_src_point} = {normalized_admittance_stub_in_point_value}'\
        .format(normalized_admittance_stub_in_point = stub_in_point_i.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_intersection = point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_src_point = start_point.get_admittance_symbol(Nomalize = True), 
                normalized_admittance_stub_in_point_value = stub_in_point_i.get_admittance(Nomalize = True))
    solution += '\n\n'

    l1 = caculate_Gamma_short_circuit_stub(stub_in_point_i, 
                                           shortcircuit_point, 
                                           stub_name)    
    return d1, l1

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
    
    global solution
    
    solution += '\t{admittance_start_point} = {admittance_start_point_value}'\
        .format(admittance_start_point = start_point.get_admittance_symbol(),
                admittance_start_point_value = start_point.get_admittance())
    solution += '\n\n'
    
    solution += '\t{gamma_start_point} = {gamma_start_point_formula} = {gamma_start_point_polar}'\
        .format(gamma_start_point = start_point.get_gamma_symbol(),
                gamma_start_point_formula = start_point.get_gamma_formula(depend_on = 'admittance'),
                gamma_start_point_polar = start_point.get_gamma_polar())
    solution += '\n\n'

    line = SL(name = line_name,
           lamda = lamda,
           point_1 = start_point,
           point_2 = end_point)

    line_length = line.get_absolute_length()
    
    solution += '\t{line} = {line_length}'\
        .format(line = line.get_line_symbol(),
                line_length = line_length)
    solution += '\n\n'
    return line

def find_equivalent_point_for_max_power(gate_point, equivalent_point_name, line_impedance):
    
    global solution
    
    solution += 'For maximum power gain:'
    
    Gamma_eq_value = gate_point.get_gamma().conjugate()
    equivalent_point = SP(name = equivalent_point_name, 
                          gamma = Gamma_eq_value, 
                          line_impedance = line_impedance)
    
    solution += '\t{gamma_equivalent_point} = {gamma_gate_point}* = {gamma_equivalent_point_value}'\
        .format(gamma_equivalent_point = equivalent_point.get_gamma_symbol(),
                gamma_gate_point = gate_point.get_gamma_symbol(),
                gamma_equivalent_point_value = equivalent_point.get_gamma_polar())
    solution += '\n\n'
    
    solution += '{impedance_equivalent_point} = {impedance_equivalent_point_formula} = {impedance_equivalent_point_value}'\
        .format(impedance_equivalent_point = equivalent_point.get_impedance_symbol(), 
                impedance_equivalent_point_formula = equivalent_point.get_impedance_formula(),
                impedance_equivalent_point_value = equivalent_point.get_impedance())
    solution += '\n\n'

    solution += '{normalized_impedance_equivalent_point} = {normalized_impedance_equivalent_point_value}'\
        .format(normalized_impedance_equivalent_point = equivalent_point.get_impedance_symbol(Nomalize = True),
                normalized_impedance_equivalent_point_value = equivalent_point.get_impedance(Nomalize = True))
    solution += '\n\n'
    return equivalent_point



