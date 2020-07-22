from abc import abstractmethod
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from  keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np

class ConvolutionalNeuralNetwork(AbstractAIModel):
    """ Convolutional Neural Network (CNN) with 1-Step Output """

    global cnn_model
    global graph

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              hyperparameters['n_steps'])
        cnn_model = self.train_cnn(X_train, y_train, hyperparameters['n_steps'])
        graph = tf.get_default_graph()

        with graph.as_default():
            score, acc = self.test_cnn(cnn_model, X_test, y_test, hyperparameters['n_steps'])

        return cnn_model, {"score": score, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        Dataset parametlerine göre train ve test'te kullanılacak dataseti getiren metod
        alt sınıflar tarafından implemente edilecektir
        """
        pass

    def split_dataset(self, df, test_ratio, n_steps):
        """ Dataseti train ve test için bölen metod """

        X, y = self.split_sequences(df, n_steps)

        return train_test_split(X, y, test_size=test_ratio, shuffle=False, stratify=None)

    def split_sequences(self, df, n_steps):
        """ split a multivariate sequence into samples metod"""
        """
        #n_steps_in = 3
        #n_steps_out = 1
        """
        sequences = df.to_numpy()
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the dataset
            if end_ix > len(sequences) - 1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)

        X, y = array(X), array(y)
        return X, y

    def train_cnn(self, X_train, y_train, n_steps):
        """ X_train ve y_train kullanarak cnn modeli oluşturan metod """

        # the dataset knows the number of features, e.g. 2
        n_features = X_train.shape[2]

        # define model
        model = Sequential()
        model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
        model.add(Dense(50, activation='relu'))
        model.add(Dense(n_features))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

        return model

    def test_cnn(self, cnn_model, X_test, y_test, n_steps):
        """ Oluşturulmuş cnn modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """
        X_test = X_test[np.size(X_test, 0) - 1:, :]
        # the dataset knows the number of features, e.g. 2
        n_features = X_test.shape[2]
        # n_steps_in = 3
        X_test = X_test.reshape(1, n_steps, n_features)
        yha_predict = cnn_model.predict(X_test, verbose=0)
        print(yha_predict)

        """ Score verilen bir girişin değerlendirme fonksiyonu """
        score, acc = cnn_model.evaluate(X_test, yha_predict, verbose=0)
        print("Score:", score)
        print(("Accuracy", acc))

        return score, acc

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: Genel tahmin özeliklek kolumlar isimi yazilacak """
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names

