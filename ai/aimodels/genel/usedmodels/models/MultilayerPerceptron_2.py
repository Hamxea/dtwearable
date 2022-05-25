import errno
import os
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

from keras.regularizers import l2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import matplotlib.pyplot as plt


class MultilayerPerceptron_2(AbstractAIModel):
    """ Mutlilayer (MLP) Perceptron with 1-Step Output """

    global mlp_model
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
                                                              dataset_parameters['window_size'])
        mlp_model = self.train_mlp(X_train, y_train, X_test, y_test)
        graph = tf.get_default_graph()

        with graph.as_default():
            acc, loss = self.test_mlp(mlp_model, X_test, y_test)

        return mlp_model, {"accuracy": acc, "loss": loss}

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
        """ split a multivariate sequence into samples method """
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

    def train_mlp(self, X_train, y_train, X_test, y_test):
        """ Method that creates mlp model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        n_input = X_train.shape[1] * X_train.shape[2]
        X_train = X_train.reshape((X_train.shape[0], n_input))
        # flatten output
        n_output = y_train.shape[1]

        n_input_test = X_test.shape[1] * X_test.shape[2]
        X_test = X_test.reshape(X_test.shape[0], n_input_test)

        # define model
        model = Sequential()
        model.add(Dense(100, activation='relu', input_dim=n_input,
                        kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
        model.add(Dense(100, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01), activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(64, kernel_regularizer=l2(0.01), activation='relu'))
        model.add(Dense(6, kernel_regularizer=l2(0.01), activation='sigmoid'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
        # fit model
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=EPOCHS, verbose=0)
        self.plot_model(history)

        return model

    def test_mlp(self, mlp_model, X_test, y_test):
        """ Method that calculates score using X_test and y_test on the created mlp model """

        # flatten input
        n_input = X_test.shape[1] * X_test.shape[2]
        # X_test = X_test.reshape(1, n_input)
        # yha_predict = mlp_model.predict(X_test, verbose=0)
        # print(yha_predict)

        X_test = X_test.reshape(X_test.shape[0], n_input)

        """ Evaluation function of an input given a score """
        (loss, acc) = mlp_model.evaluate(X_test, y_test, verbose=0)
        # score = round(score[1], 3)

        yha_predict = mlp_model.predict(X_test, verbose=0)
        print(yha_predict)
        print("Loss:", loss)
        print("Accuracy", acc)

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
        plt.title('MLP Training Loss and Accuracy')
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
