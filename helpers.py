from fractions import Fraction

    

def getRelevance(X, y, i):

    p1 = Fraction(X[(X[:,i]==1)& (y==1)].shape[0], X[(X[:,i]==1)].shape[0]) if X[(X[:,i]==1)].shape[0] != 0 else 0
    p2 = Fraction(X[(X[:,i]==1)& (y==0)].shape[0], X[(X[:,i]==1)].shape[0]) if X[(X[:,i]==1)].shape[0] != 0 else 0
    p3 = 1 -p1
    p4 = 1 -p2


    rel = (p1-p2)**2 + (p3-p4)**2
    #print(p1, p2, p3, p4, rel)
    return rel


