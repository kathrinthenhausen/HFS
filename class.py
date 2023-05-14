

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score
import networkx as nx
from sklearn.naive_bayes import BernoulliNB
from fixtures import getFixedData
from fixtures import getFixedDag

from helpers import getRelevance



class Filter(BaseEstimator, TransformerMixin):
    def __init__(self, graph_data, k=0, option="HNB"): #todo G = None
        self.graph_data = graph_data
        self.option = option
        self.k = k
        self._relevance = {}
        self._descendants = {}
        self._ancestors = {}

    #def fit(self, X, y=None):
    #    return self

    def __get_relevance(self, node):
        return getRelevance(self._xtrain, self._ytrain, node)
    
    def __get_ancestors(self, node):
        return nx.ancestors(self._digraph, node)
    
    def __get_descendants(self, node):
        return nx.descendants(self._digraph, node)
    
    def __create_digraph(self):
        self._digraph =  nx.from_numpy_array(self.graph_data, parallel_edges = False, create_using = nx.DiGraph)

    def _get_sorted_relevance(self):
        self._sorted_relevance = sorted(self._relevance, key=self._relevance.get)
    
    
    def fit(self, X_train, y_train, X_test):
        """
        Fit a local hierarchical classifier.

        Needs to be subclassed by other classifiers as it only offers common methods.

        Parameters
        ----------
        X_train : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples. Internally, its dtype will be converted
            to ``dtype=np.float32``. If a sparse matrix is provided, it will be
            converted into a sparse ``csc_matrix``.
        X_test : {array-like, sparse matrix} of shape (n_samples, n_features)
            The test input samples. Internally, its dtype will be converted
            to ``dtype=np.float32``. If a sparse matrix is provided, it will be
            converted into a sparse ``csc_matrix``.
        y_train : array-like of shape (n_samples, n_levels)
            The target values, i.e., hierarchical class labels for classification.
        

        Returns
        -------
        self : object
            Fitted estimator.
        """
        # Create DAG
        self.__create_digraph()
        self._xtrain = X_train
        self._ytrain = y_train
        self._xtest = x_test

        # Get relevance, ancestors and descendants of each node
        for node in self._digraph:
            self._relevance[node] =  self.__get_relevance(node)
            self._ancestors[node] =  self.__get_ancestors(node)
            self._descendants[node] =  self.__get_descendants(node)
        self._get_sorted_relevance()

        predictions = []
        for idx, instance in enumerate(self._xtest):
            self._get_nonredundant_features(idx)
            self._get_top_k()
            predictions.append(self._predict(idx, instance)[0])

        return predictions

    def _get_nonredundant_features(self, idx):
        self._instance_status = {}
        for node in self._digraph:
            self._instance_status[node] = 1

        for node in self._digraph:
            if self._xtest[idx][node] == 1:
                for anc in self._ancestors[node]:
                    if self._relevance[anc] <= self._relevance[node]:
                        self._instance_status[anc] = 0
            else:
                for desc in self._descendants[node]:
                    if self._relevance[desc] <= self._relevance[node]:
                        self._instance_status[desc] = 0
        print(self._instance_status)
    
    def _get_top_k(self):
        counter = 0
        for node in self._sorted_relevance:
            if (counter < self.k or not self.k) and self._instance_status[node]:
                pass
            else:
                self._instance_status[node] = 0
            counter+=1
#
    def _predict(self, idx, instance):
        print(self._instance_status)
        features = [nodes for nodes, status in self._instance_status.items() if status]
        clf = BernoulliNB()
        print(self._xtrain[:, features].shape, self._ytrain.shape)
        clf.fit(self._xtrain[:,features], self._ytrain)
        return clf.predict(instance[features].reshape(1, -1))
    
    def score(self, ytest, predictions):
        print(predictions)
        print("accuracy: "+str(accuracy_score(y_true = ytest, y_pred=predictions)))


    def transfrom():
        pass

    def predict():
        pass

x = Filter(nx.to_numpy_array(getFixedDag()))   
x_t, y_t = getFixedData(10)
x_test, y_test = getFixedData(5)     
pred = x.fit(x_t, y_t, x_test)
print(pred)
x.score(y_test, pred)