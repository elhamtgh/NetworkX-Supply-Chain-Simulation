# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:43:48 2021

@author: elham
"""
import dexpy.optimal
from dexpy.model import ModelOrder
import pandas as pd
import scipy.stats as st

SAVE='C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/RGResults/RegressionInputDOE3.xlsx'
writer = pd.ExcelWriter(SAVE,engine='xlsxwriter') #address to save output
INPUT = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/InputDataOp.xlsx'
#first for Parts information
Capacity=pd.read_excel(INPUT, sheet_name='Data1')
Demand = pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv')
SL=0.95
Z = st.norm.ppf(1-(1-SL)/2)
for i in range(1,8):
    reaction_design = dexpy.optimal.build_optimal(5, order=ModelOrder.linear)
    column_names = ['X', 'Y','Z','ss','RMI_inventory(S)']
    FilterCapacity= Capacity.loc[Capacity['ID']==i]
    #FilterDemand= Demand.loc[Capacity['ID']==i]
    actual_lows = { 'X': 0, 'Y': 0,'Z': 0,'ss': 0, 'RMI_inventory(S)': 0 }
    actual_highs = { 'X': FilterCapacity.iloc[0]['Demand']*0.6*Z, 'Y':FilterCapacity.iloc[0]['Demand']*0.3*Z,'Z': FilterCapacity.iloc[0]['Demand']*0.2*Z,'ss': FilterCapacity.iloc[0]['Demand'], 'RMI_inventory(S)': 300 }
    reaction_design.columns = column_names
    Final=dexpy.design.coded_to_actual(reaction_design, actual_lows, actual_highs)
    #Final['RSL'] = 0
    Final.to_excel(writer, sheet_name=str(i)) 
writer.save()