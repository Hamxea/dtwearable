from abc import abstractmethod
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from  keras.layers import Dense, Flatten

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np


class MultilayerPerceptronMultiStepOutput(AbstractAIModel):
    """ Mutlilayer (MLP) Perceptron with Multi-Step Output... """

    global mlp_model
    global graph

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        #df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              hyperparameters['n_steps_in'], hyperparameters['n_steps_out'])
        mlp_model = self.train_mlp(X_train, y_train)
        graph = tf.get_default_graph()

        with graph.as_default():
            score, acc = self.test_mlp(mlp_model, X_test, y_test)

        return mlp_model, {"score": score, "accuracy": acc}

    def split_dataset(self, df, test_ratio, n_steps_in, n_steps_out):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, n_steps_in, n_steps_out)

        return train_test_split(X, y, test_size=test_ratio, shuffle=False, stratify=None)

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_sequences(self, df, n_steps_in, n_steps_out):
        """ split a multivariate sequence into samples method"""
        """
        #n_steps_in = 3
        #n_steps_out = 1
        """
        sequences = df.to_numpy()
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)

        X, y = array(X), array(y)
        return  X, y

    def train_mlp(self, X_train, y_train):
        """ Method that creates mlp model using x_train and y_train """

        # flatten input
        n_input = X_train.shape[1] * X_train.shape[2]
        X_train = X_train.reshape((X_train.shape[0], n_input))
        # flatten output
        n_output = y_train.shape[1] * y_train.shape[2]
        y_train = y_train.reshape((y_train.shape[0], n_output))

        # define model
        model = Sequential()
        model.add(Dense(100, activation='relu', input_dim=n_input))
        model.add(Dense(n_output))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        # fit model
        model.fit(X_train, y_train, epochs=2000, verbose=0)

        return model

    def test_mlp(self, mlp_model, X_test, y_test):
        """ Method that calculates score using X_test and y_test on the created mlp model """
        X_test = X_test[np.size(X_test, 0) - 1:, :]
        # flatten input
        n_input = X_test.shape[1] * X_test.shape[2]
        X_test = X_test.reshape(1, n_input)
        yha_predict = mlp_model.predict(X_test, verbose=0)
        print(yha_predict)

        """ Evaluation function of an input given a score """
        score, acc = mlp_model.evaluate(X_test, yha_predict,  verbose = 0)
        print("Score:", score)
        print(("Accuracy", acc))

        return score, acc

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
