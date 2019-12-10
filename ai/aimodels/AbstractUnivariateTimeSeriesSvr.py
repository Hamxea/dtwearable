import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.model_selection import train_test_split

from ai.aimodels.AbstractAIModel import AbstractAIModel


class AbstractUnivariateTimeSeriesSvr(AbstractAIModel):
    """ """

    window_size = None

    def train(self, dataset_parameters, hyperparameters):
        df = self.get_dataset(dataset_parameters)
        df = self.windowing(df)
        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'])

        svr_model = self.train_svr(X_train, y_train)

        score = self.test_svr(svr_model, X_test, y_test)

        return svr_model, {"score": score}

    def get_dataset(self, dataset_parameters):
        # dataset_start_time = dataset_parameters['dataset_start_time']
        # dataset_end_time = dataset_parameters['dataset_end_time']

        return self.create_synthetic_dataset()

    def create_synthetic_dataset(self):
        df_size = 100
        low = 35
        high = 42

        df = DataFrame(np.random.uniform(low=low, high=high, size=df_size + self.window_size))
        df = round(df, 2)
        return df

    def windowing(self, df):
        agg_values = self.series_to_supervised(dataset=df, n_in=self.window_size)
        df = DataFrame(agg_values)
        self.rename_columns(df, 'Feat_')
        return df

    def split_dataset(self, df, test_ratio):
        """ """
        label_index = df.columns.get_loc("Label")

        X = df.iloc[:, :label_index].values
        y = df.iloc[:, label_index:].values

        return train_test_split(X, y, test_size = test_ratio, shuffle=False, stratify=None)

    def train_svr(self, X_train, y_train):

        from sklearn.svm import SVR

        model = SVR(kernel='rbf')
        model.fit(X_train, y_train)

        return model

    def test_svr(self, svr_model, X_test, y_test):

        for i in range(len(X_test)):
            X_new = np.array([X_test[i]])
            y_new = svr_model.predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = svr_model.score(X_test, y_test)
        print("Score:", score)

        return score

    # transform list into supervised learning format
    def series_to_supervised(self, dataset, n_in=3, n_out=1):
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
        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
