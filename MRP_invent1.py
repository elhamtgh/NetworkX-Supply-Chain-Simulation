# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 04:08:46 2020

@author: elham
"""

import simpy
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from CreateNetwork import VisualNetwork_input_output
from NetworkSimulation import genrate_network
import operator 
#import csv

"""Class for new replenishment order placed
by a stocking facility to its upstream
replenishing stocking facility.  The order object
contains order quantity and which facility is
placing that order
"""
class new_order(object):

    def __init__(self, requester, order_qty):
        self.requester = requester #requester can be focal firm, supplier tier1 and tier 2
        self.orderQty = order_qty #order quantity requested by requester  


"""Stocking facility class
Each stocking location in the multi-echelon 
network is an object of this class
"""
class stocking_facility(object):
    
    # initialize the new facility object
    def __init__(self, env, node_id, is_source, initial_inv, ROP, base_stock,
                 upstream, hist_demand, default_lead_time, lead_time_delay):
        self.env = env
        self.name = "node" + str(node_id)
        self.isSource = is_source
        self.on_hand_inventory = initial_inv
        self.inventory_position = initial_inv
        self.ROP = ROP
        self.baseStock = base_stock
        self.upstream = upstream
        self.histDemand = hist_demand
        self.defaultLeadTime = default_lead_time
        self.leadTimeDelay = lead_time_delay
        self.order_q = []
        self.totalDemand = 0.0
        self.totalBackOrder = 0.0
        self.totalLateSales = 0.0
        self.serviceLevel = 0.0
        self.avgOnHand = 0.0
        self.onHandMon = []
        
        # start the processes
        self.env.process(self.check_inventory())
        self.env.process(self.prepare_replenishment())
        self.env.process(self.serve_customer())
        

    # process to place replenishment order
    def check_inventory(self):
        while True:
            yield self.env.timeout(1.0)
            if self.inventory_position <= 1.05 * self.ROP:  # add 5% to avoid rounding issues
                order_qty = self.baseStock - self.on_hand_inventory
                order = new_order(self, order_qty)
                self.upstream.order_q.append(order)
                self.inventory_position += order_qty

    # process to fulfill replenishment order
    def prepare_replenishment(self):
        while True:
            if len(self.order_q) > 0:
                order = self.order_q.pop(0)

                shipment = min(order.orderQty, self.on_hand_inventory)
                if not self.isSource:
                    self.inventory_position -= shipment
                    self.on_hand_inventory -= shipment
    
                # if the order is not complete, wait for the material to appear
                # in the inventory before the complete replenishment can be sent
                remaining_order = order.orderQty - shipment
                if remaining_order:
                    while not self.on_hand_inventory >= remaining_order:
                        yield self.env.timeout(1.0)
                    if not self.isSource:
                        self.inventory_position -= remaining_order
                        self.on_hand_inventory -= remaining_order
                self.env.process(self.ship(order.orderQty, order.requester))
            else:
                yield self.env.timeout(1.0)

    # process to deliver replenishment
    def ship(self, qty, requester):
        lead_time = requester.defaultLeadTime + \
                    np.random.choice(requester.leadTimeDelay, replace=True)  # bootstrap sample lead time delay
        yield self.env.timeout(lead_time)
        requester.on_hand_inventory += qty

    # process to serve customer demand
    def serve_customer(self):
        while True:
            self.onHandMon.append(self.on_hand_inventory)
            yield self.env.timeout(1.0)
            demand = np.random.choice(self.histDemand, replace=True)  # bootstrap sample historical
            self.totalDemand += demand
            shipment = min(demand + self.totalBackOrder, self.on_hand_inventory)
            self.on_hand_inventory -= shipment
            self.inventory_position -= shipment
            backorder = demand - shipment
            self.totalBackOrder += backorder
            self.totalLateSales += max(0.0, backorder)
"""
to run simulation we need some input from our network 
First we have need add demand and import our network in model

"""
D=pd.read_csv('C:/Users/elham/Google Drive/ReSearch/Simulation/Sympi/demand.csv')#read demand which is follow MRP method

VIO=VisualNetwork_input_output()#input network info node, edge and their attributes
Node_DATA = VIO.UNodeslist.set_index("ID", drop = False) #save node info with related attributes
Edge_DATA = VIO.UEdgeslist #save edge info with related attribute
C1=genrate_network(VIO.UNodeslist,Edge_DATA ,VIO.OutSave)
C1.smvsnetwork()
num_nodes= len(Node_DATA) #number of node in our networl


def simulate_network(seedinit, num_nodes, network, initial_inv, ROP,
                     base_stock, demand, lead_time, lead_time_delay):

    env = simpy.Environment()  # initialize SimPy simulation instance
    np.random.seed(seedinit)
    
    nodes = Node_DATA  # list of the objects of the storage facility class
    

    for n in nodes:
        Sucessor_Company_List = list(C1.network.successors(n))#for current node find sucessor company or nodes
        Pre_Company_list=list(C1.network.predecessors(n))#for current node find predecessors company or nodes
        if len(Pre_Company_list)== 0:  # then it is the last tiers supply nodes, which is assumed to have infinite inventory
            for su in Sucessor_Company_List:
                FilterST= Edge_DATA.loc[operator.and_(Edge_DATA['Source ID']==n,Edge_DATA['Target ID']==su)]
                s = stocking_facility(env, n, 1, Node_DATA.loc[n,'Int'], Node_DATA.loc[n,'R'], FilterST['SS'],
                                  None, np.zeros(100), FilterST['LT'], lead_time_delay)
        else:
            # first find the upstream facility before invoking the processes
            for su in Sucessor_Company_List:
                FilterST= Edge_DATA.loc[operator.and_(Edge_DATA['Source ID']==n,Edge_DATA['Target ID']==su)]
                s = stocking_facility(env, n, 0,  Node_DATA.loc[n,'Int'], Node_DATA.loc[n,'R'], FilterST['SS'],
                                          su, D.loc[ : , n ], FilterST['LT'], lead_time_delay)
                break
        
        nodes.append(s)

    env.run(until=360)

    # find the service level of each node
    for i in range(num_nodes):
        nodes[i].serviceLevel = 1 - nodes[i].totalLateSales / (nodes[i].totalDemand + 1.0e-5)

    # find the average on-hand inventory of each node
    for i in range(num_nodes):
        if i == 0: # then it is the first supply node, which is assumed to have infinite inventory
            nodes[i].avgOnHand = 0.0
        else:
            nodes[i].avgOnHand = np.mean(nodes[i].onHandMon)

    return nodes  # return the storageNode objects