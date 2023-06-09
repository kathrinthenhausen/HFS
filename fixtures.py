import networkx as nx
import pandas as pd
import random
import numpy as np

_instance_number = 20
_feature_number = 9
def getFixedDag():
    return nx.DiGraph([(0,1),(0,2),(0,3),(1,4),(1,5),(4,6),(4,7),(3,7),(5,8)])
    return nx.DiGraph()


def getFixedAnnotated_dag():
    G = getFixedDag()
    attr = {0: 1, 1: 1, }
    G.add_nodes_from(attr)
    return G

def rand():
    return random.getrandbits(1)



def randomLinesWithAssertions():
    b = rand()
    c = rand()
    d = rand()
    e = rand() if b == 1 else 0
    f = rand() if b == 1 else 0
    g = rand() if e*d == 1 else 0
    h = rand() if e == 1 else 0
    i = rand() if f == 1 else 0
    return (1,b,c,d,e,f,g,h,i)
   


def getFixedData(instance_number = _instance_number):
    df = pd.DataFrame(columns=[i for i in range(0,_feature_number)])
    for row in range(0,instance_number):
        df.loc[len(df)] = randomLinesWithAssertions()
    df["y"] = np.random.randint(0, 2, df.shape[0])
    return df
