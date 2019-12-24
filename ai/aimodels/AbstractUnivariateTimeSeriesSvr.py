from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split

from ai.aimodels.AbstractAIModel import AbstractAIModel


class AbstractUnivariateTimeSeriesSvr(AbstractAIModel):
    """ Tek değişkenli modeller için SVR kullanarak zaman serisi oluşturma modeli """

    window_size = None

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)

        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'])

        svr_model = self.train_svr(X_train, y_train)

        score = self.test_svr(svr_model, X_test, y_test)

        return svr_model, {"score": score}

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

    # def windowing(self, df):
    #     """ tek boyutlu  veriyi window size'ı kullanarak matrise çeviren metod """
    #
    #     agg_values = self.series_to_supervised(dataset=df, n_in=self.window_size)
    #     df = DataFrame(agg_values)
    #     self.rename_columns(df, 'Feat_')
    #     return df

    def split_dataset(self, df, test_ratio):
        """ Dataseti train ve test için bölen metot. Test_ratio kadarı teste ayrılır. Ratio formatı 0.2 gibidir """

        # label_index = df.columns.get_loc("Label")
        label_index = df.shape[1]-1 # Son kolon her zaman label'dır. O yüzden yukarıdaki koda gerek kalmadı. Shape-1 son kolon indeksini verir

        X = df.iloc[:, :label_index].values
        y = df.iloc[:, label_index:].values

        return train_test_split(X, y, test_size = test_ratio, shuffle=False, stratify=None)

    def train_svr(self, X_train, y_train, kernel='rbf'):
        """ X_train ve y_train kullanarak SVR modeli oluşturan metod
            SVR scale insensitive olmadığı için veriyi scale etmek gerekmektedir
        """

        from sklearn.svm import SVR
        from sklearn.preprocessing import MinMaxScaler

        scaler = MinMaxScaler(feature_range=(0, 1))

        X_train_scaled = scaler.fit_transform(X_train)
        # y_train_scaled = scaler.transform(y_train)

        model = SVR(kernel=kernel)
        model.fit(X_train_scaled, y_train)

        return model

    def test_svr(self, svr_model, X_test, y_test):
        """ Oluşturulmuş SVR modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """
        from sklearn.preprocessing import MinMaxScaler

        scaler = MinMaxScaler(feature_range=(0, 1))
        X_test_scaled = scaler.fit_transform(X_test)

        for i in range(len(X_test_scaled)):
            X_new = np.array([X_test_scaled[i]])
            y_new = svr_model._predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = svr_model.score(X_test_scaled, y_test)
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
