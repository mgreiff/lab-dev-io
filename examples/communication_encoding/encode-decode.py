"""
Example demontsrating the hexadecimal encoding done to enable a minimal
representation and transferral of float64 arrays over the IP network
"""
# Import modules
import os
import sys
import inspect
import numpy as np

curdir  = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
rootdir = os.path.dirname(os.path.dirname(curdir))
moddir  = os.path.join(rootdir, "modules")
sys.path.insert(0,moddir) 
from pythonBeagle import encode_array_to_hex, encode_hex_to_array

# Run example
N = 10
vec_original  = np.random.rand(N,1)
hex_string    = encode_array_to_hex(vec_original)
vec_recovered = encode_hex_to_array(hex_string)

print "\n--- Random {}-dimensional vector--- \n\n{}".format(N, vec_original.T)
print "\n--- Minimal hexadecimal conversion --- \n\n{}".format(hex_string)
print "\n--- Converted back to float64 --- \n\n{}".format(vec_recovered.T)
print "\n--- Difference before and after converison --- \n\n{}".format(vec_original.T -  vec_recovered.T) 