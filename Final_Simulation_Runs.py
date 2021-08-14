# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 15:01:43 2020

@author: elham
"""
import ResilianceLevel
import pandas as pd
import DemandLT as Demand
import numpy as np
from CreateNetwork import VisualNetwork_input_output
from NetworkSimulation import genrate_network


class simulation:
    def __init__(self,run = None, Nodelist = [], Edgelist = [],name = None):
        self.Period = run #timePeriod (days)
        self.Edgdis = Edgelist #list of edge disrupted for current event
        self.Nodedis= Nodelist #list of node disrupted for current event 
        self.scname=name # name of disrution to save result
         
        
        
    def runsimulation (self,initial,ITR,Nevent,durIn, frq, svrt, Disruption_Type):
        Period =int(self.Period) #defined time period for our simulation 
        SCName = self.scname
        nodedisl = self.Nodedis #disrupted node list
        edgedisl = self.Edgdis #disrupted edge list 
        initial=initial#initial for simulation
        n=Nevent#number of event will happen in run simulation
        DUR =durIn#Creat Dictionary for disruption duration
        Type=Disruption_Type
        Svr=svrt
        Frq=frq
        LT_Change = {} #if edge is disrupted and LT can be changed
        #print("Typeee" + str (Type))
                        
#        for t in nodedisl:#Node disrupted
#            DUR1 = np.round(np.random.uniform(3,4),0) #Short Duration
#            DUR[t] = DUR1.astype(int)#change duration to int 
        
        for t in edgedisl:#Node disrupted
#            DUR1 = np.round(np.random.uniform(25,30),0) #Short Duration
#            DUR[t] = DUR1.astype(int)#change duration to int 
            LT_Change1 = np.round(np.random.uniform(8,9),0) #Short Duration
            LT_Change[t] = LT_Change1.astype(int)#change duration to int
        
        
        VIO=VisualNetwork_input_output()#input network info node, edge and their attributes models
        Node_DATA = VIO.UNodeslist.set_index("ID", drop = False) #save node info and add ID with their attributes
        Edge_DATA = VIO.UEdgeslist#edge to create the network
        
        print("******************************")
        C3=genrate_network(Node_DATA,Edge_DATA ,VIO.OutSave)
        C3.smvsnetwork()
        C3.network_metrics()
        print("******************************")
        for i in range(len(nodedisl)):
            print ("Disruption in node :" + str(nodedisl[i]) + "Shut down for:"+ str(DUR[i]))
            #print("with Frequency : every " + str(np.round((1/Node_DATA.loc[nodedisl[i],'Frequency']))) + " days")
            #print("with Severity :" + str(Node_DATA.loc[nodedisl[i],'Severity']))
        #print("with Duration :" + str(DUR))
        
        if ITR ==0:
            self.D=Demand.demand2(Period) #Generate empty list demand and save a data frame (N*P)
            #then call Resiliancelevel class to obtain resiliance level for first iteration
            print("******************************")
            print ("Iteration 1 : ")
            DF= pd.DataFrame([ResilianceLevel.Resiliance(Period,nodedisl ,edgedisl ,Frq ,Svr,DUR, LT_Change,SCName).SimResiliance(initial,n,ITR)])
            DF.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/Final.csv', index=True)#save Resiliance
            
        
        
        else:
            print("******************************")
            print ("Iteration "  + str(ITR+1) + " : ")
            FileName = str(nodedisl) + str(ITR)
            self.D1=Demand.demand2(Period)
            DF =pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/Final.csv')
            df = pd.DataFrame([ResilianceLevel.Resiliance(Period,nodedisl ,edgedisl , Frq ,Svr,DUR,Type, LT_Change,FileName).SimResiliance(initial,n,ITR)])
            DF = DF.append(df, ignore_index=True)#save resiliance level in a data frame
            #df2=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/TotalCost.csv')
            #DF2 = DF2.append(df2, ignore_index=True)
            DF.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/Final.csv', index=True)#save Resiliance

                
#            DF.loc['Mean Resiliance'] = DF.mean()
#            DF.to_csv('C:/Users/elham/Google Drive/ReSearch/Regression and relationship/NewupdateRisk/{}.csv'.format("Resiliance_" + str(SCName)), index=True)#save Resiliance 
#            #DF2.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/Performance.csv', index=False)#save Performance
#            
#            print("******************************")
#            print("Final Results after" + " : " + str(ITR) + " Runs")  
#            print(DF)         