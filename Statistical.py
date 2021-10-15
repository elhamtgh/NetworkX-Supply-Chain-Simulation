# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 07:14:57 2021

@author: elham
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_location = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/Output/SC01/Output.xlsx'
#linear Plot SL
# SLS=pd.read_excel(file_location, sheet_name='Inventory')
# SLS0=SLS[['HVAC Module', 'Cockpit']]
# SLS1=SLS[['Ambient Sensor', 'A/C lines']]
# SLS2=SLS[['A/C Ducts', 'Heater Hoses', 'Engine']]
# sns.lineplot(data=SLS2)

######################################################Delay

Delay=pd.read_excel(file_location, sheet_name='Delay')
# # Shortage = pd.read_excel(file_location, sheet_name='STAT')
# # print(Delay.describe())
# # Delay.describe().to_csv("my_descriptionDelay.csv")
# # Shortage.describe().to_csv("my_descriptionShortage.csv")
# # print(Shortage.describe())
# # List of Suppliers to plot
Suppliers = ['S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17']
Parts =['Enginel','HVAC Module', 'Collins and Aikman','A/C lines','A/C Ducts','Heater Hoses','Ambient Sensor','Final Productl']

# Iterate through the Suppliers
for Supplier in Suppliers:   
    # Draw the density plot
    sns.distplot(Delay[Supplier], hist = False, kde = True,
                kde_kws = {'linewidth': 3},
                label = Supplier)
    
# Plot formatting
plt.legend(prop={'size': 16}, title = 'Suppliers')
plt.title('Delay Delivery (Days) for each suppliers')
plt.xlabel('Delay (Day)')
plt.ylabel('Density')


# Density Plot Service level
# sns.distplot(Shortage['ServiceLevel'], hist = False, kde = True,
#                   kde_kws = {'linewidth': 3})
# # Plot formatting
# plt.title('Service Level Focal Firm')
# plt.xlabel('Service Level')
# plt.ylabel('Density')

# # Iterate through the Suppliers
# for Part in Parts:   
#     # Draw the density plot
#     sns.distplot(Shortage [Part], hist = False, kde = True,
#                 kde_kws = {'linewidth': 3},
#                 label = Part)
    
# # Plot formatting
# plt.legend(prop={'size': 16}, title = 'Part')
# plt.title('Lost Demands for parts and final product')
# plt.xlabel('Lost demand (Unit)')
# plt.ylabel('Density')




