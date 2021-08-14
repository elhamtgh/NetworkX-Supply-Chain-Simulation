# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 07:39:42 2019

@author: elham
"""
#This Modual calculate parameters for supply network:
#1.Demand
#2.Lead time 
#3.Saftey Stock based on LT and Service Level


import pandas as pd
import numpy as np
from NetworkSimulation import genrate_network
from CreateNetwork import VisualNetwork_input_output 
#from geopy.distance import geodesic
from haversine import haversine, Unit
import scipy.stats as st
import math as math
#in this modul we generate LT (based on distance and type of transportation) and then
#we will generate demand for our time period based on network connection and save them in a dataframe

VIO=VisualNetwork_input_output()#import our list from main modul - list edge and nodes
edgINF=VIO.Edgeslist
nodeINF = VIO.UNodeslist.set_index("ID", drop = False)#ID must be key to find nodes and thier relationship
SL = 0.95
Time_Period = 700
AVEGDEMAND=410
Stv_Demand=10
#print(edgINF)

#the following function find distance between each nodes
def distance_calc (row):
    Source=row['Source ID']
    Target=row ['Target ID']
    start = (nodeINF.loc[Source, "Lat"], nodeINF.loc[Source, "Long"])
    stop = (nodeINF.loc[Target, "Lat"], nodeINF.loc[Target, "Long"])
    #geodesic(start, stop).miles same as haversine
    #great_circle(start, stop).miles is the shortest distance between two points on the surface of a sphere, measured along the surface of the sphere 
    #(as opposed to a straight line through the sphere's interior). 
    return haversine(start, stop, unit=Unit.MILES)

#then based on distance we update the edge list
edgINF['distance'] = edgINF.apply (lambda row: distance_calc (row),axis=1)
#print(edgINF)
#now we need to link with our network to find connection between nodes and which edges are availble and valid
C1=genrate_network(VIO.UNodeslist,edgINF,VIO.OutSave)
C1.smvsnetwork()
#print(C1.network.edges(data=True))
#now for each node base on connection we measure demand

def demand2 (T):
    D2 = pd.DataFrame(0, index=np.arange(int(T)), columns=C1.network.nodes().keys())
    for j in range (T):
        D2.loc[j,'Final Node'] = int(np.random.normal(AVEGDEMAND,Stv_Demand))#update demand dataframe for focal firm
    D2.loc[0:T , : ].to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv', index=False)
    return D2


#the following generate the lead time and then we update the edge and save it.
def itr(i):
    def Lead_Time (row):
        a=0
        Cal1= row['distance']/ row ['Shipmment Speed']
        Cal2 = (Cal1 / row ['Shipment Operation'])*(row ['Distance Correction Multiplier'])
        if Cal2 < 3.0:
            max=3*Cal2+1
        else:
            max = 5* Cal2
        LT = round(np.random.triangular(a,Cal2,max))
        SDT = (a**2 + Cal2**2 + max**2 - a*Cal2 - a*max - Cal2*max)/18
        return LT, SDT
    
    edgINF['LT'] = edgINF.apply (lambda row: Lead_Time (row)[0] ,axis=1)
    edgINF['SDT_LT'] = edgINF.apply (lambda row: Lead_Time (row)[1] ,axis=1)
    #maxLT=max(edgINF['LT'])#find the max LT to generate demand for Focal Nodes -  because other tiers have leadtime 
    
    def Safty_Stock (row):
        AVGD = 50*AVEGDEMAND+row['SS']
        ST_Demand = Stv_Demand**2
        STDLT = row ['SDT_LT']**2
        LTMean = row['LT']
        Z = st.norm.ppf(1-(1-SL)/2)
        Safety_stock = Z*math.sqrt(AVGD*STDLT + LTMean*ST_Demand)
        return round(Safety_stock,0)
        
    edgINF['SSF'] = edgINF.apply (lambda row: Safty_Stock (row) ,axis=1)
    edgINF.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/edg1.csv', index=False)
    return edgINF
   


# 
 