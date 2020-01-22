from abc import abstractmethod
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from  keras.layers import Dense
from keras.layers import LSTM

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
import numpy as np


class LongShortTermMemory(AbstractAIModel):
    """ Long Short TermMemory (lstm) with 1-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'],
                                                              hyperparameters['n_steps'],)
        lstm_model = self.train_lstm(X_train, y_train, hyperparameters['n_steps'])
        score, acc = self.test_lstm(lstm_model, X_test, y_test, hyperparameters['n_steps'])

        return lstm_model, {"score": score, "accuracy": acc}

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

    def train_lstm(self, X_train, y_train, n_steps):
        """ X_train ve y_train kullanarak lstm modeli oluşturan metod """

        # flatten input and choose the number of features
        n_features = X_train.shape[2]
        #n_steps = 3

        # define model
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(n_features))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

        # fit model
        model.fit(X_train, y_train, epochs=400, verbose=0)

        return model

    def test_lstm(self, lstm_model, X_test, y_test, n_steps):
        """ Oluşturulmuş lstm modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """
        #n_steps = 3
        # flatten input and choose the features

        X_test = X_test[np.size(X_test, 0)-1:, :]
        print(X_test)
        print(type(X_test))
        print(X_test.shape)
        n_features = X_test.shape[2]
        print(n_features)
        X_test = X_test.reshape(1, n_steps, n_features)
        print(X_test)
        yha_predict = lstm_model.predict(X_test, verbose=0)
        print(yha_predict)
        print(type(X_test))
        """
        for i in range(0, np.size(X_test, 0) - 1):
           # n_features = X_test[i].shape[1]
            X_test = X_test [:,i]
            n_features = X_test.shape[1]
            print(n_features)
            print(X_test)
            X_test = X_test.reshape(1, n_steps, n_features)
            print(X_test)
            print(X_test.shape)
            #yha_predict = lstm_model.predict(X_test[i], verbose=0)
            #print(yha_predict)
            """

        """ 
        print(np.size(X_test, 0) - 1)
        for i in range(np.size(X_test, 0) - 1):
            # flatten input and choose the features
            print("next line \n")
            X_test = X_test[i]
            print(X_test[i])
            print(X_test[i].shape)
            # n_features = X_test.shape[1]
            X_test[i] = X_test[i].reshape(1, n_steps, 6)
            yha_predict = lstm_model.predict(X_test[i], verbose=0)"""



        """ Score verilen bir girişin değerlendirme fonksiyonu """
        (score, acc) = lstm_model.evaluate(X_test, yha_predict, verbose=0)
        #print("Score:", score)

        #return 1, 1
        return (score, acc)

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: Genel tahmin özeliklek kolumlar isimi yazilacak """
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
