from abc import abstractmethod
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from  keras.layers import Dense
from keras.layers import LSTM

from ai.aimodels import AbstractAIModel
from pandas import DataFrame
from pandas import concat
import numpy as np

class LongShortTermMemory(AbstractAIModel):
    """ Mutlilayer (LSTM) Perceptron with Multi-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'])

        lstm_model = self.train_lstm(X_train, y_train)

        score = self.test_lstm(lstm_model, X_test, y_test)

        return lstm_model, {"score": score}

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

    def train_lstm(self, X_train, y_train):
        """ X_train ve y_train kullanarak lstm modeli oluşturan metod """

        # flatten input
        n_steps = 3

        # the dataset knows the number of features, e.g. 2
        n_features = X_train.shape[2]

        # define model
        model = Sequential()
        model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
        model.add(LSTM(100, activation='relu'))
        model.add(Dense(n_features))
        model.compile(optimizer='adam', loss='mse')

        return model

    def test_lstm(self, lstm_model, X_test, y_test):
        """ Oluşturulmuş lstm modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """

        for i in range(len(X_test)):
            X_new = np.array([X_test[i]])
            y_new = lstm_model.predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = lstm_model.score(X_test, y_test)
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
