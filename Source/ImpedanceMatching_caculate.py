# System framework
from sympy import *
from cmath import *
import sys

# User framework
from Modules.Library.SmithClass import SmithPoint as SP
from Modules.Library.SmithClass import SmithLine as SL
import Modules.Library.CaculateSupport as CS
from Modules.Library.SmithChart import *
from Modules.User_Interface.DataExport import *


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
    
    # Update solution
    CS.solution += '\t{Gamma_in} = {Gamma_in_value}'\
        .format(Gamma_in = '\u0393in',
                Gamma_in_value = Gamma_in_value)
    CS.solution += '\n'
    
    CS.solution += '\t{Gamma_out} = {Gamma_out_value}'\
        .format(Gamma_out = '\u0393out',
                Gamma_out_value = Gamma_out_value)
    CS.solution += '\n'
    
    CS.solution += '\t{Zs} = {Zs_value}'\
        .format(Zs = 'Zs',
                Zs_value = Zs_value)
    CS.solution += '\n'
    
    CS.solution += '\t{ZL} = {ZL_value}'\
        .format(ZL = 'ZL',
                ZL_value = ZL_value)
    CS.solution += '\n'
    
    CS.solution += '\t{Z0} = {Z0_value}'\
        .format(Z0 = 'Z0',
                Z0_value = Z0_value)
    CS.solution += '\n'
    
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
    
    CS.solution += '\n'
    CS.solution += '----------------------------------------Solution-------------------------------------'
    CS.solution += '\n'
    CS.solution += 'Due to short circuit at the end of the stub, we have:'
    CS.solution += '\n'
    CS.solution += '\t{gamma_shortcircuit_point} = {gamma_shortcircuit_point_polar}'\
        .format(gamma_shortcircuit_point = shortcircuit_point.get_gamma_symbol(),
                gamma_shortcircuit_point_polar = shortcircuit_point.get_gamma_polar())
    CS.solution += '\n\n'
    
    # At the begin of the line
        
    input_line = CS.caculate_line_length_at_mainbranch_and_stub_to_get_maxpower(start_point = point_A, 
                                                                                       gate_point = point_C, 
                                                                                       equivalent_point_name = 's_max', 
                                                                                       line_impedance = Z0_value,
                                                                                       end_stub_point = shortcircuit_point,
                                                                                       gate = 'input')
                                                        
    # At the end of the line

    output_line = CS.caculate_line_length_at_mainbranch_and_stub_to_get_maxpower(start_point = point_B, 
                                                                                        gate_point = point_D, 
                                                                                        equivalent_point_name = 'L_max', 
                                                                                        line_impedance = Z0_value,
                                                                                        end_stub_point = shortcircuit_point,
                                                                                        gate = 'output')
    CS.solution += '\n\n'
    CS.solution += '----------------------------------------Summary-------------------------------------'
    CS.solution += '\n\n'
    
    # Update solution summary
    CS.solution += 'At input, we have {} solution:\n\n'.format(len(input_line))
    for input_solution in input_line:
        CS.solution += '\t\t{main_branch_line} = {main_branch_line_lengthvalue}, {stub} = {stub_lengthvalue}'\
            .format(main_branch_line = input_solution[0].get_line_symbol(),
                    main_branch_line_lengthvalue = input_solution[0].get_absolute_length(),
                    stub = input_solution[1].get_line_symbol(),
                    stub_lengthvalue = input_solution[1].get_absolute_length())
        CS.solution += '\n\n'
    
    CS.solution += 'At output, we have {} solution:\n\n'.format(len(output_line))
    for output_solution in output_line:
        CS.solution += '\t\t{main_branch_line} = {main_branch_line_lengthvalue}, {stub} = {stub_lengthvalue}'\
            .format(main_branch_line = output_solution[0].get_line_symbol(),
                    main_branch_line_lengthvalue = output_solution[0].get_absolute_length(),
                    stub = output_solution[1].get_line_symbol(),
                    stub_lengthvalue = output_solution[1].get_absolute_length())
        CS.solution += '\n\n'   
         
    solution_filename = sys.argv[1]
    
    if len(sys.argv) == 3:
        if sys.argv[2] == 'show_solution':
            print(CS.solution)
    
    # print(CS.solution)
    
    solution_export(CS.solution, solution_filename)
                                                                                             
    input("Press Enter to stop this script >>")


if __name__ == '__main__': 
    main()
