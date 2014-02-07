'''
#==============================================================================
chi_square.py
Created on Feb 5, 2014
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
COMMENTCHAR = '#'
ROWS = 2
chi_square_table = {1:{.10: 2.706, .05: 3.841, .025: 5.024, .01: 6.635, .001: 10.828},
                    2:{.10: 4.605, .05: 5.991, .025: 7.378, .01: 9.210, .001: 13.816},
                    3:{.10: 6.251, .05: 7.815, .025: 9.348, .01: 11.345, .001: 16.266},
                    4:{.10: 7.779, .05: 9.488, .025: 11.143, .01: 13.277, .001: 18.467},
                    5:{.10: 9.236, .05: 11.070, .025: 12.833, .01: 15.086, .001: 20.515},
                    6:{.10: 10.645, .05: 12.592, .025: 14.449, .01: 16.812, .001: 22.458},
                    7:{.10: 12.017, .05: 14.067, .025: 16.013, .01: 18.475, .001: 20.278},
                    8:{.10: 13.362, .05: 15.507, .025: 17.535, .01: 20.090, .001: 21.955},
                    9:{.10: 14.684, .05: 16.919, .025: 19.023, .01: 21.666, .001: 23.589},
                    10:{.10: 15.987, .05: 18.307, .025: 20.483, .01: 23.209, .001: 25.188}}
#==============================================================================
#-----------------------------------Main---------------------------------------
#==============================================================================
def main():
    hw5 = ChiSquare()
    hw5.PrintFeatureList()

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
    def __init__(self, min_prob = .05, input = None):
        self.classes = defaultdict(int)
        self.instance_count = 0
        self.features = defaultdict(float)
        self.filtered_features = set()
        self.features_by_class = defaultdict(lambda: defaultdict(int))
        self.instances = []     
        self.min_prob = min_prob  
        
        if input == None:
            input = sys.stdin
        else:
            input = open(input, 'r')
        
        self.ExtractFeatures(input)
        self.degree_of_freedom = (ROWS - 1) * (len(self.classes) - 1)
        self.max_chi_score = self.GetMaxChiScore()
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
    def FilterFeaturesFromFile(self, file):
        filtered_file_name = file.split("/")[-1]
        filtered_file_name = filtered_file_name.split(".")[:-1]
        filtered_file_name.extend(["filtered_" + str(self.min_prob)])

        filtered_vector_file = open(".".join(filtered_file_name), 'w')
        
        for feat in self.features:
            if self.features[feat] <= self.max_chi_score:
                self.filtered_features.add(feat)
        print("Chi score threshold: " + str(self.max_chi_score))
        print("Number of related features: " + str(len(self.filtered_features)) + os.linesep)
        
        
        for line in open(file, 'r').readlines():
            if not line.strip():
                continue
            line = line.split()
            label = line[0]
            filtered_vector_file.write(label + " ")
            for j in line[1:]:
                feat = j.split(":")[0]
                if feat in self.filtered_features:
                    filtered_vector_file.write(j + " ")
            
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
    def ExtractFeatures(self, input):
        instance_count = 0
        for line in input:
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
    def GetMaxChiScore(self):
        return chi_square_table[self.degree_of_freedom][self.min_prob]
    

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