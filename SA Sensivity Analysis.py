from SALib.sample import saltelli
from SALib.analyze import delta,rbd_fast,sobol,morris,dgsm
from SALib.test_functions import Ishigami
import numpy as np
import pandas as pd
import csv
#Y = np.loadtxt(r"C:\Users\elham\Google Drive\Book21.txt", float)

file_location = 'C:/Users/elham/Google Drive/ReSearch/Simulation/GSA/Book25.xlsx'#input edge and nodes of our network
YY=pd.read_excel(file_location, sheet_name='Output',index=False)#save list of nodes to obtain the risk settings
YYt=YY.T
f=YYt.to_numpy()

#print(f[0].shape)  
#print(f[0])   
problem = {
    'num_vars': 20,
    'names': ['Risk1','Risk2','Risk3','Risk4','Risk5','Risk6','Risk7','Risk8','Risk9','Risk10','Risk11','Risk12','Risk13','Risk14','Risk15','Risk16','Risk17','Risk18','Risk19','Risk20'],
    'bounds': [[0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10],
               [0, 10]]             
}
X=pd.read_excel(file_location, sheet_name='Input',index=False)#save list of nodes to obtain the risk settings
XX=X.to_numpy()
#param_values = saltelli.sample(problem, 210)
#Y = Ishigami.evaluate(param_values)

Di = delta.analyze(problem, XX, f[0], print_to_console=True)
#Si = sobol.analyze(problem, f[0], conf_level=0.95, print_to_console=True)
#Gi=dgsm.analyze(problem, XX, f[0], num_resamples=15, conf_level=0.95, print_to_console=False, seed=None)
#Mi = morris.analyze(problem, XX, f[0], conf_level=0.95, print_to_console=True, num_levels=4)
Si = rbd_fast.analyze(problem, XX, f[0],M=5, print_to_console=True)



