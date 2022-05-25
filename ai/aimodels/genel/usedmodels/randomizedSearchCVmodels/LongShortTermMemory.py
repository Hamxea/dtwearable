import errno
import os
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.models import Sequential
from keras.regularizers import l2
from keras.wrappers.scikit_learn import KerasClassifier
from numpy import array
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, log_loss
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

from ai.aimodels.AbstractAIModel import AbstractAIModel


class LongShortTermMemory(AbstractAIModel):
    """ Long Short TermMemory (lstm) with 1-Step Output """

    global lstm_model
    global graph
    global EPOCHS
    EPOCHS = 25

    # User home altında ai_models klasörünün path'i
    file_path_plot = os.path.join("ai_models", "ai_models_plots")

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'], )
        lstm_model = self.train_lstm(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                     parameters=hyperparameters['parameters'],
                                     cross_validation=hyperparameters['cross_validation'],
                                     num_iteration=hyperparameters['number_iteration'],
                                     window_size=dataset_parameters['window_size'])
        graph = tf.get_default_graph()

        with graph.as_default():
            acc, loss, best_parameters, classifi_metrics_report, conf_matrix_evaluation = self.test_lstm(
                lstm_model, X_test, y_test, dataset_parameters['window_size'])

        return lstm_model, {"accuracy": acc,
                            "classification metrics report": classifi_metrics_report,
                            "confusion matrix evaluation": str(conf_matrix_evaluation),
                            "Best parameters": best_parameters, "loss": loss}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, window_size)

        return train_test_split(X, y, test_size=test_ratio, shuffle=True, random_state=42, stratify=None)

    def split_sequences(self, df, window_size):

        train_df = df.iloc[:, -11:]  # Select last 11 columns (features and output) in a dataframe for training
        self.data_normalization_scaling(train_df)

        # convert the date into numpy and apply windowing (window_size)
        sequences = train_df.to_numpy()
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + window_size
            # check if we are beyond the dataset
            if end_ix > len(sequences) - 1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x[:, :-1])
            y.append(seq_y[-1:])
        X, y = array(X), array(y)
        return X, y

    def create_model(self, init_mode, optimizer, units, activation,
                     dropout_rate):

        # define model
        model = Sequential()
        model.add(LSTM(units, activation=activation, input_shape=(3, 10),
                       return_sequences=True))
        model.add(Dropout(dropout_rate))
        model.add(LSTM(units, activation=activation, kernel_initializer=init_mode, input_shape=(3, 10)))
        model.add(Dense(4, activation='softmax'))

        print(model.summary())
        model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def train_lstm(self, X_train, y_train, X_test, y_test, parameters, cross_validation, num_iteration, window_size, ):
        """ Method that creates lstm model using x_train and y_train """

        # create model
        model = KerasClassifier(build_fn=self.create_model)
        grid = RandomizedSearchCV(estimator=model, param_distributions=parameters, cv=cross_validation, n_jobs=-1,
                                  n_iter=num_iteration,
                                  return_train_score=True)  # n_jobs = -1 or multiprocessing.cpu_count()-1

        grid_result = grid.fit(X_train, y_train)
        print('Best score: ', grid_result.best_score_)
        print('Best parameters: ', grid_result.best_params_)

        return grid_result

    def test_lstm(self, lstm_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created lstm model """

        yha_predict = lstm_model.predict(X_test)
        print(yha_predict)

        cl_report = classification_report(y_test, yha_predict)
        print('Report showing the main classification metrics: \n', cl_report)

        cm = confusion_matrix(y_test, yha_predict)
        print('Confusion matrix to evaluate the accuracy of a classification: \n', cm)

        """ Evaluation function of an input given a score """
        # (loss, acc)
        acc = lstm_model.score(X_test, y_test)

        # loss = log_loss(y_test, (np.reshape(yha_predict, (yha_predict.shape[0], 1))))
        # print("Loss:", loss)
        print("Test Accuracy:", acc)

        return lstm_model.best_score_, 0, lstm_model.best_params_, cl_report, cm

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
