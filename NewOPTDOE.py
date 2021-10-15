# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 17:20:33 2021

@author: elham
"""
import dexpy.optimal
from dexpy.model import ModelOrder
import pandas as pd
import scipy.stats as st
import math
import numpy as np



SAVE='C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/RGResults/RegressionInputDOE4.xlsx'
writer = pd.ExcelWriter(SAVE,engine='xlsxwriter') #address to save output
INPUT = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/InputDataOp.xlsx'
Capacity=pd.read_excel(INPUT, sheet_name='Data1')
#print(Capacity)
SL=0.85
Z = st.norm.ppf(1-(1-SL)/2)
for i in range(1,8):
    
    reaction_design = dexpy.optimal.build_optimal(5, order=ModelOrder.linear)
    column_names = ['X', 'Y','Z','ss','RMI_inventory(S)']
    FilterCapacity= Capacity.loc[Capacity['ID']==i]
    actual_lows = { 'X': FilterCapacity.iloc[0]['Demand']*0.8, 'Y': FilterCapacity.iloc[0]['Demand']*0.3 , 'Z': 0, 'ss': 0,'RMI_inventory(S)': 0}
    actual_highs = { 'X': FilterCapacity.iloc[0]['Demand']*0.8*Z, 'Y': FilterCapacity.iloc[0]['Demand']*0.3*Z , 'Z': 100, 'ss': FilterCapacity.iloc[0]['Demand']*Z,'RMI_inventory(S)': 200 }
    reaction_design.columns = column_names
    Final = dexpy.design.coded_to_actual(reaction_design, actual_lows, actual_highs)
    for index, row in Final.head().iterrows(): 
        Value= (row['X'] + row ['Y'] - FilterCapacity.iloc[0]['Demand'] )/FilterCapacity.iloc[0]['Demand']
        if Value <= 0.2:
            row['Z'] = 100
            row ['RMI_inventory(S)']= 200*Z
        if 0.2<Value<= 1.2:
            row['Z'] = 0
            row ['RMI_inventory(S)']= 200*Z*0.6
        if Value> 1.2:
            row['Z'] = 0
            row ['RMI_inventory(S)']= 0
    Final = Final.apply(np.ceil)    
    Final.to_excel(writer, sheet_name=str(i)) 
writer.save()


