'''
#==============================================================================
cky.py
Created on Jan 29, 2014
@author: aelshen
#==============================================================================
'''

import os
import sys
from chi_square import ChiSquare
#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True

#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    if len(sys.argv) < 3:
        print("filter_features.py requires at least two arguments:"
               + os.linesep + "\t(1)minimum probability"
               + os.linesep + "\t(2+)training vector file followed by any other vector files to be filtered")
        sys.exit()
        
    min_prob = float(sys.argv[1])
    
    files = []
    for i in sys.argv[2:]:
        files.append(i)
    
    hw5 = ChiSquare(min_prob, files[0])
    
    for file in files:
        hw5.FilterFeaturesFromFile(file) 
    
    print("Hello, World!")

#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )