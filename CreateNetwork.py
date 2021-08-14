# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from NetworkSimulation import genrate_network as NTW


class VisualNetwork_input_output:
    def __init__(self,X={},Y={},A={},E={}, Z={}, S={}):
        
        ## class to creat initial network, this class has two parts initial network and scenario generation 
        #file location for input data - nodes and edges
        file_location = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/InputData.xlsx'
        self.OutSave= "C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation"
    
        #import Node and Edge List with their attributes
        self.Edgeslist=pd.read_excel(file_location, sheet_name='Edges')
        self.UEdgeslist=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/edg1.csv')
        
        self.Nodeslist=pd.read_excel(file_location, sheet_name='Nodes')
        self.UNodeslist=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Node1.csv')
        
        #now updated the capacities value based on optimization output
        #first Update Primary capacity
        for key, value in S.items():
            self.Edgeslist.loc[self.Edgeslist['PartKey'] == key, ['SS']] = value -value+90
        self.Edgeslist['SS'] = self.Edgeslist['SS'].fillna(0)
        for key, value in X.items():
            self.UNodeslist.loc[self.UNodeslist['PartKey'] == key, ['CapacityR']] = value - value +90
        self.UNodeslist['CapacityR'] = self.UNodeslist['CapacityR'].fillna(0)
        #Update Secondary Capacity 
        for key, value in Y.items():
            self.UNodeslist.loc[self.UNodeslist['PartKey'] == key, ['CapacitySc']] = value -value + 90
        self.UNodeslist['CapacitySc'] = self.UNodeslist['CapacitySc'].fillna(0)
        #backUpCapacity 
        for key, value in A.items():
            self.UNodeslist.loc[self.UNodeslist['PartKey'] == key, ['CapacityBck']] = value -value + 90
        self.UNodeslist['CapacityBck'] = self.UNodeslist['CapacityBck'].fillna(0)
        #Active or not Secondary Capacity 
        for key, value in E.items():
            self.UNodeslist.loc[self.UNodeslist['PartKey'] == key, ['SC_YesNo']] = value - value + 90
        self.UNodeslist['SC_YesNo'] = self.UNodeslist['SC_YesNo'].fillna(0)
        #Active or not backUpCapacity 
        for key, value in A.items():
            self.UNodeslist.loc[self.UNodeslist['PartKey'] == key, ['BC_YesNo']] = value - value + 90
        self.UNodeslist['BC_YesNo'] = self.UNodeslist['BC_YesNo'].fillna(0)
 
        
        
        
    #class variables, shared between all instances of this class
    def mapnetwork(self):
        C1=NTW(self.UNodeslist,self.Edgeslist,self.OutSave)
        C1.smvsnetwork()








    

    

    
    






    
    
    
    







