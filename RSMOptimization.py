# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:18:49 2021

@author: elham
"""

#Optmization model for resilience management 
import pandas as pd
import DemandLT as D
import numpy as np

# first import the Model class from docplex.mp
from docplex.mp.model import Model
from CreateNetwork import VisualNetwork_input_output
import Scenariogeneration

            
def Optimization(Data1):

    Parts=Data1["Parts Name"].values #set Part
    Bpoint=Data1["Breakpoint"].values #set Part
    BpointQ=Data1["BreakPointQ"].values #set Part
    UsageRate = Data1["Usage_R"].values# Usage Rate for each part
    PercentageS = Data1["Secondary"].values # Percentage increase in unit cost of reserving capacity for partkfrom secondary supplier
    PercentageB = Data1["Backup"].values # Percentage increase in unit cost of reserving capacity for partkfrom back up 
    CostBreakpoint = Data1["BCost"].values #BreakPoint Cost 
    FixedCostB=Data1["FixedCostBackUp"].values #FixedCost of BackupSuppliers
    FixedCostS = Data1["FixedCostSecondary"].values# Fixed Cost Secondary Supplier
    PerunitCostP = Data1["PerUnitSurplusCapacity"].values # Perunit Cost Primary Supplier 
    CapacityP = Data1["Capacity"].values # Capacity Primaru Supplier 
    CapacityS = Data1["SecondaryCapacity"].values # Capacity Secondary Supplier
    CapacityB = Data1["BackUpCapacity"].values # Capacity Backup Supplier
    HoldingCost = Data1["SSCost"].values # Holding Cost for safety Stock at promary supplier locations
    COFXP = Data1["X_Cof"].values #CAllBack Primaru Supplier 
    COFYS = Data1["Y_Cof"].values # CAllBack Secondary Supplier
    COFZB = Data1["Z_Cof"].values # CAllBack Backup Supplier
    COFSS = Data1["S_Cof"].values # CAllBack SS
    INTER = Data1["inter"].values # CAllBack SS
    
    RateDic = dict(zip(Parts, UsageRate))# Usage Rate for each part
    PercentageSC = dict(zip(Parts, PercentageS))# reserving capacity cost for secondary supplier
    PercentageBC = dict(zip(Parts, PercentageB))# per unit cost for backup capacity
    UnitcostPri = dict(zip(Parts, PerunitCostP))# per unit cost for primary supplier  breakpoint
    FixedCostBv = dict(zip(Parts, FixedCostB))# FixedCost Backup 
    FixedCostSv = dict(zip(Parts, FixedCostS))# FixedCost Secondary 
    BreakpointCostPv = dict(zip(Bpoint, CostBreakpoint))# breakpoint cost 
    BreakpointQ = dict(zip(Bpoint, BpointQ))# breakpoint values 
    CapacityPDic = dict(zip(Parts, CapacityP))# Capacity Primary Supplier
    CapacitySDic = dict(zip(Parts, CapacityS))# Capacity Secondary Supplier 
    CapacityBDic = dict(zip(Parts, CapacityB))# Capacity Back Supplier 
    HoldingCostDIC = dict(zip(Parts, HoldingCost))#  Holding Cost for safety Stock at promary supplier locations
    COFXF = dict(zip(Parts, COFXP))# Capacity Primary Supplier
    COFYF = dict(zip(Parts, COFYS))# Capacity Secondary Supplier 
    COFZF = dict(zip(Parts, COFZB))# Capacity Back Supplier 
    COFSSF = dict(zip(Parts, COFSS))#  Holding Cost for safety Stock at promary supplier locations
    COFINT = dict(zip(Parts, INTER))#  Interpert
    
        
    #for connection with simulation part
    X={}#add primary capacity for simulation part
    Y={}#add secondary capacity for simulation part  
    A={}# add backup capacity for simulation part 
    E={}# binary variables if secondary is active and can use it 
    Z={}# binary variabe if back up  is active and can use it
    S={}#SafetyStock at Primary Supplier Location 
    
    
    #Demand
    Demand = int(np.random.normal(D.AVEGDEMAND,D.Stv_Demand))
    
    
    # create one model instance, with a name
    m = Model(name='Resilience Opmizimization')
    
    ##########time for decision Variables 
    #reserved capacity of partk primary supplier
    x = {(k) : m.continuous_var(name='x_{0}'.format(k), lb=0, ub=1) for k in Parts}
    #rSafety Stock of partk at primary supplier
    ss = {(k) : m.continuous_var(name='ss_{0}'.format(k)) for k in Parts}
    #Equal 1, if the secondary supplieriis selected
    e ={(k) : m.binary_var(name='e_{0}'.format(k)) for k in Parts}
    #Resereved capacity of partk secondary supplier
    y ={(k) : m.continuous_var(name='y_{0}'.format(k), lb=0, ub=1) for k in Parts}
    #Equal 1, if the backup supplieriis selected
    z ={(k) : m.binary_var(name='z_{0}'.format(k)) for k in Parts}
    #Resereved capacity of partk backup supplier
    a ={(k) : m.continuous_var(name='a_{0}'.format(k), lb=0, ub=1) for k in Parts}
    #Auxiliary variable to link the primary supplier capacity quantity tothe piece-wise linear capacity cost.
    v = {(j,k): m.binary_var(name='v_{0}_{1}'.format(j,k)) for j in Bpoint for k in Parts}
    #Auxiliary variable to link the secondary supplier capacity quantity tothe piece-wise linear capacity cost.
    l = {(j,k): m.binary_var(name='l_{0}_{1}'.format(j,k)) for j in Bpoint for k in Parts}
    #Binary variable to link the primary supplier capacity quantity tothe piece-wise linear capacity cost.
    s = {(j,k): m.binary_var(name='s_{0}_{1}'.format(j,k)) for j in Bpoint for k in Parts}
    #Binary variable to link the secondary supplier capacity quantity tothe piece-wise linear capacity cost.
    o = {(j,k): m.binary_var(name='o_{0}_{1}'.format(j,k)) for j in Bpoint for k in Parts}
            
    ###Constaraints 
    #capacity limitation for promary and backup supplier 
    for k in Parts:
            m.add_constraint(m.sum(l[j,k]  for j in Bpoint) == 1)
            m.add_constraint(m.sum(s[j,k]  for j in Bpoint) <= 1)
            m.add_constraint(m.sum(v[j,k]  for j in Bpoint) == 1)
            m.add_constraint(m.sum(o[j,k]  for j in Bpoint) <= 1)
            m.add_constraint(x[k]+y[k] == 1)
            m.add_constraint(e[k] <= 1)
            m.add_constraint(z[k] <= 1)
            m.add_constraint(a[k]*RateDic[k]*Demand - z[k]*CapacityBDic[k] <= 0 )
            m.add_constraint(y[k]*RateDic[k]*Demand - e[k]*CapacitySDic[k] <= 0 )
            m.add_constraint(ss[k]*RateDic[k]*Demand + x[k]*RateDic[k]*Demand - CapacityPDic[k] <= 0 )
            #m.add_constraint(ss[k]>= 0 )
    
            m.add_constraint(x[k]*RateDic[k]*Demand - m.sum(BreakpointQ[j] *v[j,k]  for j in Bpoint) <= 0 )
            m.add_constraint(v[1,k] -  s[1,k] <= 0 )
            m.add_constraint(v[7,k] -  s[6,k] <= 0 )
            for j in range(2,6):
                  m.add_constraint(v[j,k] -  s[j-1,k] - s[j-1,k] <= 0 )
                  m.add_constraint(l[j,k] -  o[j-1,k] - o[j-1,k] <= 0 )
                
            m.add_constraint(y[k]*RateDic[k]*Demand - m.sum(BreakpointQ[j] *l[j,k]  for j in Bpoint) <= 0 )
            m.add_constraint(l[1,k] -  o[1,k] <= 0 )
            m.add_constraint(l[7,k] -  o[6,k] <= 0 )
    # m.add_constraint(COFXF[k]*x[k] + COFYF[k]*y[k] + COFZF[k]*z[k]+ COFSSF[k]*ss[k] >=90 for k in Parts)
    # m.add_constraint(x['A/C Ducts']-ss['A/C Ducts']+COFINT['A/C Ducts'] >=1090)
        
        
    #objective value 
    objective= m.sum((BreakpointCostPv[j]*UnitcostPri[k]) *v[j,k] +BreakpointCostPv[j]*(1+ PercentageSC[k])*l[j,k] for j in Bpoint for k in Parts) + m.sum((1+PercentageBC[k])*UnitcostPri[k]*RateDic[k]*Demand*a[k] + z[k]*FixedCostBv[k]+ e[k]*FixedCostSv[k] + ss[k]*HoldingCostDIC[k] for k in Parts)
    m.minimize(objective)
    m.solve()
    obj = m.objective_value
    print("model solved with objective: {:g}".format(obj))
    #m.print_information()
    #m.print_solution()
    
    for k in Parts:
        print(k, ":" , round(x[k].solution_value*Demand*RateDic[k]))
        X.update({k:round(x[k].solution_value*Demand*RateDic[k])})
        print(k, ":" , round(y[k].solution_value*Demand))
        Y.update({k:round(y[k].solution_value*Demand*RateDic[k])})
        #print(k, ":" , round(a[k].solution_value*Demand*RateDic[k]))
        A.update({k:round(a[k].solution_value*Demand*RateDic[k])})
        Z.update({k:round(z[k].solution_value)})
        #print(k, ":" , round(z[k].solution_value))
        E.update({k:round(e[k].solution_value)})
        print(k, ":" , round(ss[k].solution_value*RateDic[k]*Demand))
        S.update({k:round(ss[k].solution_value*RateDic[k]*Demand)})
    return X,Y,A,E,Z,S
    





file_location = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/InputDataOp.xlsx'
#first for Parts information
Data=pd.read_excel(file_location, sheet_name='Data1')


# read out put of Simulation ;
    
VIO=VisualNetwork_input_output(Optimization(Data)[0],Optimization(Data)[1],Optimization(Data)[2],Optimization(Data)[3],Optimization(Data)[4],Optimization(Data)[5])#input network info node, edge and their attributes
Nodes= VIO.UNodeslist.set_index("ID", drop = False) 
Nodes.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/Node1.csv', index=False)
# for disruption setting in scenario firs element frequancy l=low,h=high;second element severity s=sever,m=moderate;third element duration sh=short,ln=long
Scenariogeneration.Start(Itr =10 , initialization = 90 , Nevent = 1, risk_degree =['hr'], disruption_setiitng=['l','s','sh'], Disruption_Type=0, Tier = 1, disruption_component =[1,0])
# SimulationOut=pd.read_excel('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/Statistical/Stat.xlsx')
# RSl= SimulationOut['Final_Node'].quantile(0.85)
    
        




