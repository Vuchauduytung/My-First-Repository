# System framework
import numpy as np
from sympy import *
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from cmath import *

# User framework
from SmithClass import SmithPoint as SP
from CaculateSupport import *


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