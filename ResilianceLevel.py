# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 06:49:38 2019

@author: elham
"""

import pandas as pd
import operator 
from CreateNetwork import VisualNetwork_input_output
from NetworkSimulation import genrate_network 
import MRP_Invent
import numpy as np 



class Resiliance:
    def __init__(self, Period = None, NodeDis = [], EdgeDis = [], Frq= None ,Svr= None,DUR= [],Type= None, LTCH= None, SCName = None):
        self.Period = Period #timePeriod (days)
        self.Edgdis = EdgeDis#list of edge disrupted for current event
        self.Nodedis= NodeDis #list of node disrupted for current event 
        self.durcurrentDis = DUR #as input for disruption setting short or long 
        self.type=0
        self.svr=Svr
        self.frq=Frq
        self.LTCH = LTCH #LT will be changed when we have disruption 
        self.SCName=SCName
        self.period_lst = np.arange(Period+1)
        #writer = pd.ExcelWriter("C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/Output.xlsx") #address to save output 
        #VIO=VisualNetwork_input_output()#input network info node, edge and their attributes
        #Node_list= VIO.UNodeslist.set_index("ID", drop = False) #save node info with related attributes
        # header = ['Node','Demand' , 'FirstInv', 'EndInv', 'SS','Netrq', 'Requested', 'Shipped', 'Recieved', 'Lostdemand', 'Backordered', 'INCost', 'ORDCost', 'BCKCost'] # header of columns
        # for i in range(0,len(Node_list)):
        #     self.INVL = pd.DataFrame(index = self.period_lst, columns = header).fillna(0) #create a empty datafram to save output
        #     self.INVL.to_excel(writer, "{}".format(Node_list['ID'][i]))
        # writer.save()
    
    def SimResiliance (self,INTF,number,ii):
        VIO=VisualNetwork_input_output()#input network info node, edge and their attributes
        Node_DATA = VIO.UNodeslist.set_index("ID", drop = False) #save node info with related attributes
        Edge_DATA = VIO.UEdgeslist #save edge info with related attribute
        writer = pd.ExcelWriter("C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/INV2.xlsx") #address to save output 
        
        def Simulation(row):#starts simulation for each row in edge list
            R1 =row['R']#save R parameter for current row
            ShipFre = row['ShipFreq']#Shippment Frquency for each link/or transporation 
            ShipCap = row ['TShCap']
            LT1=row['LT'] #save Lead Time  parameter for current row
            Tnode1=row['Target ID'] #save target node  parameter for current row
            Snode1 = row['Source ID']#save source node  parameter for current row
            NodeType = Node_DATA.loc[Tnode1,'Type'] #save target node  type parameter for current row
            # these are updated capacity for primary, secondary and backup suppliers 
            PCapacity = Node_DATA.loc[Snode1 ,'CapacityR'] 
            SCapacity =Node_DATA.loc[Snode1 ,'CapacitySc']
            BCapacity =Node_DATA.loc[Snode1 ,'CapacityBck']
            SActive =Node_DATA.loc[Snode1 ,'SC_YesNo']
            BActive =Node_DATA.loc[Snode1 ,'BC_YesNo']
            #we need add delay time for backup suppliers activation 
            DelayActivation =Node_DATA.loc[Snode1 ,'LagtimeB']
            USG1 = row['Usage'] #save usage for part from source node  type parameter for current row
            Snode1 = row['Source ID']#save source node  parameter for current row
            inventory_int1 = int(np.random.normal(400,11))
            #inventory_int1=Node_DATA.loc[Snode1,'Int'] #intial Inventory for specific part
            durnode=Node_DATA.loc[Snode1,'Duration'] #for normal events by looking at node location 
            FRnode=Node_DATA.loc[Snode1,'Frequency'] #normal event  based on node risk index
            SVRnode=Node_DATA.loc[Snode1,'Severity'] #normal event based on node risk index
            duruns=0
            changeLT = 0
            iniperiod=INTF
            nn=number
            #urunt=0
            SVR=0
            SS1 =row ['SS'] #Safty Stock
            C2=genrate_network(VIO.UNodeslist,Edge_DATA ,VIO.OutSave)#generate network for refering the connection between nodes
            C2.smvsnetwork()
            #supplierlist=list(C2.network.successors(Snode1))#find suppliers for Current node
            
            if self.type == 0:
                SVR=SVRnode
                duruns=durnode
                frq=FRnode
            else:
                if len(self.Nodedis) > 0 :#menas if we have any disruption 
                    nodedis_set = set(self.Nodedis)# change list to set for efficient way
                    if Snode1 in nodedis_set: #if disruption happen in node
                        duruns= self.durcurrentDis[Snode1] #update duartion 
                        #FER.append(np.round((1/Node_DATA.loc[Snode1,'Frequency']),0)) #update frequency 
                        #SEVR.append(Node_DATA.loc[Snode1,'Severity']) #update Severity  
                        SVR=self.svr
                        frq=self.frq
                        
                elif len(self.Edgdis) > 0 :
                     edgedis_set = set(self.Edgdis) # change list to set for efficient way
                     if Snode1 in edgedis_set:  #if disruption happen in edge
                         changeLT = self.LTCH [Snode1] # change LT related to edges
                         duruns= self.durcurrentDis # for how many duration it will work for delay in leadtime
                         print("node" + str(Snode1) + "LTisequal"+ str(LT1) + str('added')+ str(changeLT))
            #print("now updated:+++++++" + str(frq*100) + "dur" +str(duruns) + str(SVR))
            C2=MRP_Invent.TrackingUpdate(self.Period)#Start simulation inventory tracking 
            df=C2.Simulation_Inv(iniperiod,nn,self.Period,100,50,30,R1,LT1,changeLT,Tnode1,NodeType,USG1,Snode1,inventory_int1,SS1,int(duruns),SVR,frq*100,ShipFre,ShipCap,PCapacity,SCapacity,BCapacity,SActive,BActive,DelayActivation)
            df.to_excel(writer, "{}".format(Snode1 + " " + "to" + " " + Tnode1))
            
        Edge_DATA.apply(lambda row: Simulation (row),axis=1)# for each connection inventory tracking will start
        writer.save()
        
        #following part lines 92 - 100 save results in a excel sheet
        sheets_dict = pd.read_excel('C:/Users/elham/Google Drive/ReSearch/Regression and relationship/NewupdateRisk/INV2.xlsx', sheet_name=None)

        for key in sheets_dict:
            AllNodes = pd.concat(sheets_dict.values())
            
            

        AllNodes.rename(columns={'Unnamed: 0':'period'}, inplace=True)
        AllNodes.to_excel("AllCNodes_Edges.xlsx", index=False)
        # following part obtain reports and resiiance level
        #first start with defined parameters
        C1=genrate_network(VIO.UNodeslist,Edge_DATA ,VIO.OutSave)
        C1.smvsnetwork()
        Demand=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv')
        Resiliance_Level = {}
        CostB= {}
        CostInv ={}
        CostOrd = {}
        SL={}
        Demand.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/input/{}.csv'.format("Demand" + str(ii)), index=False)#save demand
        AllNodes.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/input/{}.csv'.format("All" + str(ii)), index=False)#save demand

        
        # following for each node in network based on the connection start to obtain resiliance and related reports
        #first start with tier n
        for y,d in C1.network.nodes(data=True):#look at each node and each connection to measure resiliance
            ServiceLevel = []
            #ggrigate_ServiceL=[]
            TotalD= []
            UNSAT = []
            Sucessor_Company_List = list(C1.network.successors(y))#for current node find sucessor company or nodes
            Pre_Company_list=list(C1.network.predecessors(y))#for current node find predecessor company and node
            if len(Pre_Company_list)== 0:#filter last tier of network
                for su in Sucessor_Company_List:#for each period period check level of inventory and backlog 
                    FilterST= AllNodes.loc[operator.and_(AllNodes['Source']==y,AllNodes['Target']==su)] #filter for specific node and period
                    for t in range(self.Period +1):
                        FilterSEC= FilterST.loc[FilterST['period']==t]
                        UNSAT.append(FilterSEC.iloc[0]['UnsatisfiedD'])
                        TotalD.append(FilterSEC.iloc[0]['DT'])
                    Upper=sum(UNSAT)
                    Lower=sum (TotalD)
                    ServiceLevel.append((1-(Upper/Lower))*100)
                
                RSL=sum(ServiceLevel) / len(ServiceLevel)
                Resiliance_Level[y]=round(RSL,2)
            else:# now it looks at other tiers with different connections 
                USAT2=[]
                for i in range(self.Period+1):
                    FilterP= AllNodes.loc[operator.and_(AllNodes['Target']==y,AllNodes['period']==i)]
                    USAT2.append(FilterP['UnsatisfiedD'].max())
                    if i < self.Period:
                        TotalD.append (Demand[y][i])
                RSL=(1-(sum(USAT2)/sum(TotalD)))*100
                Resiliance_Level[y]=round(RSL,2)
                SL[y]=ServiceLevel
                FilterC= AllNodes.loc[AllNodes['Target']==y]
                CostB[y] = FilterC['backlogscost'].sum()
                CostInv[y] = FilterC['INCOST'].sum()
                CostOrd[y] = FilterC['Ordcost'].sum()
        
        REPORT = pd.DataFrame(list(CostB.items()),columns=['Name', 'BackCost'])
        REPORT1 = pd.DataFrame(list(CostInv.items()),columns=['Name', 'InvCost'])
        REPORT2 = pd.DataFrame(list(CostOrd.items()),columns=['Name', 'OrderCost'])
        REPORT['INVcost']= REPORT1['InvCost']
        REPORT['Ordercost']= REPORT2['OrderCost']
        REPORT.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/input/output/{}.csv'.format("Cost"), index=False)#save demand 
           #followinh just print and plot results         
        print("Total backlogscost Cost for nodes" + " " + "is" + ":" + str(CostB))
        print("Total Inventory Cost for nodes" + " " + "is" + ":" + str(CostInv))
        print("Total Order Cost for nodes" + " " + "is" + ":" + str(CostOrd))
        #print(Resiliance_Level)
        
        return Resiliance_Level
 


