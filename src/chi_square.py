'''
#==============================================================================
cky.py
/Users/aelshen/Documents/Dropbox/School/CLMS 2013-2014/Winter 2014/Ling 571-Deep Processing Techniques for NLP/hw2_571_aelshen/src/cky.py
Created on Jan 29, 2014
@author: aelshen
#==============================================================================
'''
import os
import sys
import fileinput
from collections import defaultdict, Counter
#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True

#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    hw5 = ChiSquare()
    print("Hello, World!")
#==============================================================================    
#---------------------------------Functions------------------------------------
#==============================================================================


#==============================================================================    
#----------------------------------Classes-------------------------------------
#==============================================================================
##-------------------------------------------------------------------------
## Class ChiSquare
##-------------------------------------------------------------------------
##    Description:        desciription
##
##    Arguments:         arguments
##
##
##    Properties:         properties
##
##    Calls:                  calls
##
##-------------------------------------------------------------------------
class ChiSquare:
    def __init__(self):
        self.classes = defaultdict(int)
        self.instance_count = 0
        self.features = defaultdict(float)
        self.features_by_class = defaultdict(lambda: defaultdict(int))
        self.instances = []
        
        
        self.ExtractFeatures()
        self.CalculateChiScores()

    ##-------------------------------------------------------------------------
    ## ExtractFeatures()
    ##-------------------------------------------------------------------------
    ##    Description:        description
    ##
    ##    Arguments:        arguments
    ##
    ##    Calls:                calls
    ##
    ##    Returns:            returns
    ##-------------------------------------------------------------------------
    def ExtractFeatures(self):
        instance_count = 0
        #for vector in fileinput.input():
        for line in open(sys.argv[1], 'r').readlines():
            feature_vector = []
            
            self.instance_count += 1
            line = line.split()
            label= line[0]
            self.classes[label] += 1
            
            for feat in line[1:]:
                feat,count = feat.split(":")
                self.features[feat] = float("-inf")
                feature_vector.append( (feat,count) )
                self.features_by_class[label][feat] += 1
                
                
            self.instances.append(Instance(label, feature_vector))
            
            
    ##-------------------------------------------------------------------------
    ## CalculateChiScores()
    ##-------------------------------------------------------------------------
    ##    Description:        description
    ##
    ##    Arguments:        arguments
    ##
    ##    Calls:                calls
    ##
    ##    Returns:            returns
    ##-------------------------------------------------------------------------
    def CalculateChiScores(self):
        for feature in self.features:
            score = 0.0
            contingency_table, expected_table = self.CreateTables(feature)
            
            
            
            self.features[feature] = score
        #end for feature in self.features:
        
    ##-------------------------------------------------------------------------
    ## CalculateTables()
    ##-------------------------------------------------------------------------
    ##    Description:        description
    ##
    ##    Arguments:        arguments
    ##
    ##    Calls:                calls
    ##
    ##    Returns:            returns
    ##-------------------------------------------------------------------------
    def CreateTables(self, feature):
        contingency_table = [[0.0 for x in range(len(self.classes) + 1)] for x in range(3)]
        expected_table = [[0.0 for x in range(len(self.classes) + 1)] for x in range(3)]
        classes = list(self.classes)
        
        #create the contingency table
        for i in range( len(classes) ):
            cls = classes[i]
            
            if feature in self.features_by_class[cls]:
                b_i = self.features_by_class[cls][feature]
            else:
                b_i = 0
            
            contingency_table[0][i] = b_i
            contingency_table[1][i] = self.classes[cls] - b_i
            
        #create the table of expected values
        for i in range( len(classes) ):
            cls = classes[i]
            
            if feature in self.features_by_class[cls]:
                b_i = self.features_by_class[cls][feature]
            else:
                b_i = 0
            
            contingency_table[0][i] = b_i
            contingency_table[1][i] = self.classes[cls] - b_i
        
        for j in range(2):
            for k in range( len(classes) ):
                contingency_table[j][len(self.classes)] += contingency_table[j][k]
                contingency_table[2][k] += contingency_table[j][k]
                expected_table[j][len(self.classes)] += expected_table[j][k]
                expected_table[2][k] += expected_table[j][k]
                
        
        
        
        return contingency_table, expected_table
             
##-------------------------------------------------------------------------
## Class Instance
##-------------------------------------------------------------------------
##    Description:        desciription
##
##    Arguments:         arguments
##
##
##    Properties:         properties
##
##    Calls:                  calls
##
##-------------------------------------------------------------------------
class Instance:
    def __init__(self, label, features):
        self.label = label
        self.features = features

#==============================================================================    
#------------------------------------------------------------------------------
#==============================================================================
if __name__ == "__main__":
    sys.exit( main() )