# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 18:28:43 2019

@author: elham
"""
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


class Tracking:
    def __init__(self, T = None):
        self.period_lst = np.arange(T) # index
        header = ['Source','Target','demand','inv_Level','Order','Lost_Demand','INCOST','OrdCost'] # columns
        self.STS = pd.DataFrame(index = self.period_lst, columns = header).fillna(0)
        self.writer = pd.ExcelWriter("C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/INV.xlsx")
        
        
    def SimulationInv(self,T,invcost,ordcost,lostcost,R,LT,Tnode,USG,Snode,inventory_int,SS):
        D=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv')
        
        
        
    
        # Fill DataFrame
        for j in range (T):
            self.STS['demand'][j] =D[Tnode][j]*USG
            self.STS['Source'][j] = Snode
            self.STS['Target'][j] = Tnode
            
        
        
        for period in self.period_lst:
            OrderTarget=0
            if period == 0:
                if self.STS['demand'][period] < inventory_int:
                    self.STS['inv_Level'][period] = inventory_int - self.STS['demand'][period]
                    self.STS['INCOST'][period] = self.STS['inv_Level'][period]*invcost
                else:     
                    self.STS['inv_Level'][period] = 0
                    
            if period > 0 and int(period) < T:
                if self.STS['demand'][period] < self.STS['inv_Level'][period-1]:
                    self.STS['inv_Level'][period] = self.STS['inv_Level'][period-1] - self.STS['demand'][period]
                    self.STS['INCOST'][period] = self.STS['inv_Level'][period]*invcost
                else:
                    self.STS['Lost_Demand'][period]= abs(self.STS['inv_Level'][period-1] - self.STS['demand'][period])
                    
                        
                    #STS['inv_Level'][period] = 0
                        
                if period  % R == 0 :
                    
                    for i in range(R):
                        OrderTarget = OrderTarget + self.STS['demand'][period+i]
                    
                    if self.STS['inv_Level'][period] <= SS:
                             self.STS['Order'][period] = OrderTarget - self.STS['inv_Level'][period]
                             self.STS['OrdCost'][period] = ordcost*self.STS['Order'][period]
                            
                             t=int(period + LT)
                             if t < T :
                                 self.STS['inv_Level'][t] = self.STS['inv_Level'][t-1] + self.STS['Order'][period]
                             
                              
        plt.figure()
        plt.step(self.period_lst,self.STS['inv_Level'][0:T], where = 'post')
        plt.title('Inventory Process from' + " " +  Snode + "" + 'to'+"" + Tnode)
        plt.savefig( "C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/{}.png".format(str(Snode + Tnode)), format = "png", dpi = 300)
        return self.STS
      
