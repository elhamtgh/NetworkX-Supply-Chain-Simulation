# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 06:27:44 2020

@author: elham
"""
#this modul generate all ghraph from my output results 
#we have two excel files for tracking inventory and all agrigate in each simulation 

import pandas as pd
from CreateNetwork import VisualNetwork_input_output
from NetworkSimulation import genrate_network
import numpy as np
import matplotlib.pyplot as plt
import operator 
import plotly
import plotly.graph_objs as go



class Dashboard_Output:
    def __init__(self, Period = None ,NodeDis = [], EdgeDis = []):
        self.Period = Period #timePeriod (days)
        self.Edgdis = EdgeDis #list of edge disrupted for current event
        self.Nodedis= NodeDis #list of node disrupted for current event
        
    def Plot_Visulaziatio (self):
        VIO=VisualNetwork_input_output()#input network info node, edge and their attributes
        All=pd.read_excel('C:/Users/elham/.spyder-py3/AllCNodes_Edges.xlsx')
        All.rename(columns={'Unnamed: 0':'period'}, inplace=True)
        #print(All)
        Edge_DATA = VIO.UEdgeslist #save edge info with related attribute
        C1=genrate_network(VIO.UNodeslist,Edge_DATA ,VIO.OutSave)
        C1.smvsnetwork()
        Resiliance_Level = {}
        BackorderT={}
        SL={}
        
        # following for each node in network based on the connection start to obtain resiliance and related reports
        #first start with tier n
        for y,d in C1.network.nodes(data=True):
            i=0
            ServiceLevel = []
            Aggrigate_ServiceL=[]
            Backorder=[]
            Sucessor_Company_List = list(C1.network.successors(y))
            Pre_Company_list=list(C1.network.predecessors(y))
            if len(Pre_Company_list)== 0:
                for i in range(self.Period+1): 
                    FilterST= All.loc[operator.and_(All['Source']==y,All['period']==i)]
                    for su in Sucessor_Company_List:
                        FilterFST = FilterST.loc[FilterST['Target']==su]
                        if FilterFST.iloc[0]['DT'] > 0:
                            ServiceLevel.append((1-(FilterFST.iloc[0]['UnsatisfiedD']/FilterFST.iloc[0]['DT']))*100)
                            Backorder.append(FilterFST.iloc[0]['backlogs'])
                        else:
                            ServiceLevel.append(100)
                            Backorder.append(FilterFST.iloc[0]['backlogs'])
                    Aggrigate_ServiceL.append(sum(ServiceLevel) / len(ServiceLevel))
                RSL=sum(Aggrigate_ServiceL) / len(Aggrigate_ServiceL)
                Resiliance_Level[y]=round(RSL,2)
            else:# now it looks at other tiers with different connections 
                #Second_count=0
                
                for i in range(self.Period+1):
                    FilterP= All.loc[operator.and_(All['Target']==y,All['period']==i)]
                    Backorder.append(FilterP['backlogs'].max())
                    for sc in Pre_Company_list:
                        FilterF = FilterP.loc[FilterP['Source']==sc]
                        if FilterF.iloc[0]['DT'] > 0:
                            ServiceLevel.append((1-(FilterF.iloc[0]['UnsatisfiedD']/FilterF.iloc[0]['DT']))*100)
                            
                        else:
                            ServiceLevel.append(100)
                            
                    Aggrigate_ServiceL.append(sum(ServiceLevel) / len(ServiceLevel))
                    
                RSL=sum(Aggrigate_ServiceL) / len(Aggrigate_ServiceL)
                Resiliance_Level[y]=round(RSL,2)
                BackorderT[y] = Backorder
                SL[y]=Aggrigate_ServiceL
                
                
       
              

               
        periodlst = np.arange(self.Period)       
        for k in BackorderT:
            d=list(BackorderT[k])
            plt.figure()#plot inventory level for current connection
            plt.step(periodlst,d[0:365], where = 'post')
            plt.title('BackOrder for' + " " +  str(k) )
            plt.savefig( "C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/Plots/{}.png".format("BackOrderF"+ str(k)), format = "png", dpi = 300)
            plt.cla()
            #plt.show()
        for s in SL:
            d=list(SL[s])
            plt.figure()#plot inventory level for current connection
            plt.step(periodlst,d[0:365], where = 'post')
            plt.title('Service Level for ' + " " +  str(s) )
            plt.savefig( "C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/Plots/{}.png".format("Servicel LevelF"+ str(s)), format = "png", dpi = 300)
            plt.cla()
            #plt.close()

        #print(Resiliance_Level)
        return Resiliance_Level
    
    def Inventory_Plot(self):
        periodlst = np.arange(self.Period)
        DI=self.Period
        sheets_dict = pd.read_excel('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/INV2.xlsx', sheet_name=None)
        
        for key in sheets_dict:
            print(key)
            df=sheets_dict[key]
            plt.figure()#plot inventory level for current connection
            plt.step(periodlst,df['EndinvAA'][0:DI], where = 'post')
            plt.title('Inventory Process from' + " " +  key)
            plt.savefig( "C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/Plots/{}.png".format(str(key)), format = "png", dpi = 300)
            plt.cla()
        

class Plot_Results:
    def __init__(self):
     self.file_location_Results = 'C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/OutputMarch14/FinalReport.xlsx'
     self.R=pd.read_excel(self.file_location_Results, sheet_name='Plot1')
    def plot_multi(self):
        #Set marker properties
        markersize = self.R['R']*0.7
        markercolor = self.R['Type']
        markershape = self.R['Scenario']
        #Make Plotly figure
        fig1 = go.Scatter(x=self.R['InvCost(10e8)'],y=self.R['DL'],text=self.R['Node'],textposition="top center",marker=dict(size=markersize,
                                color=markercolor,
                                symbol=markershape,
                                opacity=1.0,
                                reversescale=True,
                                colorscale='tealrose'),
                                line=dict (width=0.02),
                                mode='markers')

        #Make Plot.ly Layout
        mylayout = go.Layout(xaxis=dict( title="InvCost(10e8)"),yaxis=dict( title="DL"))

        #Plot and save html
        plotly.offline.plot({"data": [fig1],"layout": mylayout},auto_open=True,
                     filename=("Scenario4.html"))
        
    def plot(self):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
                x=self.R['InvCost(10e8)0'],
                y=self.R['R0'],
                name="Scenario _ 0"       # this sets its legend entry
                    ))


        fig.add_trace(go.Scatter(
                x=self.R['InvCost(10e8)1'],
                y=self.R['R1'],
                name="Scenario _ 1" 
                    ))
        
        fig.add_trace(go.Scatter(
               x=self.R['InvCost(10e8)2'],
                y=self.R['R0'],
                name="Scenario _ 2" 
                    ))
        fig.update_layout(
                title="Resiliance_Inventory Cost",
                xaxis_title="Resiliance",
                yaxis_title="Inventory Cost",
                font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                        )
                )
        fig.show()
        fig.write_image('deeptier2.png')



M=Dashboard_Output(365,[],[])
M.Inventory_Plot()
M.Plot_Visulaziatio()
#N=Plot_Results()
#N.plot_multi()



