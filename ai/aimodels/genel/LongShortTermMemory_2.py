from abc import abstractmethod
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np


class LongShortTermMemory_2(AbstractAIModel):
    """ Long Short TermMemory (lstm) with 1-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        global lstm_model
        global graph

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              hyperparameters['n_steps'], )
        lstm_model = self.train_lstm(X_train, y_train, hyperparameters['n_steps'])
        graph = tf.get_default_graph()

        with graph.as_default():
            loss, acc = self.test_lstm(lstm_model, X_test, y_test, hyperparameters['n_steps'])

        return lstm_model, {"loss": loss, "accuracy": acc}

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

        return train_test_split(X, y, test_size=test_ratio, random_state=25, shuffle=False, stratify=None)

    def split_sequences(self, df, n_steps):
        """ split a multivariate sequence into samples method"""
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
            X.append(seq_x[:, :-1])
            y.append(seq_y[-1:])
        X, y = array(X), array(y)
        return X, y

    def train_lstm(self, X_train, y_train, n_steps):
        """ X_train ve y_train kullanarak lstm modeli oluşturan metod """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        # n_steps = 3

        # define model
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(6, activation='softmax'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # fit model
        model.fit(X_train, y_train, epochs=50, verbose=0)

        return model

    def test_lstm(self, lstm_model, X_test, y_test, n_steps):
        """ Oluşturulmuş lstm modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """
        # n_steps = 3
        # flatten input and choose the features

        yha_predict = lstm_model.predict(X_test, verbose=0)
        print(yha_predict)

        """ Score verilen bir girişin değerlendirme fonksiyonu """
        (loss, acc) = lstm_model.evaluate(X_test, y_test, verbose=0)
        print("Loss:", loss)
        print("Accuracy:", acc)

        return loss, acc

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: Genel tahmin özeliklek kolumlar isimi yazilacak """
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names