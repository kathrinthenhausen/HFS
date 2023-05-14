import networkx as nx
import random

import numpy as np
import pandas as pd

def getSmallFixedDag():
    return nx.DiGraph([(0,1), (0,2), (1,3), (1,4), (2,4)])


def rand():
    return random.getrandbits(1)

def randomLinesWithAssertions():
    b = rand()
    c = rand()
    d = rand() if b == 1 else 0
    e = rand() if b*c == 1 else 0
    return (1,b,c,d,e)

def getFixedData():
    instance_number = 5
    df = pd.DataFrame(columns=[i for i in range(0,5)])
    for row in range(0,instance_number):
        df.loc[len(df)] = randomLinesWithAssertions()
    df["y"] = np.random.randint(0, 2, df.shape[0])
    df.to_csv('small1.csv', encoding='utf-8')

def getFixed2Data():
    data = {
        0:[1,1,1,1,1],
        1:[1,0,0,1,1],
        2:[0,1,0,0,1],
        3:[1,0,0,1,0],
        4:[0,0,0,0,1],
        "y":[1,0,1,1,0]}
    return pd.DataFrame(data).to_numpy()
