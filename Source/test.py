import numpy as np
from plot_SmithChart import *

# a_vector = np.repeat(0.1, 50)
# b_vector = np.linspace(-4, 16, num = 50)
# plot_Smith(a_vector, b_vector)

Express = constant_module_gamma_function(2)
img_impedance = find_cmg_cri_intersection(Express, 1)
print(Express)
print(img_impedance)