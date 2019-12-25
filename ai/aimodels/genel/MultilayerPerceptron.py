from abc import abstractmethod
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

from ai.aimodels.AbstractAIModel import AbstractAIModel
from numpy import array
from pandas import DataFrame
from pandas import concat
import numpy as np
import json

class MutlilayerPerceptron(AbstractAIModel):
    """ Mutlilayer (MLP) Perceptron with Multi-Step Output """

    def train(self, dataset_parameters, hyperparameters):
        """ dataset parametreleri ve hiperparametrelere göre modeli eğiten metod """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        train_data, test_data = self.split_dataset(df, hyperparameters['train_split_value'])

        # convert into input/output
        X_train, y_train = self.split_sequences(train_data, hyperparameters['n_steps_in'],
                                                hyperparameters['n_steps_out'])

        mlp_model = self.train_mlp(X_train, y_train)

        # convert into input/output
        X_test, y_test = self.split_sequences(test_data, hyperparameters['n_steps_in'],
                                              hyperparameters['n_steps_out'])

        # flatten input
        n_input = X_test.shape[1] * X_test.shape[2]

        # y_test = test_data.reshape(1, n_input)

        X_test = test_data.reshape(1, n_input)
        score = self.test_mlp(mlp_model, X_test, y_test)

        return mlp_model, {"score": score}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        Dataset parametlerine göre train ve test'te kullanılacak dataseti getiren metod
        alt sınıflar tarafından implemente edilecektir
        """
        pass

    # split a multivariate sequence into samples
    def split_sequences(self, sequences, n_steps_in, n_steps_out):
        X, y = list(), list()
        for i in range(len(sequences)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out
            # check if we are beyond the dataset
            if out_end_ix > len(sequences):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

    def split_dataset(self, df, train_split_value):
        """ Dataseti train ve test için bölen metod """

        df_numpy = df.to_numpy()

        """Train and Test splits"""
        df_numpy_train = df_numpy[:train_split_value]
        df_numpy_test = df_numpy[train_split_value:]

        return df_numpy_train, df_numpy_test

    def train_mlp(self, X_train, y_train):
        """ X_train ve y_train kullanarak MLP modeli oluşturan metod """

        # flatten input
        n_input = X_train.shape[1] * X_train.shape[2]
        X_train = X_train.reshape((X_train.shape[0], n_input))
        # flatten output
        n_output = y_train.shape[1] * y_train.shape[2]
        y_train = y_train.reshape((y_train.shape[0], n_output))

        # define model
        model = Sequential()
        model.add(Dense(100, activation='relu', input_dim=n_input))
        model.add(Dense(n_output))
        model.compile(optimizer='adam', loss='mse')
        # fit model
        model.fit(X_train, y_train, epochs=2000, verbose=0)

        return model

    def test_mlp(self, mlp_model, X_test, y_test):
        """Oluşturulmuş mlp modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod """

        X_new = mlp_model.predict(X_test, verbose=0)
        # score = mlp_model.evaluate(X_new, y_test)
        # print("Score:", score)

        return json.dumps(X_new)

    """
    def test_mlp(self, mlp_model, X_test, y_test):
        Oluşturulmuş MLP modeli üzerinde X_test ve y_test kullanarak score hesaplayan metod 

        for i in range(len(X_test)):
            X_new = np.array([X_test[i]])
            y_new = mlp_model.predict(X_new)
            print("X=%s, Predicted=%s" % (X_new[0], y_new[0]))

        score = mlp_model.evaluate(X_test, y_test)
        #score = model.evaluate(x_test, y_test, batch_size=128)
        print("Score:", score)

        return score

    """
