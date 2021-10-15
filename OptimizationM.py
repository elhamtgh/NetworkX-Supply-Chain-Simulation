# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 15:10:14 2020

@author: elham
"""

#Optmization model for resilience management 
import sys
import docplex.mp
import pandas as pd
import DemandLT as D
import numpy as np
# first import the Model class from docplex.mp
from docplex.mp.model import Model

#input data and parameters 
file_location = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/InputDataOp.xlsx'
FixedcostSC1=pd.read_excel(file_location, sheet_name='FixedCostSec')
Holding_cost1=pd.read_excel(file_location, sheet_name='HoldingCost')
CostIK= pd.read_excel(file_location, sheet_name='Ik')
Capacity=pd.read_excel(file_location, sheet_name='Sets')


#FixedCost to select the secondary suppliers
FixedcostSC=dict(FixedcostSC1.values.tolist())
#Raw material holding cost at firm location 
Holding_cost= Holding_cost1.set_index('Part').T.to_dict('records')[0]
#Usage Rate for each raw material 
Usagerate=Holding_cost1.set_index('Part').T.to_dict('records')[1]
#EmergencyCost
EmPrice=CostIK.set_index('Key').T.to_dict('records')[0]
print(EmPrice)

#Sets
Suppliers = range(1, 15)# {1..14}
primaryS= range(1, 8)# {1..8}
secondS = range(8, 15)# {8..15}
Parts = range(101, 108)# {101 .. 108}
Capacity_Level = range (11,18)# {0.1 .. 0.7}


#Parameters
Demand = int(np.random.normal(D.AVEGDEMAND,D.Stv_Demand))
#Holding_cost = {6:9020, 7:9044, 8:9051}
#Usagerate = {6:0.3, 7:0.45, 8:0.51}
EmPrice1 = {(1,6): 10, (1,7):37, (1,8):45, (2,6): 21, (2,7):46, (2,8):52, (3,6): 14, (3,7):38, (3,8):44,(4,6): 16, (4,7):42, (4,8):61}
UNITPrice = {(1,6): 5, (1,7):7, (1,8):9, (2,6): 11, (2,7):16, (2,8):12, (3,6): 8, (3,7):7, (3,8):9,(4,6): 17, (4,7):12, (4,8):11}
Fixedcostcapacity = {(1,6,9): 120, (1,6,10): 210, (1,6,11): 340, (1,7,9): 118, (1,7,10): 215, (1,7,11): 303, (1,8,9): 119, (1,8,10): 202, (1,8,11): 278,
                     (2,6,9): 1830, (2,6,10): 1243, (2,6,11): 833, (2,7,9): 108, (2,7,10): 205, (2,7,11): 313, (2,8,9): 109, (2,8,10): 145, (2,8,11): 208,
                     (3,6,9): 128, (3,6,10): 223, (3,6,11): 301, (3,7,9): 98, (3,7,10): 195, (3,7,11): 308, (3,8,9): 121, (3,8,10): 176, (3,8,11): 138,
                     (4,6,9): 126, (4,6,10): 999, (4,6,11): 298, (4,7,9): 121, (4,7,10): 145, (4,7,11): 321, (4,8,9): 108, (4,8,10): 219, (4,8,11): 218}
Supplycapacity = {(1,6,9): 210, (1,6,10): 311, (1,6,11): 340, (1,7,9): 218, (1,7,10): 315, (1,7,11): 303, (1,8,9): 219, (1,8,10): 202, (1,8,11): 178,
                  (2,6,9): 2, (2,6,10): 343, (2,6,11): 433, (2,7,9): 208, (2,7,10): 205, (2,7,11): 213, (2,8,9): 309, (2,8,10): 245, (2,8,11): 208,
                  (3,6,9): 228, (3,6,10): 323, (3,6,11): 401, (3,7,9): 198, (3,7,10): 295, (3,7,11): 308, (3,8,9): 221, (3,8,10): 276, (3,8,11): 438,
                  (4,6,9): 226, (4,6,10): 309, (4,6,11): 398, (4,7,9): 221, (4,7,10): 245, (4,7,11): 421, (4,8,9): 408, (4,8,10): 119, (4,8,11): 281}
#Fixedcostselect = {3:40, 4:40}
EmCost = {(1,6): 201, (1,7):157, (1,8):235, (2,6): 121, (2,7):146, (2,8):152, (3,6): 214, (3,7):138, (3,8):144,(4,6): 216, (4,7):142, (4,8):161}
providepart = {(1,6): 0, (1,7):0, (1,8):1, (2,6): 0, (2,7):1, (2,8):0, (3,6): 1, (3,7):0, (3,8):1,(4,6): 1, (4,7):0, (4,8):0}

# create one model instance, with a name
m = Model(name='Resilience Opmizimization')

# create flow variables 
#Inventory level of partkat focal firm
I = {k: m.integer_var(name='I_{0}'.format(k)) for k in Parts}
#Emergency inventory of partkpre-positioned at supplieri
a = {(i,k): m.continuous_var(name='a_{0}_{1}'.format(i,k)) for i in Suppliers for k in Parts}
#Amount of partkshipment from primary supplierito focal firm
#v = {(i,k): m.integer_var(name='v_{0}_{1}'.format(i,k)) for i in Suppliers for k in Parts if (i,k) in UNITPrice}
v = {(i,k): m.integer_var(name='v_{0}_{1}'.format(i,k)) for i in Suppliers for k in Parts}
#Equal 1, if level ofjcapacity of partksupplied by supplierireserved at focal firm
x = {(i,k,j) : m.binary_var(name='x_{0}_{1}_{2}'.format(i,k,j)) for i in Suppliers for k in Parts for j in Capacity_Level}
#Equal 1, if the secondary supplieriis selected
y = {(i) : m.binary_var(name='y_{0}'.format(i)) for i in Suppliers if (i) in FixedcostSC}
#Emergency inventory of partkpre-positioned at supplieri, in fraction of supplier capacity
e = {(i,k): m.continuous_var(name='e_{0}_{1}'.format(i,k), lb=0, ub=1) for i in Suppliers for k in Parts}


###Constaraints 
# for selecting primary and secondary suppliers 
for k in Parts:
    for i in primaryS:
        m.add_constraint(m.sum(x[i,k,j] for j in Capacity_Level) == 1)
for k in Parts:
    for i in secondS:
        m.add_constraint(m.sum(x[i,k,j] for j in Capacity_Level) <= 1)
#for selecting the specific secondary supplier 
m.add_constraint(m.sum(y[i] for i in secondS if i in FixedcostSC) <= 1)
#capacity limitation 
for k in Parts:
    for i in Suppliers:
        m.add_constraint(v[i,k] - m.sum(Supplycapacity[i,k,j]*x[i,k,j] for j in Capacity_Level)<=0)
#for emergency assigment 
for k in Parts:
    for i in Suppliers:
        m.add_constraint(e[i,k] - providepart [i,k] <= 0 )
#shipment constraints 
for k in Parts:
    m.add_constraint(m.sum(providepart[i,k]*(v[i,k]+ a[i,k]) for i in Suppliers) -I[k] >= Usagerate[k]*Demand)

#objective value 
m.minimize(m.sum(x[i,k,j]*Fixedcostcapacity[i,k,j] for i in Suppliers for k in Parts for j in Capacity_Level if (i,k,j) in Fixedcostcapacity) + m.sum(y[i]*FixedcostSC[i] for i in secondS if i in FixedcostSC) + m.sum(Holding_cost[k]*I[k] for k in Parts if i in Holding_cost)
+ m.sum(e[i,k]*EmPrice[i,k] for i in Suppliers for k in Parts if (i,k) in EmPrice)+ m.sum(v[i,k]*UNITPrice[i,k] for i in Suppliers for k in Parts if (i,k) in UNITPrice) + m.sum(a[i,k]*EmCost[i,k] for i in Suppliers for k in Parts if (i,k) in EmCost))   
sm=m.solve()
m.print_information()
sm.display()
    

