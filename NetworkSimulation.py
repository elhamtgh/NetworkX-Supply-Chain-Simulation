# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#this modual is for:
#1.mapping network 
#2. genrate randomn network 
#3. create connection 
#4. measure network metrics 

# import libaries
import networkx as nx
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap as Basemap
import pandas as pd

#from AddRandomnEdge import addRandomnedg as RNDEDG1

class genrate_network:
    def __init__(self, node = None, edge=None, save=None):
        self.node=node
        self.edge=edge
        self.save=save
        self.lat=[]
        self.lon=[]
        self.Firm=[]
        self.size=[]
        self.risk = []
        self.Fr =[]
        self.Sev = []
        self.pos={}
        self.network = nx.DiGraph()
        
    #visualization Network 
    # def network(self):
    #     fig = plt.figure(figsize=(35,21))
    #     m = Basemap(
    #         projection='robin',
    #         lon_0=0,
    #         llcrnrlon=-130,
    #         llcrnrlat=25,
    #         urcrnrlon=-60,
    #         urcrnrlat=50,
    #         lat_ts=0,
    #         resolution='l',
    #         suppress_ticks=True)
        
    #     # position in decimal lat/lon
    #     for row in self.node.iterrows():
    #         self.lat.append(row[1][1])
    #     for row in self.node.iterrows():
    #         self.lon.append(row[1][2])
    #     for row in self.node.iterrows():
    #         self.Firm.append(row[1][0])
    #     for row in self.node.iterrows():
    #         self.size.append(row[1][6])
    #     for row in self.node.iterrows():
    #         self.risk.append(row[1][6])
    #     for row in self.node.iterrows():
    #         self.Fr.append(row[1][11])
    #     for row in self.node.iterrows():
    #         self.Sev.append(row[1][12])
            
    #     # convert lat and lon to map projection
    #     mx,my=m(self.lon,self.lat)
        
    #     #add nodes/edges with their attributes 
    #     for row in self.node.iterrows():
    #         self.network.add_node(row[1][0], label=row[1][3],ID=row[1][0], type=row[1][5], regioncode=row[1][4],lat=row[1][1],long=row[1][2], size = (int(row[1][6])*10), risk =row[1][6], Fr= row [1][11], Sev = row [1][12])
    #     for row in self.edge.iterrows():
    #         self.network.add_edge(row[1][0], row[1][2],USGR=row[1][4],LT=row[1][11])
            
    #     for i in range (0, len(self.node)):
    #         self.pos[self.Firm[i]]=(mx[i],my[i])
    #     #print(len(self.network.edges()))
    #     #RNDEDG1(self.network)
    #     #print(len(self.network.edges()))


    #     nx.draw(self.network,self.pos,with_labels = True)
    #     nx.draw_networkx_edges(G = self.network, pos = self.pos ,style='dashdot',edge_color='b', alpha=0.2)
    #     # Now draw the map
    #     m.drawcountries(linewidth = 0.5)
    #     m.drawstates()
    #     #m.fillcontinents(color='white',lake_color='white')
    #     m.drawcountries(color="black")
    #     m.drawcoastlines(linewidth=0.5)
    #     #m.bluemarble()
    #     plt.title('Ford Supplier Network M306 Commudity')
    #     plt.savefig(self.save + "/Map.png", format = "png", dpi = 300)
    #     plt.close()
        #plt.show()
    
    def smvsnetwork(self):
        for row in self.node.iterrows():
            self.Firm.append(row[1][0])
        for row in self.node.iterrows():
            self.size.append(row[1][6])
        for row in self.node.iterrows():
            self.lat.append(row[1][1])
        for row in self.node.iterrows():
            self.lon.append(row[1][2])
        for row in self.node.iterrows():
            self.risk.append(row[1][6])
        for row in self.node.iterrows():
            self.Fr.append(row[1][11])
        for row in self.node.iterrows():
            self.Sev.append(row[1][12])
            
        #add nodes/edges with their attributes 
        for row in self.node.iterrows():
            self.network.add_node(row[1][0],label=row[1][3] ,ID=row[1][0], type=row[1][5], regioncode=row[1][4],lat=row[1][1],long=row[1][2], size = int(row[1][6])*100, risk =row[1][6], Fr= row [1][11], Sev = row [1][12])
        for row in self.edge.iterrows():
            self.network.add_edge(row[1][0], row[1][2], USGR=row[1][4], LT=row[1][12])
    
        for i in range (0, len(self.node)):
            self.pos[self.Firm[i]]=(self.lat[i],self.lon[i])
        plt.figure()    
        nx.draw(self.network,self.pos,with_labels = True)
        nx.draw_networkx_edges(G = self.network, pos = self.pos ,style='dashdot',edge_color='b', alpha=0.2)
        
        #map Network
        
        plt.title('Ford Supplier Network M306 Commudity')
        plt.savefig(self.save + "/Map.png", format = "png", dpi = 300)
        plt.close()
        #plt.show()
    
    
    def get_allnodes (self):
        return self.network.nodes(data=True)
    
    def network_metrics (self):# find the  network metrics 
        N= self.network.order()
        e = self.network.size()
        Clos_Centrality = nx.closeness_centrality(self.network)
        average_clustering = nx.average_clustering(self.network)
        betweenness_centralit = nx.betweenness_centrality(self.network)
        self.degree= nx.degree(self.network)
        df1=pd.DataFrame([Clos_Centrality])
        df2=pd.DataFrame([average_clustering])
        df3=pd.DataFrame([betweenness_centralit])
        df4=pd.DataFrame([self.degree])
        df1.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/{}.csv'.format("Clos_Centrality"), index=False)#save Resilianc
        df2 .to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/{}.csv'.format("average_clustering"), index=False)#save Resilianc
        df3.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/{}.csv'.format("betweenness_centralit"), index=False)#save Resilianc
        df4.to_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Optmization/resultssimulation/{}.csv'.format("Degree"), index=False)#save Resilianc
        print("Basic Graph Properties :")
        print("Node : " + str(N) + ";  "+ "Edge : " + " "+ str(e) + ";  "+ "Density : " + str(nx.density(self.network)))
        print ("Average Clustering coefficient : " + str(df2.max()))
        #print ("closeness centrality : " + str(df4.max()))
        #print ("Betweenness centrality : " + str(df3.max()))
        #print ("centrality : " + str(nx.centrality(self.network)))
        
      
        
    
    
                
        

    