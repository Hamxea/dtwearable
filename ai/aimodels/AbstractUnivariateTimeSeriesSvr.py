from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split

from ai.aimodels.AbstractAIModel import AbstractAIModel


class AbstractUnivariateTimeSeriesSvr(AbstractAIModel):
    """ Time series generation model using SVR for univariate models """

    window_size = None

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)

        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'])

        svr_model = self.train_svr(X_train, y_train)

        score = self.test_svr(svr_model, X_test, y_test)

        return svr_model, {"score": score}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def create_synthetic_dataset(self):
        """ Method that creates a dataset synthetically according to the need """

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
        """ A method that divides the dataset for train and test. As much as test_ratio is reserved for testing. Ratio format is like 0.2 """

        # label_index = df.columns.get_loc("Label")
        label_index = df.shape[1]-1 # Son kolon her zaman label'dır. O yüzden yukarıdaki koda gerek kalmadı. Shape-1 son kolon indeksini verir

        X = df.iloc[:, :label_index].values
        y = df.iloc[:, label_index:].values

        return train_test_split(X, y, test_size = test_ratio, shuffle=False, stratify=None)

    def train_svr(self, X_train, y_train, kernel='rbf'):
        """ Method that creates SVR model using x_train and y_train
            Since the SVR scale is not insensitive, it is necessary to scale the data.
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
        """ Method that calculates score using X_test and y_test on the created SVR model """
        from sklearn.preprocessing import MinMaxScaler

        scaler = MinMaxScaler(feature_range=(0, 1))
        X_test_scaled = scaler.fit_transform(X_test)

        for i in range(len(X_test_scaled)):
            X_new = np.array([X_test_scaled[i]])
            y_new = svr_model.predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = svr_model.score(X_test_scaled, y_test)
        print("Score:", score)

        return score

    def series_to_supervised(self, dataset, n_in=3, n_out=1):
        """ Method to convert dataset format to supervised learning format """

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
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
