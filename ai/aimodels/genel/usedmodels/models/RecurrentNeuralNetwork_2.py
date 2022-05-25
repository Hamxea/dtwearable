import errno
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

from keras.regularizers import l2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import SimpleRNN
import matplotlib.pyplot as plt

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import os


class RecurrentNeuralNetwork_2(AbstractAIModel):
    """ Recurrent Neural Network with 1-Step Output """

    global lstm_model
    global graph
    global EPOCHS
    EPOCHS = 25

    # User home altında ai_models klasörünün path'i
    file_path_plot = os.path.join("ai_models", "ai_models_plots")

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'], )
        rnn_model = self.train_rnn(X_train, y_train, X_test, y_test, dataset_parameters['window_size'])
        graph = tf.get_default_graph()

        with graph.as_default():
            acc, loss = self.test_rnn(rnn_model, X_test, y_test, dataset_parameters['window_size'])

        return rnn_model, {"accuracy": acc, "loss": loss}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, window_size)

        return train_test_split(X, y, test_size=test_ratio)  # , shuffle=False, stratify=None)

    def split_sequences(self, df, window_size):
        """ split a multivariate sequence into samples method"""
        """
        #window_size_in = 3
        #window_size_out = 1
        """
        sequences = df.to_numpy()
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

    def train_rnn(self, X_train, y_train, X_test, y_test, window_size):
        """ Method that creates rnn model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        # window_size = 3

        # define model
        model = Sequential()
        model.add(SimpleRNN(100, activation='relu', return_sequences=True, input_shape=(window_size, n_features),
                            kernel_regularizer=l2(0.01), recurrent_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
        model.add(SimpleRNN(100, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(6, kernel_regularizer=l2(0.01), activation='sigmoid'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',  metrics=['accuracy'])

        # fit model
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=EPOCHS, verbose=0)
        self.plot_model(history)

        return model

    def test_rnn(self, rnn_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created rnn model """

        yha_predict = rnn_model.predict(X_test, verbose=0)
        print(yha_predict)

        """ Evaluation function of an input given a score """
        (loss, acc) = rnn_model.evaluate(X_test, y_test, verbose=0)
        print(acc, loss)

        return acc, loss

    def plot_model(self, model_history):
        """ Epoch sayısı üzerinden eğitim kaybı ile doğrulama kaybının grafiğini çizer. """

        try:
            os.makedirs(self.file_path_plot)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        ai_model_plot_file_name = os.path.join(self.file_path_plot, __name__ + "_" + str(datetime.now().timestamp()) + ".png")

        acc_train = model_history.history['acc']
        loss_train = model_history.history['loss']
        acc_val = model_history.history['val_acc']
        loss_val = model_history.history['val_loss']
        epochs = range(1, EPOCHS+1)
        plt.plot(epochs, acc_train, label='Training Accuracy')
        plt.plot(epochs, loss_train, label='Training loss')
        plt.plot(epochs, acc_val, label='Validation Accuracy')
        plt.plot(epochs, loss_val, label='Validation loss')
        plt.title('RNN Training Loss and Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Loss/Accuracy')
        plt.legend()
        plt.savefig(ai_model_plot_file_name)
        plt.show()
        plt.close()

        return

    def plot_model_2(self, model_history):
        """ Epoch sayısı üzerinden eğitim kaybı ile doğrulama kaybının grafiğini çizer. """

        ai_model_plot_file_name = os.path.join(self.file_path_plot, __name__ + "_" + str(datetime.now().timestamp()) + ".png")

        acc_train = model_history.history['acc']
        loss_train = model_history.history['loss']
        acc_val = model_history.history['val_acc']
        loss_val = model_history.history['val_loss']

        # plot history
        plt.ion()
        fig = plt.figure()
        subfig = fig.add_subplot(122)
        subfig.plot(acc_train, label="training accuracy")
        if acc_val is not None:
            subfig.plot(acc_val, label="validation accuracy")
        subfig.set_title('Model Accuracy')
        subfig.set_xlabel('Epoch')
        subfig.legend(loc='upper left')
        subfig = fig.add_subplot(121)
        subfig.plot(loss_train, label="training loss")
        if loss_val is not None:
            subfig.plot(loss_val, label="validation loss")
        subfig.set_title('Model Loss')
        subfig.set_xlabel('Epoch')
        subfig.legend(loc='upper left')
        fig.savefig(ai_model_plot_file_name)
        fig.show()
        plt.ioff()

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
