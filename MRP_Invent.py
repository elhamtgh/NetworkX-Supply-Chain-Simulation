# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 06:55:53 2019

@author: elham
"""
import numpy as np 
import pandas as pd



class TrackingUpdate:
    def __init__(self, T = None):
        self.period_lst = np.arange(T+1) # index for output 
        header = ['Target','Source','DT','RSL','FirstinvAA','EndinvAA','Pcapacity','Scapacity','Bcapacity','OrderTarget(SS)','NetR','orderprocessing','needShip','RecievedOrder','UnsatisfiedD','backlogs','INCOST','Ordcost','backlogscost','MaxDelayLeadtime'] # header of columns
        self.INVL = pd.DataFrame(index = self.period_lst, columns = header).fillna(0) #create a empty datafram to save output
        #self.writer = pd.ExcelWriter("C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/Results/InvProcess/INV2.xlsx") # address save output 
     
        
    def Simulation_Inv(self,Initial,number,T,ordcost,invcost,lostcost,R,LT,changeLT,Tnode,typeTnode,USG,Snode,inventory_int,SS,duruns,SVR,frq,ShipFre,ShipCap,PCapacity,SCapacity,BCapacity,SActive,BActive,DelayActivation):#start simulation for tracking inventory
        D=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv')#read demand which is follow MRP method
        
        Delay_Leadtime = [0]#save any delay delivered backlog order in each period time
        self.INVL.loc[0,'DT'] =0# just first row in our table for showing intial inventory- we do not need demand
        for i in range (T):#update output demand columns  
                self.INVL.loc[i+1,'DT'] =D[Tnode][i]
        self.INVL.loc[:,'Source'] = Snode #fill coulmn Source column in output datafram
        self.INVL.loc[:,'RSL'] = 1 #fill coulmn Source column in output datafram
        self.INVL.loc[:,'Target'] = Tnode #fill coulmn Target column in output datafram
       
        AVGDemand=self.INVL['DT'].mean()#average daily demand to obtain order target 
        Ordertarget = round(AVGDemand*(R) + SS,0) #order target calculate  
        EndDisruption = []#for saving period disruption happen 
        orderpending = []
        StartEvent=[] #when Event or disruption has been start
#        if duruns>0:
#            FR=1
#            SEVV=SVR
#            DURATION=duruns
#        else:
#            FR=FRn
#            SEVV=SVRn
#            DURATION=durn
        for t in range(number):
            StartEvent.append(Initial + 15 + t*round(frq))
            
        EndDisruption = []#for saving period disruption happen 
        for f in StartEvent:
            for d in range(duruns):#save period time we will have disrution based on duration 
                EndDisruption.append(f + d)
        PeriodDis_set = set(EndDisruption)
        #print(PeriodDis_set)
        #print ("Now Severity is " + str(SVR))
            
            
         
        for period in self.period_lst:#now start filling each columns of output dataframe
            OrderTarget=0
            #if period > Initial :
                #if period % FR == 0 : #check if it is time to have disruption for Source node 
            #print("Period list" + str(PeriodDis_set))
            #print("period now" + str(period))
            #print(Snode)

            
            if period == 0: #in time period 0 just we want to show intial inventory 
                self.INVL.loc[period,'FirstinvAA']=inventory_int
                self.INVL.loc[period,'EndinvAA']=inventory_int
                self.INVL.loc[period,'orderprocessing'] = 0
                self.INVL.loc[period,'needShip'] = 0
                self.INVL.loc[period,'Pcapacity'] = PCapacity + SS
                self.INVL.loc[period,'Scapacity'] = SCapacity
                self.INVL.loc[period,'Bcapacity'] = BCapacity
                

            else:
                self.INVL.loc[period,'FirstinvAA']=self.INVL.loc[period-1,'EndinvAA']#in other period first inventory equal end inventory in perviouse period 
               
                if period  % R == 0  :#if time to order 
#                   if self.INVL.loc[period,'FirstinvAA'] <= Reorder_Point:
                     for i in range(R):
                         if int(period+i)<=T:#planning no more than our time period 
                             OrderTarget = Ordertarget + self.INVL.loc[period+i,'DT']
                             #OrderTarget = Ordertarget #order target need to satisfied future period till we recieve inventory and next ordering time
                     self.INVL.loc[period,'OrderTarget(SS)'] = OrderTarget #order level for our inventory policy 
                    
                     if OrderTarget - self.INVL.loc[period,'FirstinvAA'] > 0 and self.INVL.loc[period,'DT'] >0 :#check if have lack of inventory and need order
                        self.INVL.loc[period,'NetR'] = OrderTarget - self.INVL.loc[period,'FirstinvAA'] # we need place order
                     else :
                        self.INVL.loc[period,'NetR'] =0 #otherwise no order
                self.INVL.loc[period,'orderprocessing'] = self.INVL.loc[period-1,'orderprocessing'] - self.INVL.loc[period-1,'needShip'] + self.INVL.loc[period,'NetR'] 
                if period % ShipFre ==0 :
                    if self.INVL.loc[period,'orderprocessing'] > ShipCap:
                        self.INVL.loc[period,'needShip'] = ShipCap
                    else:
                        self.INVL.loc[period,'needShip'] = self.INVL.loc[period,'orderprocessing']  
                     #print("net" + str(self.INVL.loc[period,'NetR']))
                     #print(period)
                    
                     
                if period in PeriodDis_set:
                    #print(period in PeriodDis_set)
                    svr=1-SVR
                    LT = LT + changeLT+BActive*DelayActivation
                    #print("Severity" + str(svr))
                    self.INVL.loc[period+LT,'RecievedOrder'] = np.round(self.INVL.loc[period,'needShip']*svr,0)#after leadtime we recieve the inventory we order
                    #print("Shipped" + str(self.INVL.loc[period+LT,'RecievedOrder']))
                    self.INVL.loc[period,'RSL'] = svr
                    #print("Now must be updated" + str(svr))
                    
                else:
                    svr=1
                    #print("Severity" + str(svr))
                    self.INVL.loc[period+LT,'RecievedOrder'] = np.round(self.INVL.loc[period,'needShip']*svr,0)#after leadtime we recieve the inventory we order
                    #print("Shipped" + str(self.INVL.loc[period+LT,'RecievedOrder']))
                    self.INVL.loc[period,'RSL'] = svr
                
                                      
                self.INVL.loc[period,'EndinvAA']=self.INVL.loc[period,'FirstinvAA'] + self.INVL.loc[period-1,'Pcapacity']+ SActive*self.INVL.loc[period-1,'Scapacity'] + BActive*self.INVL.loc[period-1,'Bcapacity']+  -self.INVL.loc[period,'DT']+ self.INVL.loc[period,'RecievedOrder']#update end inventory
                D.loc[period-1,Snode]+=self.INVL.loc[period,'NetR']*USG#update demand for source node in demand file due to MRP
                self.INVL.loc[period,'backlogs'] = self.INVL.loc[period-1,'UnsatisfiedD']  
                if self.INVL.loc[period,'EndinvAA']<self.INVL.loc[period,'FirstinvAA']:
                    self.INVL.loc[period,'Pcapacity'] = self.INVL.loc[period-1,'EndinvAA']-self.INVL.loc[period-1,'FirstinvAA']
                    if self.INVL.loc[period,'Pcapacity'] <0:
                        self.INVL.loc[period,'Pcapacity']=0
                    else:
                        self.INVL.loc[period,'Pcapacity']=self.INVL.loc[period,'Pcapacity']
                else:
                    self.INVL.loc[period,'Pcapacity']=self.INVL.loc[period-1,'Pcapacity']
                
                if SActive == 1:
                    if self.INVL.loc[period,'EndinvAA']<self.INVL.loc[period,'FirstinvAA'] + self.INVL.loc[period-1,'Pcapacity']:
                        self.INVL.loc[period,'Scapacity'] = self.INVL.loc[period-1,'EndinvAA']-(self.INVL.loc[period-1,'FirstinvAA'] + self.INVL.loc[period-1,'Pcapacity'])
                        if self.INVL.loc[period,'Scapacity'] <0:
                             self.INVL.loc[period,'Scapacity']=0
                        else:
                            self.INVL.loc[period,'Scapacity']=self.INVL.loc[period,'Pcapacity']
                    else:
                        self.INVL.loc[period,'Scapacity']=self.INVL.loc[period-1,'Scapacity']
                
                if BActive == 1:
                    if self.INVL.loc[period,'EndinvAA']<self.INVL.loc[period,'FirstinvAA'] + self.INVL.loc[period-1,'Pcapacity'] +  self.INVL.loc[period-1,'Scapacity']:
                        self.INVL.loc[period,'Bcapacity'] = self.INVL.loc[period-1,'EndinvAA']-(self.INVL.loc[period-1,'FirstinvAA'] + self.INVL.loc[period-1,'Pcapacity'] + self.INVL.loc[period-1,'Scapacity'])
                        if self.INVL.loc[period,'Bcapacity'] <0:
                             self.INVL.loc[period,'Bcapacity']=0
                        else:
                            self.INVL.loc[period,'Bcapacity']=self.INVL.loc[period,'Bcapacity']
                    else:
                        self.INVL.loc[period,'Bcapacity']=self.INVL.loc[period-1,'Bcapacity']
                        
                    
                   
                if self.INVL.loc[period,'EndinvAA']< 0:#just calculate the lost sales
                    self.INVL.loc[period,'UnsatisfiedD'] = abs(self.INVL.loc[period,'EndinvAA'])
                    orderpending.append([period,self.INVL.loc[period,'UnsatisfiedD']])#when we have backlig orders and save them to track them 
                    self.INVL.loc[period,'EndinvAA'] = 0
                else:
                    self.INVL.loc[period,'UnsatisfiedD'] = 0
                    #obtain when backlig order will be stasitfied and find delay delivary
                indexback =[]
                if (len(orderpending)) > 0:
                    for k in range(len(orderpending)):
                        if orderpending[k][0] < period and self.INVL.loc[period,'EndinvAA']> orderpending[k][1]:
                            #print(Snode,Tnode,orderpending)
                            Delay_Leadtime.append(period - orderpending[k][0])
                            self.INVL.loc[period,'EndinvAA'] = self.INVL.loc[period,'EndinvAA'] - orderpending[k][1]
                            indexback.append(k)
                            #print("Delay:" + str(Delay_Leadtime))
                            #del orderpending[0]
                            #print(Snode,Tnode,orderpending)

                self.INVL.loc[0,'MaxDelayLeadtime'] = max(Delay_Leadtime) # find the worse case of delivery  
                if len(indexback)>0:
                    for d in range(len(indexback)):
                        del orderpending[0]
                
                
            #following just update related costs
            self.INVL.loc[period,'Ordcost'] = ordcost*self.INVL.loc[period,'RecievedOrder'] 
            self.INVL.loc[period,'backlogscost'] = self.INVL.loc[period,'backlogs']*lostcost
            self.INVL.loc[period,'INCOST'] = self.INVL.loc[period,'EndinvAA']*invcost 
      
        #print("Delay lead time for Back order from " + " "+ Snode + "  " + 'to'+"  " + Tnode + str(Delay_Leadtime))
        D.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv', index=False)#save demand                    
        return self.INVL
                



     
