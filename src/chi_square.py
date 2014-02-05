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
from math import pow
from collections import defaultdict, Counter
#==============================================================================
#--------------------------------Constants-------------------------------------
#==============================================================================
DEBUG = True
ROWS = 2
#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    if len(sys.argv) < 3:
        min_prob = 0.05
    else:
        min_prob = float(sys.argv[2])
        
    hw5 = ChiSquare(min_prob)
    hw5.PrintFeatureList()
    hw5.FilterFeatures()

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
    def __init__(self, min_prob):
        self.classes = defaultdict(int)
        self.instance_count = 0
        self.features = defaultdict(float)
        self.filtered_features = set()
        self.features_by_class = defaultdict(lambda: defaultdict(int))
        self.instances = []        
        
        
        self.ExtractFeatures()
        self.degree_of_freedom = (ROWS - 1) * (len(self.classes) - 1)
        self.max_chi_score = self.GetMaxChiScore(min_prob)
        self.CalculateChiScores()

    ##-------------------------------------------------------------------------
    ## FilterFeatures()
    ##-------------------------------------------------------------------------
    ##    Description:        description
    ##
    ##    Arguments:        arguments
    ##
    ##    Calls:                calls
    ##
    ##    Returns:            returns
    ##-------------------------------------------------------------------------
    def FilterFeatures(self):
        filtered_vector_file = open("filtered.vectors.txt", 'w')
        
        for feat in self.features:
            if self.features[feat] <= self.max_chi_score:
                self.filtered_features.add(feat)
        filtered_vector_file.write("Number of related features: " + str(len(self.filtered_features)) + os.linesep)
        
        for i in self.instances:
            filtered_vector_file.write(i.label + " ")
            for j in i.features:
                feat = j[0]
                if feat in self.filtered_features:
                    filtered_vector_file.write(":".join(j) + " ")
            
            filtered_vector_file.write(os.linesep)
        
        filtered_vector_file.close()
    
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
            classes = list(self.classes)
            for i in range(ROWS):
                for j in range( len(classes) ):
                    score += pow(contingency_table[i][j] - expected_table[i][j], 2) / expected_table[i][j]
            
            
            
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
        contingency_table = [[0.0 for x in range(len(self.classes) + 1)] for x in range(ROWS + 1)]
        expected_table = [[0.0 for x in range(len(self.classes) + 1)] for x in range(ROWS + 1)]
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
            
        for j in range(2):
            for k in range( len(classes) ):
                contingency_table[j][len(self.classes)] += contingency_table[j][k]
                contingency_table[ROWS][k] += contingency_table[j][k]
                
                
        #create the table of expected values
        for k in range(ROWS): 
            for l in range( len(classes) ):
                expected_table[k][l] =   contingency_table[k][len(self.classes)] \
                                       * contingency_table[ROWS][l]\
                                       / self.instance_count
        
        
#         for j in range(2):
#             for k in range( len(classes) ):
#                 contingency_table[j][len(self.classes)] += contingency_table[j][k]
#                 contingency_table[2][k] += contingency_table[j][k]
#                 expected_table[j][len(self.classes)] += expected_table[j][k]
#                 expected_table[2][k] += expected_table[j][k]
                
        
        
        
        return contingency_table, expected_table


    ##-------------------------------------------------------------------------
    ## GetMaxChiScore()
    ##-------------------------------------------------------------------------
    ##    Description:        description
    ##
    ##    Arguments:        arguments
    ##
    ##    Calls:                calls
    ##
    ##    Returns:            returns
    ##-------------------------------------------------------------------------
    def GetMaxChiScore(self, prob):
        return 9.488
    

    ##-------------------------------------------------------------------------
    ## PrintFeatureList()
    ##-------------------------------------------------------------------------
    ##    Description:        description
    ##
    ##    Arguments:        arguments
    ##
    ##    Calls:                calls
    ##
    ##    Returns:            returns
    ##-------------------------------------------------------------------------
    def PrintFeatureList(self):
        for feat in sorted(self.features, key=self.features.get, reverse=True):
            doc_count = 0
            for cls in self.classes:
                if feat in self.features_by_class[cls]:
                    doc_count += self.features_by_class[cls][feat]
                else:
                    doc_count += 0
            print(feat + "\t" + str(self.features[feat]) + "\t" + str(doc_count))
             
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