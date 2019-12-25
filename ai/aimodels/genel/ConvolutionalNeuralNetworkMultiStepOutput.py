from abc import abstractmethod
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from  keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

from ai.aimodels import AbstractAIModel
from pandas import DataFrame
from pandas import concat
import numpy as np

class ConvolutionalNeuralNetworkMultiStepOutput(AbstractAIModel):
    """ Mutlilayer (CNN) Perceptron with Multi-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'])

        cnn_model = self.train_cnn(X_train, y_train)

        score = self.test_cnn(cnn_model, X_test, y_test)

        return cnn_model, {"score": score}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        Dataset parametlerine göre train ve test'te kullanılacak dataseti getiren metod
        alt sınıflar tarafından implemente edilecektir
        """
        pass

    def create_synthetic_dataset(self):
        """ İhtiyaca göre sentetik olarak dataset oluşturan metod """

        df_size = 100
        low = 35
        high = 42

        df = DataFrame(np.random.uniform(low=low, high=high, size=df_size + self.window_size))
        df = round(df, 2)
        return df

    def windowing(self, df):
        """ tek boyutlu  veriyi window size'ı kullanarak matrise çeviren metod """

        agg_values = self.series_to_supervised(dataset=df, n_in=self.window_size)
        df = DataFrame(agg_values)
        self.rename_columns(df, 'Feat_')
        return df

    def split_dataset(self, df, test_ratio):
        """ Dataseti train ve test için bölen metod """

        label_index = df.columns.get_loc("Label")

        X = df.iloc[:, :label_index].values
        y = df.iloc[:, label_index:].values

        return train_test_split(X, y, test_size = test_ratio, shuffle=False, stratify=None)

    def train_cnn(self, X_train, y_train):
        """ X_train ve y_train kullanarak cnn modeli oluşturan metod """

        # choose a number of time steps
        n_steps_in, n_steps_out = 3, 2

        # flatten output
        n_output = y_train.shape[1] * y_train.shape[2]
        y_train = y_train.reshape((y_train.shape[0], n_output))

        # the dataset knows the number of features, e.g. 2
        n_features = X_train.shape[2]

        # define model
        model = Sequential()
        model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps_in, n_features)))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
        model.add(Dense(50, activation='relu'))
        model.add(Dense(n_output))
        model.compile(optimizer='adam', loss='mse')

        # fit model
        model.fit(X_train, y_train, epochs=7000, verbose=0)

        return model

    def test_cnn(self, cnn_model, X_test, y_test):
        """ Oluşturulmuş cnn modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """

        for i in range(len(X_test)):
            X_new = np.array([X_test[i]])
            y_new = cnn_model.predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = cnn_model.score(X_test, y_test)
        print("Score:", score)


        return score

    def series_to_supervised(self, dataset, n_in=3, n_out=1):
        """ Dataset formatını supervised öğrenme formatına çeviren metod """

        cols = list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(dataset.shift(i))
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(dataset.shift(-i))
        # put it all together
        agg = concat(cols, axis=1)
        # drop rows with NaN values
        agg.dropna(inplace=True)
        return agg.values


    def rename_columns(self, df, identifier='Feat_'):
        """ Df kolon isimlerini değiştiren metod """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
