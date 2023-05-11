import string
from alg import FeatureSelect
from algorithms import hnb
from fixsmall import getFixed2Data, getSmallFixedDag
from fixtures import getFixedDag, getFixedData
    
def real():
    data = getFixedData(100)
    test = getFixedData(10)
    G = getFixedDag()
    print(test)
    hnb(data, G, 10, test, 0)

def class_real():
    data = getFixedData(100)
    test = getFixedData(10)
    G = getFixedDag()
    HFS = FeatureSelect(G, data, test)
    HFS.fit_and_predict("hnb")
    hnb(data, G, 10, test, 0)

def test():
    columns = {"0": int,"1": int, "2": int, "3": int, "4": int, "y": string}
    data = getFixed2Data()
    G = getSmallFixedDag()
    #hnb(data, G, 5, 1)

class_real()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
