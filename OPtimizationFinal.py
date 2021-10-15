# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:06:00 2021

@author: elham
"""


#Optmization model for resilience management 
import pandas as pd
import DemandLT as D
import numpy as np
# first import the Model class from docplex.mp
from docplex.mp.model import Model


#input the data elements that do not change with scenarios 
file_location = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/InputDataOp.xlsx'
#first for Parts information
Data1=pd.read_excel(file_location, sheet_name='Data1')
Parts=Data1["Parts Name"].values #set Part
UsageRate = Data1["Usage_R"].values# Usage Rate for each part
HoldingCost = Data1["Cost"].values # inventory holding cost for each part
PercentageS = Data1["Secondary"].values # Percentage increase in unit cost of reserving capacity for partkfrom secondary supplier
PercentageB = Data1["Backup"].values # Percentage increase in unit cost of reserving capacity for partkfrom back up 
RateDic = dict(zip(Parts, UsageRate))# Usage Rate for each part
HoldCostDic = dict(zip(Parts, HoldingCost))# inventory holding cost for each part
PercentageSC = dict(zip(Parts, PercentageS))# reserving capacity cost for secondary supplier
PercentageBC = dict(zip(Parts, PercentageB))# reserving capacity cost for backup supplier

#supplier Data
Data2=pd.read_excel(file_location, sheet_name='Data2')
Supplier=Data2["Supplier"].values #set Suppliers
#SecondarySCost=Data2["Capacity_Surplus_Cost"].values
#Secondarycost = dict(zip(Supplier, SecondarySCost))
#combination of supplier and parts 
#production = [(i,k) for i in Supplier for k in Parts]
production = [(k) for k in Parts]
Data3=pd.read_excel(file_location, sheet_name='Data3')
FixedCostB=Data3["FixedCostBackUp"].values#fixed cost for choosing the back up supplier when disruption happen 
FixedCostS=Data3["FixedCostSecondary"].values#fixed cost for choosing the Secondary supplier when disruption happen 
RegularCapacity = Data3["PerUnitSurplusCapacity"].values#cost using surplus capacity 
#SecondaryCapacity = Data3["PerUnitsecondaryCapacity"].values#cost using secondary capacity
#BackUpCapacityC=Data3["PerUnitbackupCapacity"].values#reserved BackUp capacity at supplier location 
#UnitPrice=Data3["UnitPrice1"].values #Unit price of ordering from regular capacity 
#Binary = Data3["Binary"].values
CapacityREG = Data3["Capacity"].values#Capacity primary supplier
CapacitySeco= Data3["SecondaryCapacity"].values#Capacity backup capacity
CapacityBack= Data3["BackUpCapacity"].values#Capacity backup capacity
#MinOrder = Data3["MinOrder"].values#Minordering

FixedCost1 = dict(zip(production, FixedCostS))
FixedCost2 = dict(zip(production, FixedCostB))
RegularCapacityCost = dict(zip(production, RegularCapacity))
#SecondaryCapacity1 = dict(zip(production, SecondaryCapacity))
#BackUpCapacityC1 = dict(zip(production, BackUpCapacityC))
#price_regular = dict(zip(production, UnitPrice))
#price_backup = dict(zip(production, UnitPrice1))
BinaryP = dict(zip(production, Binary))
CapacityREG1 = dict(zip(production, CapacityREG))
CapacitySEC1 = dict(zip(production, CapacitySeco))
CapacityBack1 = dict(zip(production, CapacityBack))
#MinOrder1 = dict(zip(production, MinOrder))

#add Capacity Indexes 
#Data4=pd.read_excel(file_location, sheet_name='Data4')
#CapacityLevel1= Data1["Capacity_Level"].values 
#FixedCost= Data4["FixedCost"].values
#limitedcapacity = Data4["Capacity"].values
#CapcityID= [(i,k,j) for i in Supplier for k in Parts for j in CapacityLevel1 ]
#FixedCostLevel = dict(zip(CapcityID, FixedCost))
#CapacityLevel = dict(zip(CapcityID, limitedcapacity))

#Demand
Demand = int(np.random.normal(D.AVEGDEMAND,D.Stv_Demand))

# create one model instance, with a name
m = Model(name='Resilience Opmizimization')

##########time for decision Variables 
#reserved capacity of partk primary supplier
x = {(k) : m.continuous_var(name='x_{0}'.format(k), lb=0, ub=1) for k in Parts}
#Equal 1, if the secondary supplieriis selected
e ={(k) : m.binary_var(name='e_{0}'.format(k)) for k in Parts}
#Resereved capacity of partk secondary supplier
y ={(k) : m.continuous_var(name='y_{0}'.format(k), lb=0, ub=1) for k in Parts}
#Equal 1, if the backup supplieriis selected
z ={(k) : m.binary_var(name='z_{0}'.format(k)) for k in Parts}
#Resereved capacity of partk backup supplier
a ={(k) : m.continuous_var(name='a_{0}'.format(k), lb=0, ub=1) for k in Parts}

#Inventory level of partkat focal firm
#I = {k: m.integer_var(name='I_{0}'.format(k)) for k in Parts}
#Emergency inventory of partkpre-positioned at supplieri
#a = {(i,k): m.continuous_var(name='a_{0}_{1}'.format(i,k)) for i in Supplier for k in Parts}
#Amount of partshipment from primary supplierito focal firm
#v = {(i,k): m.integer_var(name='v_{0}_{1}'.format(i,k)) for i in Suppliers for k in Parts if (i,k) in UNITPrice}
#v = {(i,k): m.integer_var(name='v_{0}_{1}'.format(i,k)) for i in Supplier for k in Parts}
#Emergency inventory of partkpre-positioned at supplieri, in fraction of supplier capacity
#e = {(i,k): m.continuous_var(name='e_{0}_{1}'.format(i,k), lb=0, ub=1) for i in Supplier for k in Parts}

###Constaraints 
#percentage of capacity on supplier nad secondary dual sourcing  
for k in Parts:
        m.add_constraint(x[k]+y[k]== BinaryP [k])
#selecting backup supplier 
for k in Parts:
    for i in Supplier:
        m.add_constraint(z[i,k] - BinaryP [i,k] <= 0)
#capacity limitation for promary and backup supplier 
for k in Parts:
    for i in Supplier:
        m.add_constraint(e[i,k]*RateDic[k]*Demand - z[i,k]*CapacityBack1[i,k] <= 0 )
for k in Parts:
    for i in Supplier:
        m.add_constraint(x[i,k]*RateDic[k]*Demand - CapacityREG1[i,k] <= 0 )
#min ordering
for k in Parts:
    for i in Supplier:
        m.add_constraint(v[i,k] - BinaryP [i,k]*MinOrder1[i,k] >= 0 )   
for k in Parts:
    for i in Supplier:
        m.add_constraint(a[i,k] - BinaryP [i,k]*MinOrder1[i,k]*z[i,k] >= 0 )     
#production constraints 
for k in Parts:
    m.add_constraint(m.sum(BinaryP[i,k]*(v[i,k]+ a[i,k]) for i in Supplier) -I[k] >= RateDic[k]*Demand) 

#objective value 
objective= m.sum(x[i,k]*RegularCapacity1[i,k]+y[i,k]*SecondaryCapacity1[i,k]+ e[i,k]*BackUpCapacityC1[i,k]for i in Supplier for k in Parts) + m.sum(z[i,k]*FixedCost1[i,k] for i in Supplier for k in Parts) + m.sum(HoldCostDic[k]*I[k] for k in Parts)+ m.sum(v[i,k]*price_regular[i,k] + a[i,k]*price_backup[i,k] for i in Supplier for k in Parts)
m.minimize(objective)
m.solve()
m.print_information()
m.print_solution()


        

        






