from typing import Any
import networkx as nx
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

from helpers import getRelevance

class FeatureSelect():
    "Class for HNB, HNB-s, RNB"
    def __init__(
            self, digraph: nx.DiGraph, train, test
    ):
        self.digraph = digraph
        self.train = train
        self.test = test

    def _get_relevance(self, feature):
        return getRelevance(self.train, feature)
    
    def _get_ancestors(self, node):
        return nx.ancestors(self.digraph, node)
    
    def _get_descendants(self, feature):
        return nx.descendants(self.digraph, feature)
    
    def _get_sorted_relevance(self):
        relevance = {}
        for feature in range(self.test.shape[1]-1):
            relevance[feature]=self._get_relevance(feature)
        return sorted(relevance, key=relevance.get)

    def _get_nonredundant_features(self, instance):
        instance_status = {}
        for feature in range(self.train.shape[1]-1):
            instance_status[feature] = 1
    
        for feature in range(self.train.shape[1]-1):
            if self.test.loc[instance].at[feature] == 1:
                for anc in self._get_ancestors(feature):
                    if self._get_relevance(anc) <= self._get_relevance(feature):
                        instance_status[anc] = 0
            else:
                for desc in self._get_descendants(feature):
                    if self._get_relevance(desc) <= self._get_relevance(feature):
                        instance_status[desc] = 0
        select = [feature for feature, status in instance_status.items() if status == 1]
        select.append("y")
        return select

    def _get_top_k(self, k, feature_set = []):
        select = []
        counter = 0
        for feature in self._get_sorted_relevance():
            if counter < k and (feature in feature_set or feature_set == []):
                select.append(feature)
                counter+=1
        select.append("y")
        return select

    def fit_and_predict(self, option, k=0): 
        if k==0:
            k = self.train.shape[1]
        predictions = []
        for instance in range(self.test.shape[0]):
            print(instance)
            select = []
            if option == "hnb-s" or option == "hnb":
                select = self._get_nonredundant_features(instance)
                print(select)
            if option == "hnb":
                select = self._get_top_k(k, select)
            if option == "rnb":
                select = self._get_top_k(k)
            instance_train = self.train[select]
            instance_test = self.test[select].loc[instance]
            clf = GaussianNB()
        
            clf.fit(instance_train.iloc[:, 0:-1], instance_train["y"])
            predictions.append(clf.predict(instance_test.iloc[0:-1].values.reshape(1,-1))[0])
        print(predictions)
        print("accuracy: "+str(accuracy_score(y_true = np.array(self.test["y"]), y_pred=predictions)))


    


