import errno
import os
from abc import abstractmethod
from datetime import datetime
from pathlib import Path
import pandas as pd
from loguru import logger
from matplotlib import pyplot

from tensorflow.python.keras.regularizers import l2
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.layers import GRU

from numpy import array
import matplotlib.pyplot as plt

from experiments.config import data_path, model_plots_path, EPOCHS


class GatedRecurrentNeuralNetwork():
    """ Gated Recurrent Neural Network (gru) with 1-Step Output """

    global gru_model
    global graph

    # Path of ai_models folder under User home
    file_path = str(Path.home()) + model_plots_path
    ai_model_class = "ai.aimodels.GatedRecurrentNeuralNetworkAIModel.GatedRecurrentNeuralNetworkAIModel"

    def __init__(self):
        # If the file_path folder does not exist in the file system, create it
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def get_dataset(self, dataset_parameters):
        """ Method that returns the appropriate dataset according to the dataset parameters """

        from experiments.config import dataset_parameters, hyperparameters

        dataset_start_time = dataset_parameters['dataset_start_time']
        dataset_end_time = dataset_parameters['dataset_end_time']
        dataset_window_size = dataset_parameters['window_size']
        dataset_column_names_list = []
        for i in range(dataset_window_size):
            dataset_column_names_list.append('F' + str(i))

        data = pd.read_csv(data_path, sep=',')
        df_data = data[["ap_hi", "ap_lo"]]

        return df_data

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        from experiments.config import dataset_parameters, hyperparameters

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        df = self.normalized_time_series(df=df)

        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              dataset_parameters['window_size'], )
        X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.1, random_state=25,
                                                              shuffle=False, stratify=None)

        # X_train, y_train, X_valid, y_valid, X_test, y_test = self.normalized(X_train, y_train, X_valid, y_valid,
        #                                                                     X_test, y_test)

        gru_model = self.train_gru(X_train, y_train, X_valid, y_valid, dataset_parameters['window_size'])
        # graph = tf.get_default_graph()

        # score, acc
        acc, loss = self.test_gru(gru_model, X_test, y_test, dataset_parameters['window_size'])

        return gru_model, {"accuracy": acc, "loss": loss}  # {"score": score}

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        X, y = self.split_sequences(df, window_size)

        return train_test_split(X, y, test_size=test_ratio, random_state=25, shuffle=False, stratify=None)
        # , shuffle=True, random_state=2, stratify=None)

    def normalized(self, X_train, y_train, X_valid, y_valid, X_test, y_test):
        # MIN MAX NORMALIZATION

        from sklearn.preprocessing import MinMaxScaler

        scaler_X = MinMaxScaler()
        scaler_Y = MinMaxScaler()

        # Get X_train values reshaped in to 2D for scaler
        X_train_values = X_train.reshape(-1, 1)

        # Fit on X_train_values and transform
        X_train_normalized = scaler_X.fit_transform(X_train_values)
        # print('Min: %f, Max: %f' % (scaler.data_min_, scaler.data_max_))

        # Transform y_train
        y_train_normalized = scaler_Y.fit_transform(y_train)

        # Transform X_Valid
        X_valid_values = X_valid.reshape(-1, 1)
        X_valid_normalized = scaler_X.transform(X_valid_values)

        # Transform y_valid
        y_valid_normalized = scaler_Y.transform(y_valid)

        # Transform X_test
        X_test_values = X_test.reshape(-1, 1)
        X_test_normalized = scaler_X.transform(X_test_values)

        # Transform y_test
        y_test_normalized = scaler_Y.transform(y_test)

        # Reshape normalized values back to 3-D
        X_train = X_train_normalized.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2])
        X_valid = X_valid_normalized.reshape(X_valid.shape[0], X_valid.shape[1], X_valid.shape[2])
        X_test = X_test_normalized.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

        y_train = y_train_normalized.reshape(y_train.shape[0], y_train.shape[1])
        y_valid = y_valid_normalized.reshape(y_valid.shape[0], y_valid.shape[1])
        y_test = y_test_normalized.reshape(y_test.shape[0], y_test.shape[1])

        return X_train, y_train, X_valid, y_valid, X_test, y_test

    def normalized_time_series(self, df):
        from sklearn import preprocessing

        x = df.values  # returns a numpy array

        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        normalized_df = pd.DataFrame(x_scaled)
        return normalized_df

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
            X.append(seq_x)
            y.append(seq_y)
        X, y = array(X), array(y)
        return X, y

    def train_gru(self, X_train, y_train, X_valid, y_valid, window_size):
        """ Method that creates gru model using x_train and y_train """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        # window_size = 3

        # define model
        model = Sequential()
        model.add(GRU(100, activation='relu', return_sequences=True, input_shape=(window_size, n_features),
                      kernel_regularizer=l2(0.01), recurrent_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
        model.add(GRU(100, kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2, kernel_regularizer=l2(0.01)))
        model.compile(optimizer='adam', loss='mse',
                      metrics=[tf.keras.metrics.MeanAbsoluteError(), tf.keras.metrics.MeanSquaredError(),
                               tf.keras.metrics.RootMeanSquaredError(), tf.keras.metrics.MeanSquaredLogarithmicError()])

        # fit model
        history = model.fit(X_train, y_train, epochs=EPOCHS, validation_data=(X_valid, y_valid), verbose=0)
        self.plot_model(history)

        return model

    def test_gru(self, gru_model, X_test, y_test, window_size):
        """ Method that calculates score using X_test and y_test on the created gru model """

        """ Evaluation function of an input given a score """
        yha_predict = gru_model.predict(X_test, verbose=0)
        print(yha_predict)
        logger.debug(yha_predict)

        """ Evaluation function of an input given a score """
        # (loss, acc) = lstm_model.evaluate(X_test, y_test, verbose=0)
        # print("Loss:", loss)
        # print("Accuracy:", acc)
        score = gru_model.evaluate(X_test, y_test, verbose=1)
        print(score)
        logger.debug(score)

        return score, 97

    def plot_model(self, history):
        # plot loss during training
        # pyplot.subplot(221)
        # pyplot.title('Loss')
        # pyplot.plot(history.history['loss'], 'r--', label='train', )
        # pyplot.plot(history.history['val_loss'], 'b--', label='test')
        # pyplot.legend()

        # plot mae during training
        pyplot.subplot(221)
        # pyplot.title('Mean Absolute Error')
        pyplot.plot(history.history['mean_absolute_error'], 'r--', label='train')
        pyplot.plot(history.history['val_mean_absolute_error'], 'g--', label='test')
        pyplot.xlabel('Epoch')
        pyplot.ylabel('MAE')
        pyplot.tight_layout()
        pyplot.legend()
        pyplot.show()

        # plot mse during training
        pyplot.subplot(222)
        # pyplot.title('Mean Squared Error')
        pyplot.plot(history.history['mean_squared_error'], 'c--', label='train')
        pyplot.plot(history.history['val_mean_squared_error'], 'b--', label='test')
        pyplot.xlabel('Epoch')
        pyplot.ylabel('MSE')
        pyplot.tight_layout()
        pyplot.legend()
        pyplot.show()

        # plot rmse during training
        pyplot.subplot(223)
        # pyplot.title('Root Mean Squared Error')
        pyplot.plot(history.history['root_mean_squared_error'], 'm--', label='train')
        pyplot.plot(history.history['val_root_mean_squared_error'], 'g--', label='test')
        pyplot.xlabel('Epoch')
        pyplot.ylabel('MSE')
        pyplot.tight_layout()
        pyplot.legend()
        pyplot.show()

        # plot msle during training
        pyplot.subplot(224)
        # pyplot.title('Mean Squared Logarithmic Error')
        pyplot.plot(history.history['mean_squared_logarithmic_error'], 'o--', label='train')
        pyplot.plot(history.history['val_mean_squared_logarithmic_error'], 'b--', label='test')
        pyplot.xlabel('Epoch')
        pyplot.ylabel('MSLE')
        pyplot.tight_layout()
        pyplot.legend()
        pyplot.show()

        self.save_model_plot(self.ai_model_class)

    def save_model_plot(self, ai_model_class):
        """ Save model file with pickle """

        ai_model_file_name = self.file_path + "/" + ai_model_class + "_" + str(
            datetime.now().timestamp()) + ".png"
        pyplot.savefig(ai_model_file_name, dpi='figure', format=None, metadata=None,
                       bbox_inches=None, pad_inches=0.1,
                       facecolor='auto', edgecolor='auto',
                       backend=None)
        print("ai_model_file_name:", ai_model_file_name)
        logger.debug("ai_model_file_name:", ai_model_file_name)
        return ai_model_file_name

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
