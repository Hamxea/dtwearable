import errno
import os
import pickle
from abc import abstractmethod
from datetime import datetime
from pathlib import Path

from sklearn.model_selection import train_test_split
from statsmodels.tsa.vector_ar.var_model import VAR
import matplotlib.pyplot as plt

from ai.aimodels.AbstractAIModel import AbstractAIModel


class VectorAutoRegression_2(AbstractAIModel):
    """ Vector Auto Regression (VAR) with 1-Step Output """

    # User home altında ai_models klasörünün path'i
    file_path_plot = os.path.join("ai_models", "ai_models_plots")

    def train(self, dataset_parameters, hyperparameters):
        """ The method that trains the model based on dataset parameters and hyperparameters """

        df = self.get_dataset(dataset_parameters)
        # df = self.windowing(df)
        train_data, test_data = self.split_dataset(df, dataset_parameters['test_ratio'], dataset_parameters['window_size'])
        var_model = self.train_var(train_data, dataset_parameters['window_size'])
        score, acc = self.test_var(var_model, test_data)

        return var_model, {"score": score, "accuracy": acc}

    @abstractmethod
    def get_dataset(self, dataset_parameters):
        """
        According to the dataset parameters, the method that brings the dataset to be used in train and test will be implemented by subclasses.
        """
        pass

    def split_dataset(self, df, test_ratio, window_size):
        """ Method that divides dataset for train and test """

        train_data = df[:int((1 - test_ratio) * len(df))]
        test_data = df[int((1 - test_ratio) * len(df)):]

        return train_data, test_data

    def train_var(self, train_data, window_size):
        """ Method that creates the var model using x_train and y_train """

        model = VAR(endog=train_data)
        model_fit = model.fit()
        print(model_fit.summary())
        self.plot_model(model_fit)

        return model_fit

    def test_var(self, var_model, test_data):
        """ Method that calculates score using X_test and y_test on the created var model """

        # make prediction of test validation data with 1 step_out
        # var_model.y
        prediction = var_model.forecast(test_data.to_numpy(), steps=1)
        print(prediction)

        return 1, 0

    def plot_model(self, model_fit):
        """ Epoch sayısı üzerinden eğitim kaybı ile doğrulama kaybının grafiğini çizer. """

        try:
            os.makedirs(self.file_path_plot)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        ai_model_plot_file_name = os.path.join(self.file_path_plot, __name__ + "_" + str(datetime.now().timestamp()) + ".png")

        model_plot = model_fit.plot()
        # save the figure
        pickle.dump(model_plot, open(ai_model_plot_file_name, 'wb'))
        print("ai_model_file_name:", ai_model_plot_file_name)

        plt.show()

        return

    def rename_columns(self, df, identifier='Feat_'):
        """ TODO: General forecast will be written, especially the names of the columns """
        """ Method to change df column names """

        col_count = len(df.columns)
        column_names = []
        for i in range(col_count - 1):
            column_names.append(identifier + str(i))
        column_names.append('Label')
        df.columns = column_names
