from numpy import *
from sklearn.tree import DecisionTreeClassifier
from skmultiflow.core.utils.data_structures import InstanceWindow
from skmultiflow.core.utils.utils import *

class BatchClassifier:

    def __init__(self, window_size = 100, max_models = 100):
        self.H = []
        self.h = None
        self.window_size = window_size
        self.max_models = max_models
        self.window = InstanceWindow(window_size)
        self.j = 0
        # self.n_DT=0

    def partial_fit(self, X, y=None, classes=None):

        # Get information on the input stream
        r, c = get_dimensions(X)

        # DEBUG MESSAGES
        # print("Begin MAX H "+str(self.max_models))
        # print("r:" +str(r)+" c:" +str(c))

        for i in range(r):
            # Check if the window is instanciated
            if self.window is None:
                self.window = InstanceWindow(self.window_size)

            # Add an element to the window (1 row)
            self.window.add_element(np.asarray([X[i]]), np.asarray([[y[i]]]))

            # Increment the counter for the n_elements
            self.j+=1
            # Create the model (DT)
            if self.h is None :
                self.h = DecisionTreeClassifier()

            # Check if the window is full
            if self.j == self.window_size:
                # A new model has to be generated
                # print("### FITTING MODEL "+str(self.n_DT)+" UNTIL RECORD "+str(i)+" ###")
                # Train the new model
                X_batch=self.window.get_attributes_matrix()
                y_batch=self.window.get_targets_matrix()
                self.h.fit(X_batch,y_batch)
                # Keep only self.max_models : pop the oldest to push a new one
                if(len(self.H) == self.max_models):
                    self.H.pop(0)
                self.H.append(self.h)
                # Update the counters
                # self.n_DT+=1
                self.j=0
                # DEBUG MESSAGES
                # print("CURRENT LEN H "+str(len(self.H)))
                # print("CURRENT MAX H "+str(self.max_models))
                # print("HELLO WORLD "+str(self.H))

        return self

    def predict(self, X):
        # TODO
        N,D = X.shape
        # print("### PREDICTING "+str(X)+" ###")
        # print("N:" +str(N)+" D:" +str(D))
        # Set the predictions to zero
        predictions = zeros(len(self.H)) if len(self.H) > 0 else 0

        # Compute predictions with the current models
        # print("CURRENT LEN H "+str(len(self.H)))
        for i in range(len(self.H)):
            predictions[i] = self.H[i].predict(X)
        
        # print("PREDICTIONS: "+str(predictions))
        # print("FINAL PRED: "+str(np.bincount(asarray(predictions, dtype=int64)).argmax()))
        # # Return Majority class of predictions
        # return ndarray(shape=(N,), buffer=np.bincount(asarray(predictions, dtype=int64)).argmax())
        return predictions
