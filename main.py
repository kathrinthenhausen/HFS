import string
from algorithms import algo, algowithtest
from fixsmall import getFixed2Data, getSmallFixedDag
from fixtures import getFixedDag, getFixedData
    
def real():
    data = getFixedData(100)
    test = getFixedData(10)
    G = getFixedDag()
    print(test)
    algowithtest(data, G, 10, test, 0)



def test():
    columns = {"0": int,"1": int, "2": int, "3": int, "4": int, "y": string}
    data = getFixed2Data()
    G = getSmallFixedDag()
    algo(data, G, 5, 1)

real()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
