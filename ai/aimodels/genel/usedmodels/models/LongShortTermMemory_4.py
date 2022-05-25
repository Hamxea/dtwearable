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
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, RandomizedSearchCV

from ai.aimodels.AbstractAIModel import AbstractAIModel


class LongShortTermMemory_4(AbstractAIModel):
    """ Long Short TermMemory (lstm) with 1-Step Output """

    global lstm_model
    global graph
    global EPOCHS
    EPOCHS = 25

    # User home altında ai_models klasörünün path'i

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)

        df.to_csv(r'C:\Users\hamza.mohammed\Desktop\kardiyoloji_data_original.csv', index=False)

        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'], )
        lstm_model = self.train_lstm(X_train, y_train, X_test, y_test, hyperparameters['parameters'],
                                     dataset_parameters['window_size'])
        graph = tf.get_default_graph()

        with graph.as_default():
            acc, loss = self.test_lstm(lstm_model, X_test, y_test, dataset_parameters['window_size'])

        return lstm_model, {"accuracy": acc, "loss": loss}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, window_size)

        return train_test_split(X, y, test_size=test_ratio, shuffle=True, stratify=None)

    def split_sequences(self, df, window_size):
        """ split a multivariate sequence into samples method """
        X = df.iloc[:, :-1]
        #y = df.iloc[:, -1:]
        y = df[df.columns[-1]]
        return X, y

    def create_model(self, init_mode, optimizer, units, activation,
                     dropout_rate):
        # flatten input and choose the number of features
        # n_features = X_train.shape

        # define model
        model = Sequential()
        model.add(Dense(units, input_dim=8, activation=activation))
        model.add(Dense(4, kernel_regularizer=l2(0.01), kernel_initializer=init_mode, activation='softmax'))
        print(model.summary())
        model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def train_lstm(self, X_train, y_train, X_test, y_test, parameters, window_size):
        """ Method that creates lstm model using x_train and y_train """

        # create model
        model = KerasClassifier(build_fn=self.create_model)

        """pipe = Pipeline([
            ('oversample', SMOTE(random_state=12)),
            ('clf', model)
        ])"""

        grid = RandomizedSearchCV(estimator=model, param_distributions=parameters, cv=15, n_jobs=-1, n_iter=10 ,
                                  return_train_score=True)  # n_jobs = -1 or multiprocessing.cpu_count()-1

        grid_result = grid.fit(X_train, y_train)
        print('Best score: ', grid_result.best_score_)
        print('Best parameters: ', grid_result.best_params_)
        # grid_result.pre

        # fit model
        # history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=EPOCHS, verbose=0)
        # self.plot_model(grid_result) or self.plot_model(history, EPOCHS, class_name=__name__)

        return grid_result

    def test_lstm(self, lstm_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created lstm model """

        yha_predict = lstm_model.predict(X_test)
        print(yha_predict)

        cl_report = classification_report(y_test, yha_predict)
        print(cl_report)

        cm = confusion_matrix(y_test, yha_predict)
        print(cm)

        """ Evaluation function of an input given a score """
        # (loss, acc)
        acc = lstm_model.score(X_test, y_test)
        # print("Loss:", loss)
        print("Accuracy:", acc)

        return acc, 0

    def plot_model(self, model_history):
        """ Epoch sayısı üzerinden eğitim kaybı ile doğrulama kaybının grafiğini çizer. """

        try:
            os.makedirs(self.file_path_plot)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        ai_model_plot_file_name = \
            self.file_path_plot + "\\" + __name__ + "_" + str(datetime.now().timestamp()) + ".png"

        acc_train = model_history.history['sparse_categorical_accuracy']
        loss_train = model_history.history['loss']
        acc_val = model_history.history['val_sparse_categorical_accuracy']
        loss_val = model_history.history['val_loss']
        epochs = range(1, EPOCHS + 1)
        plt.plot(epochs, acc_train, label='Training Accuracy')
        plt.plot(epochs, loss_train, label='Training loss')
        plt.plot(epochs, acc_val, label='Validation Accuracy')
        plt.plot(epochs, loss_val, label='Validation loss')
        plt.title('LSTM Training Loss and Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Loss/Accuracy')
        plt.legend()
        plt.savefig(ai_model_plot_file_name)
        plt.show()
        plt.close()

        return

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
