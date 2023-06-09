
import string
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

from helpers import getRelevance


def algo(data, G, k, test, verbose = 0):

    ancestors = {}
    descendants = {}
    relevance = {}
    status = {}

    for feature in range(data.shape[1]-1):
        ancestors[feature] = nx.ancestors(G, feature)
        descendants[feature] = nx.descendants(G, feature)
        relevance[feature] = getRelevance(data, feature)
    sorted_relevance = sorted(relevance, key=relevance.get)
    
    if (verbose):
        print("ancestors: "+str(ancestors) + "descendants: " + str(descendants))
        for i in range(data.shape[1]-1):
            print("i: "+str(float(relevance[i])))
        
    
    for row in range(data.shape[0]):
        instance_status = {}
        for feature in range(data.shape[1]-1):
            instance_status[feature] = 1
            if data.loc[row].at[feature] == 1:
               for anc in ancestors[feature]:
                    if relevance[anc] <= relevance[feature]:
                        instance_status[anc] = 0
            else:
                for desc in descendants[feature]:
                    if relevance[desc] <= relevance[feature]:
                        instance_status[desc] = 0
        status[row] = instance_status
       
        #create select1 mit go_i
        select1 = [feature for feature, status in instance_status.values() if status == 1]
        select2 = []
        counter = 0
        for feature in sorted_relevance:
            if counter < k and instance_status[feature] ==1:
                select2.append(feature)
                counter+=1
        select2.append("y")
        instance_data = data[select2].at(row)
        instance_test = test[select2].at(row)
        print(instance_data)
        clf = GaussianNB()
        clf.fit(instance_data.iloc[:, 0:-1], instance_data["y"])
        y_pred = clf.predict(instance_test.iloc[:, 0:-1])
        print("accuracy: "+str(accuracy_score(y_true = test["y"], y_pred=y_pred)))


def algowithtest(data, G, k, test, verbose = 0):
    
    ancestors = {}
    descendants = {}
    relevance = {}
    status = {}

    #initialize
    for feature in range(data.shape[1]-1):
        ancestors[feature] = nx.ancestors(G, feature)
        descendants[feature] = nx.descendants(G, feature)
        relevance[feature] = getRelevance(data, feature)
    sorted_relevance = sorted(relevance, key=relevance.get)
    
    if (verbose):
        print("ancestors: "+str(ancestors) + "descendants: " + str(descendants))
        for i in range(data.shape[1]-1):
            print("i: "+str(float(relevance[i])))
        
    predictions = []
    for row in range(test.shape[0]):
        instance_status = {}
        for feature in range(data.shape[1]-1):
            instance_status[feature] = 1
            if test.loc[row].at[feature] == 1:
               for anc in ancestors[feature]:
                    if relevance[anc] <= relevance[feature]:
                        instance_status[anc] = 0
            else:
                for desc in descendants[feature]:
                    if relevance[desc] <= relevance[feature]:
                        instance_status[desc] = 0
        status[row] = instance_status
       
        #create select1 mit go_i
        select1 = [feature for feature, status in instance_status.values() if status == 1]
        select2 = []
        counter = 0
        for feature in sorted_relevance:
            if counter < k and instance_status[feature] ==1:
                select2.append(feature)
                counter+=1
        select2.append("y")
        instance_data = data[select2]
        instance_test = test[select2].loc[row]
        clf = GaussianNB()
        clf.fit(instance_data.iloc[:, 0:-1], instance_data["y"])
        predictions.append(clf.predict(instance_test.iloc[0:-1].values.reshape(1,-1))[0])
    print("accuracy: "+str(accuracy_score(y_true = np.array(test["y"]), y_pred=predictions)))

