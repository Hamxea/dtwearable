from abc import abstractmethod

import numpy as np
from pandas import DataFrame
from pandas import concat
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score, RepeatedKFold
from sklearn.neighbors import KNeighborsRegressor

from sklearn.preprocessing import MinMaxScaler

from ai.aimodels.AbstractAIModel import AbstractAIModel


class AbstractUnivariateTimeSeriesKNN(AbstractAIModel):
    """ Time series generation model using knn for univariate models """

    window_size = None

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)

        X_train, X_test, y_train, y_test = self.split_dataset(df, dataset_parameters['test_ratio'])

        knn_model, mean_absolute_error_mean, mean_absolute_error_std = self.train_knn(X_train,
                                                                                      y_train)

        score = self.test_knn(knn_model, X_test, y_test)

        return knn_model, {"Mean Absolute Error (mean)": mean_absolute_error_mean,
                           "Mean Absolute Error (std)": mean_absolute_error_std, "score": score}

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

    def split_dataset(self, df, test_ratio):
        """ A method that divides the dataset for train and test. As much as test_ratio is reserved for testing.
        Ratio format is like 0.2 """

        # label_index = df.columns.get_loc("Label")
        label_index = df.shape[
                          1] - 1  # Son kolon her zaman label'dır. O yüzden yukarıdaki koda gerek kalmadı. Shape-1 son kolon indeksini verir

        X = df.iloc[:, :label_index].values
        y = df.iloc[:, label_index:].values

        return train_test_split(X, y, test_size=test_ratio, shuffle=False, stratify=None)

    def train_knn(self, X_train, y_train, kernel='rbf'):
        """ Method that creates knn model using x_train and y_train
            Since knn scale is not insensitive, it is necessary to scale the data.
        """

        scaler = MinMaxScaler(feature_range=(0, 1))

        X_train_scaled = scaler.fit_transform(X_train)
        # y_train_scaled = scaler.transform(y_train)

        y_train = y_train.reshape(y_train.shape[0], )

        # define the model
        model = KNeighborsRegressor(n_neighbors=3)
        model.fit(X_train_scaled, y_train)

        # evaluate the model
        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        n_scores = cross_val_score(model, X_train_scaled, y_train, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1,
                                   error_score='raise')
        # report performance
        print('MAE: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))

        return model, np.mean(n_scores), np.std(n_scores)

    def test_knn(self, knn_model, X_test, y_test):
        """ Method that calculates score using X_test and y_test on the created knn model """

        scaler = MinMaxScaler(feature_range=(0, 1))
        X_test_scaled = scaler.fit_transform(X_test)

        for i in range(len(X_test_scaled)):
            X_new = np.array([X_test_scaled[i]])
            y_new = knn_model.predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = knn_model.score(X_test_scaled, y_test)
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
